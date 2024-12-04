from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import HttpResponse
import requests, json
import time
import re


# full_response_content = []


def proxy_generate_request(request):
    if request.method == 'POST':
        # 获取前端发送的 JSON 数据
        data = json.loads(request.body)

        # 向localhost:11434/api/generate发送请求
        url = "http://localhost:11434/api/generate"
        headers = {'Content-Type': 'application/json'}
        print("ai-back: ", data)

        # 发送POST请求到外部API，使用stream=True来处理流式返回
        response = requests.post(url, headers=headers, json=data, stream=True)

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
