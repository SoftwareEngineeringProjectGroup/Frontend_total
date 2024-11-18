import json, requests, time
from translate import Translator
from django.http import JsonResponse, StreamingHttpResponse
import re


# def connect_internet(request):
#     if request.method == 'POST':
#         # 获取前端发送的 JSON 数据
#         data_post = json.loads(request.body)
#         a = time.time()
#         translator = Translator(to_lang="zh")
#         prompt = translator.translate(data_post.get("prompt", ""))
#         # print(data_post)
#         url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
#         data = {
#             "user": "test-1",
#             "model": "generalv3.5",  # 指定请求的模型
#             "messages": [{
#                 "role": "system",
#                 "content": "你是搜索系统，只能用英语回复我"
#             },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             "stream": True
#         }
#         header = {
#             "Authorization": "Bearer HOhEcQykmTZwwUCQrpvX:PhTphCZWLLpRenOihoHY"
#         }
#         response = requests.post(url, headers=header, json=data, stream=True)
#
#         # 将二进制格式转换成类似gemma的返回
#         def byte_to_byte(by: bytes):
#             str_by = by.decode('utf-8')
#             # 正则表达式匹配 "content" 后面的内容
#             pattern = r'"content":"(.*?)"}'
#
#             # 匹配了回复信息
#             text = ''
#             try:
#                 text = re.search(pattern, str_by).group(1)
#             except AttributeError:
#                 text = ''
#
#             chunk = '{"response":"' + text + '","done":false}\n'
#             return chunk.encode('utf-8')
#
#         # 流式响应
#         # 完整接收所有的内容
#         full_response_content = []
#         for chunk0 in response.iter_content(chunk_size=8192):
#             # print(byte_to_byte(chunk0), chunk0)
#             full_response_content.append(byte_to_byte(chunk0))
#
#         # 将整个响应的内容流式地返回
#         # print(full_response_content)
#
#         def stream_response():
#             for item in full_response_content:
#                 time.sleep(0.5)
#                 yield item
#
#         # 将流式数据返回给前端
#         response = StreamingHttpResponse(stream_response(), content_type='text/event-stream')
#         response.headers['Cache-Control'] = 'no-cache'  # 修改为使用 headers 属性
#         response.headers['X-Accel-Buffering'] = 'no'  # 禁用 Nginx 缓存（如果适用）
#         b = time.time()
#         print(b - a, "s")
#
#         return response
#
#     return JsonResponse({"error": "只能POST请求"}, status=405)

def connect_internet(request):
    # 设置流式API的URL和请求信息
    if request.method == 'POST':
        # 获取请求中的数据
        translatorzh = Translator(to_lang="zh")
        translatoren=Translator(to_lang="en")
        user_input = translatorzh.translate(json.loads(request.body).get('prompt', ''))
        print(user_input)

        # 设置流式API的URL和请求信息
        url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
        data = {
            "user": "test-2",
            "model": "generalv3.5",
            "messages": [
                {"role": "system", "content": ""},
                {"role": "user", "content": user_input+",用英语回复我"}
            ],
            "stream": True
        }
        headers = {
            "Authorization": "Bearer HOhEcQykmTZwwUCQrpvX:PhTphCZWLLpRenOihoHY"
        }

        a = time.time()
        response = requests.post(url, headers=headers, json=data, stream=True)

        response_all = []

        def byte_to_str(by: bytes):
            str_by = by.decode('utf-8')
            # 正则表达式匹配 "content" 后面的内容
            pattern = r'"content":"(.*?)"}'

            # 匹配了回复信息
            try:
                text = re.search(pattern, str_by).group(1)
            except AttributeError:
                text = ''

            return text

        def event_stream():
            try:
                for line in response.iter_lines():
                    if line:
                        text = translatoren.translate(byte_to_str(line))
                        response_all.append(text)
                        chunk = '{"response":"' + text + '","done":false}\n'
                        yield chunk.encode("utf-8")
            finally:
                b = time.time()
                # print("".join(response_all))

        return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

    else:
        return StreamingHttpResponse("Invalid Request Method", status=405)
