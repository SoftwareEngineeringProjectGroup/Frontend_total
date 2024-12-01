import json, requests, time
from translate import Translator
from django.http import JsonResponse, StreamingHttpResponse
import re

# 获取前端发送的 JSON 数据

data_post = {"prompt": "Is there anything new today"}
a = time.time()
translator = Translator(to_lang="zh")
b = time.time()
prompt = translator.translate(data_post.get("prompt", ""))
print(prompt)
# print(data_post)
url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
data = {
    "user": "test-1",
    "model": "generalv3.5",  # 指定请求的模型
    "messages": [{
        "role": "system",
        "content": "你是英语老师"
    },
        {
            "role": "user",
            "content": prompt
        }
    ],
    "stream": True
}
header = {
    "Authorization": "Bearer HOhEcQykmTZwwUCQrpvX:PhTphCZWLLpRenOihoHY"
}

response = requests.post(url, headers=header, json=data, stream=True)
c = time.time()
print(b - a)
print(c - b)


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


def event_stream():
    for line in response.iter_lines():
        if line:
            print(byte_to_byte(line))


event_stream()
