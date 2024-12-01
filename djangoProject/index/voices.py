from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from fish_audio_sdk import Session, TTSRequest, ASRRequest
from io import BytesIO
import time


def generate_audio(request):
    if request.method == "POST":
        session = Session("b2efe1fb3a7f4986acc416da7708bc27")
        dic1 = {"L": "738d0cc1a3e9430a9de2b544a466a7fc",
                "Di": "54a5170264694bfc8e9ad98df7bd89c3",
                "C": "e4642e5edccd4d9ab61a69e82d4f8a14",
                "S": "e80ea225770f42f79d50aa98be3cedfc",
                "P": "665e031efe27435780ebfa56cc7e0e0d",
                "B": "99503144194c45ed8fb998ceac181dcc",
                "N": "3d1cb00d75184099992ddbaf0fdd7387",
                "De": ""}
        try:
            # 获取请求体中的 JSON 数据
            data = request.POST
            text = data.get("text", "")
            # print(text)
            ref_id = dic1[data.get("id", "De")]
            # print(text)
            if not text:
                return HttpResponseBadRequest("Text is required")

            # 使用 Fish Audio SDK 生成音频数据
            audio_buffer = BytesIO()  # 创建内存中的 BytesIO 对象
            for chunk in session.tts(TTSRequest(
                    reference_id=ref_id,
                    text=text
            )):
                audio_buffer.write(chunk)

            # 设置响应
            response = HttpResponse(audio_buffer.getvalue(), content_type='audio/mpeg')
            # response['Content-Disposition'] = 'inline; filename="output.mp3"'
            return response

        except Exception as e:
            # 捕获异常并打印错误信息
            print(f"Error occurred: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


def speechToText(request):
    # Read the audio file
    if request.method == 'POST':
        audio_file = request.FILES.get('audio')
        if not audio_file:
            return JsonResponse({'error': '音频文件未找到'}, status=400)

        # 读取音频文件内容
        audio_data = audio_file.read()
        # b = time.time()

        # 音频识别
        session = Session("b2efe1fb3a7f4986acc416da7708bc27")
        response = session.asr(ASRRequest(audio=audio_data))
        # c = time.time()
        # print(c-b)
        if response.text == ".":
            response.text = ""

        return JsonResponse({'text': response.text}, status=200)
    else:
        return JsonResponse({'error': '仅支持 POST 请求'}, status=405)
