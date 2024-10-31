import json
import time
import os
import requests
from django.http import JsonResponse, StreamingHttpResponse, HttpResponseBadRequest
from django.shortcuts import HttpResponse
import re
from translate import Translator
from fish_audio_sdk import Session, TTSRequest, ASRRequest
from io import BytesIO
from .test2 import proxy_generate_request
from .voices import generate_audio, speechToText


# Create your views here.
def hello(request):
    if request.method == "GET":
        dic1 = {"message": "你好"}
        return JsonResponse(dic1)

    return JsonResponse({"message": "不好捏"})


def info_id(request, id):
    if request.method == "GET":
        print(id)
        return HttpResponse(id)


def list_id(request):
    if request.method == "GET":
        with open("./user/data.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        ids = []
        for key in data.keys():
            ids.append(generate_id_item(key, data[key]))
        res = {"code": 0, "message": "", "data": ids}
        print(res)
        return JsonResponse(res)


def generate_id_item(id, dic):
    dic0 = {"id": id,
            "role": dic["role"],
            "title": dic["title"],
            "time": dic["time"]}
    return dic0


# def proxy_generate_request(request):
#     if request.method == 'POST':
#         # 获取前端发送的 JSON 数据
#         data = json.loads(request.body)
#
#         # 向localhost:11434/api/generate发送请求
#         url = "http://localhost:11434/api/generate"
#         headers = {'Content-Type': 'application/json'}
#
#         # 发送POST请求到外部API，使用stream=True来处理流式返回
#         response = requests.post(url, headers=headers, json=data, stream=True)
#
#         # 定义变量来记录整个响应
#         full_response_content = []
#
#         # 定义生成器函数，逐步返回内容
#         def stream_response():
#             for chunk in response.iter_content(chunk_size=8192):
#                 if chunk:
#                     # 记录每个chunk的response到字符串列表中
#                     full_response_content.append(chunk.decode('utf-8'))  # 返回是utf-8编码
#                     # print(chunk.decode('utf-8').encode('utf-8'))
#
#                     yield chunk  # 同时返回bytes给前端
#
#         # 将流式数据逐步返回给前端
#         streaming_response = StreamingHttpResponse(stream_response(), content_type=response.headers.get('Content-Type'))
#
#         # 将完整的响应内容组合成一个字符串
#         complete_response_str = ''.join(full_response_content)
#
#         # 后端得到的信息等
#
#         return streaming_response
#
#     return JsonResponse({"error": "只能POST请求"}, status=405)


def connect_internet(request):
    if request.method == 'POST':
        # 获取前端发送的 JSON 数据
        data_post = json.loads(request.body)
        a = time.time()
        translator = Translator(to_lang="zh")
        prompt = translator.translate(data_post.get("prompt", ""))
        # print(data_post)
        url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
        data = {
            "user": "test-1",
            "model": "generalv3.5",  # 指定请求的模型
            "messages": [{
                "role": "system",
                "content": "你是搜索系统，只能用英语回复我"
            },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": True
        }
        header = {
            "Authorization": "Bearer HOhEcQykmTZwwUCQrpvX:PhTphCZWLLpRenOihoHY"  # 注意此处替换自己的APIPassword
        }
        response = requests.post(url, headers=header, json=data, stream=True)

        # 将二进制格式转换成类似gemma的返回
        def byte_to_byte(by: bytes):
            str_by = by.decode('utf-8')
            # 正则表达式匹配 "content" 后面的内容
            pattern = r'"content":"(.*?)"}'

            # 匹配了回复信息
            text = ''
            try:
                text = re.search(pattern, str_by).group(1)
            except AttributeError:
                text = ''

            chunk = '{"response":"' + text + '","done":false}\n'
            return chunk.encode('utf-8')

        # 流式响应
        # 完整接收所有的内容
        full_response_content = []
        for chunk0 in response.iter_content(chunk_size=8192):
            # print(byte_to_byte(chunk0), chunk0)
            full_response_content.append(byte_to_byte(chunk0))

        # 将整个响应的内容流式地返回
        # print(full_response_content)

        def stream_response():
            for item in full_response_content:
                time.sleep(0.5)
                yield item

        # 将流式数据返回给前端
        response = StreamingHttpResponse(stream_response(), content_type='text/event-stream')
        response.headers['Cache-Control'] = 'no-cache'  # 修改为使用 headers 属性
        response.headers['X-Accel-Buffering'] = 'no'  # 禁用 Nginx 缓存（如果适用）
        b = time.time()
        print(b - a, "s")

        return response

    return JsonResponse({"error": "只能POST请求"}, status=405)


# 测试返回文件
def generate_bubble_sort_file(request):
    # Bubble sort code
    bubble_sort_code = """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

if __name__ == "__main__":
    arr = [64, 34, 25, 12, 22, 11, 90]
    bubble_sort(arr)
    print("Sorted array is:", arr)
"""
    # Define the file path where the generated file will be saved temporarily
    file_path = "./files/bubble_sort.py"
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    print(BASE_DIR)
    # Write the bubble sort code to the file
    with open(file_path, "w") as file:
        file.write(bubble_sort_code)

    # Return the file as a downloadable response
    with open(file_path, "rb") as file:
        response = HttpResponse(file.read(), content_type="application/octet-stream")
        response["Content-Disposition"] = f"attachment; filename={os.path.basename(file_path)}"
        return response
