from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import HttpResponse
import requests, json
import time
import re
from aip import AipImageClassify
import base64


# full_response_content = []


def recognition_image(request):
    if request.method == 'POST':
        # 获取前端发送的 JSON 数据
        data = json.loads(request.body)

        # 向localhost:11434/api/generate发送请求
        url = "http://localhost:11434/api/generate"
        headers = {'Content-Type': 'application/json'}


        name = get_name(data["image"], data["prompt"])
        dataAi = {"prompt": "short introduce " + name + " in 300 words", "model": data["model"]}

        # 发送POST请求到外部API，使用stream=True来处理流式返回
        response = requests.post(url, headers=headers, json=dataAi, stream=True)

        # 定义列表来记录整个响应内容

        # 定义生成器函数，逐步返回内容
        def stream_response():
            complete_response = ''
            try:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        # 记录每个chunk的response到字符串列表中
                        str_chunk = chunk.decode('utf-8')
                        pattern = r',"response":"(.*?)"'
                        # 使用 re.search 查找匹配的内容
                        match = re.search(pattern, str_chunk)
                        if match:
                            # 提取捕获组中的内容
                            response_content = match.group(1)
                            # print(f"匹配到的内容: {response_content}")
                            # print(chunk.decode('utf-8'))
                            complete_response += response_content
                            # print(json.dumps({"response": response_content}))
                            yield chunk  # 同时返回bytes给前端
                        else:
                            print("没有找到匹配的内容")
                        # full_response_content.append(json.load(chunk.decode('utf-8'))["response"])  # 返回是utf-8编码

            finally:
                # 在所有的chunk都处理完毕后，将完整的响应内容组合成一个字符串
                complete_response = complete_response.replace('\\n', '\n')

        #
        # # 将流式数据逐步返回给前端
        streaming_response = StreamingHttpResponse(stream_response(), content_type=response.headers.get('Content-Type'))

        # 将完整的响应内容组合成一个字符串
        # complete_response = "".join(full_response_content)

        # 可以在这里对完整的响应内容做一些其他处理，比如写日志或者保存到数据库
        # 比如写日志：

        return streaming_response


def get_car(base,tip=True):
    # 设置App ID、API Key、Secret Key
    APP_ID = '116492337'
    API_KEY = 'WMu29FmfSnE8RmTb0FnhXdEX'
    SECRET_KEY = 'duodCnpj8EhDiDqthBHdIb6ScjuIbYK1'

    # 初始化AipOcr对象
    client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)

    a = time.time()
    if tip:
        # 去掉前缀 `data:image/png;base64,`
        base64_string = base.split(",")[1]
        binary_data = base64.b64decode(base64_string)
    else:
        binary_data = base
    b = time.time()
    """ 调用汽车识别 """
    options = {}
    options["top_num"] = 1
    if tip:
        result = client.carDetect(binary_data, options)
    else:
        result = client.carDetectUrl(binary_data, options)
    c = time.time()
    # print("log:", b - a)
    # print("get", c - b)
    print("car: ",result["result"][0]["name"])
    return result["result"][0]["name"]


def get_name(base, prompt):
    tip=True
    if "https" in prompt:
        # 匹配 URL 的正则表达式
        pattern = r"https://.*"
        # 使用 re.search 找到匹配的 URL
        base = re.search(pattern, prompt).group(0)
        tip=False

    try:
        if "car" in prompt:
            return get_car(base,tip)
        elif "plant" in prompt:
            return get_plant(base,tip)
        elif "animal" in prompt:
            return get_animal(base,tip)
        else:
            return "Kobe"
    except Exception as e:
        return "Kobe"


def get_plant(base,tip=True):
    # 设置App ID、API Key、Secret Key
    APP_ID = '116492337'
    API_KEY = 'WMu29FmfSnE8RmTb0FnhXdEX'
    SECRET_KEY = 'duodCnpj8EhDiDqthBHdIb6ScjuIbYK1'

    # 初始化AipOcr对象
    client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)

    a = time.time()

    if tip:
        # 去掉前缀 `data:image/png;base64,`
        base64_string = base.split(",")[1]
        binary_data = base64.b64decode(base64_string)
    else:
        binary_data = base


    b = time.time()
    """ 调用植物识别 """
    options = {}
    options["top_num"] = 1
    if tip:
        result = client.plantDetect(binary_data, options)
    else:
        result = client.plantDetectUrl(binary_data, options)
    c = time.time()
    # print("log:", b - a)
    # print("get", c - b)
    print("plant",result["result"][0]["name"])
    return result["result"][0]["name"]


def get_animal(base,tip=True):
    # 设置App ID、API Key、Secret Key
    APP_ID = '116492337'
    API_KEY = 'WMu29FmfSnE8RmTb0FnhXdEX'
    SECRET_KEY = 'duodCnpj8EhDiDqthBHdIb6ScjuIbYK1'

    # 初始化AipOcr对象
    client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)

    a = time.time()
    if tip:
        # 去掉前缀 `data:image/png;base64,`
        base64_string = base.split(",")[1]
        binary_data = base64.b64decode(base64_string)
    else:
        binary_data = base
    b = time.time()
    """ 调用动物识别 """
    options = {}
    options["top_num"] = 1
    if tip:
        result = client.animalDetect(binary_data, options)
    else:
        result = client.animalDetectUrl(binary_data, options)
    c = time.time()
    # print("log:", b - a)
    # print("get", c - b)
    print("animal: ",result["result"][0]["name"])
    return result["result"][0]["name"]
