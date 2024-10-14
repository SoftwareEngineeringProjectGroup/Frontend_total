from django.test import TestCase
import json

# Create your tests here.
import requests


def remove_first_and_last_line(text):
    lines = text.strip().split('\n')
    if len(lines) > 2:
        return '\n'.join(lines[1:-1])
    return ''


# 设置API的URL和请求头部
api_url = "http://localhost:11434/api/generate"  # 将其替换为实际的API端点
headers = {
    "Authorization": "Bearer YOUR_API_KEY",  # 替换为您的API密钥
    "Content-Type": "application/json"
}

# 请求数据
payload = {
    "prompt": "Write a simple HTML webpage, no need to say anything else",
    "model": "gemma2:2b"
}
response_text = ""
# 发送POST请求并处理流式返回
try:
    with requests.post(api_url, headers=headers, json=payload, stream=True) as response:
        # 检查请求是否成功
        response.raise_for_status()

        # 逐行读取流式返回的数据
        for line in response.iter_lines(decode_unicode=True):
            if line:
                # 解析JSON数据
                data = json.loads(line.decode('utf-8').strip()) if isinstance(line, bytes) else json.loads(line.strip())
                print(data)
                response_text += data.get("response", "")
                # 检查是否完成
                if data.get("done", False):
                    break
        print(response_text)
        with open("stream_post_request.html", "w", encoding="utf-8") as f:
            f.write(remove_first_and_last_line(response_text))

except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
