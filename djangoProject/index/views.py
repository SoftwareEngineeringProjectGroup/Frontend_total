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
from .aiback import proxy_generate_request
from .voices import generate_audio, speechToText
from .internets import connect_internet


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



