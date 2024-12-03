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
from aip import AipImageClassify
import base64
from .aiback import proxy_generate_request
from .voices import generate_audio, speechToText
from .internets import connect_internet
from .imageRecognize import recognition_image


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

#反馈
def feed_back(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("feedback:",data)
        return JsonResponse({"status": 200})






