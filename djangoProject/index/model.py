import requests
import json

def construct_prompt(user_input):
    """
    根据用户输入动态生成 Prompt。
    如果用户输入为空，使用默认的 Prompt。
    """
    default_prompt = "Generate a one-week meal plan with breakfast, lunch, and dinner for each day."
    if user_input.strip():
        return f"Based on the user's input, create a one-week meal plan. Input: \"{user_input}\"."
    return default_prompt

def generate_dynamic_recipe(prompt):
    # 构建动态 Prompt（根据需要翻译或调整）
    prompt = construct_prompt(prompt)

    # API 请求设置
    url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
    data = {
        "user": "test-1",
        "model": "gemma2:2b",
        "messages": [
            {"role": "system", "content": "你是一个搜索系统，只能用英语回复我"},
            {"role": "user", "content": prompt}
        ],
        "stream": True  # 流式返回
    }
    headers = {
        "Authorization": "Bearer HOhEcQykmTZwwUCQrpvX:PhTphCZWLLpRenOihoHY",
        "Content-Type": "application/json"
    }

    # 发起 POST 请求
    response = requests.post(url, headers=headers, json=data, stream=True)

    # 定义生成器函数，流式返回 JSON 数据
    def response_stream():
        yield json.dumps({"status": "processing", "message": f"Processing prompt: {prompt}"}) + "\n"

        # 遍历响应流
        for line in response.iter_lines():
            if line:  # 确保不为空行
                decoded_line = line.decode("utf-8")
                try:
                    # 解析 JSON 数据
                    json_line = json.loads(decoded_line)
                    if "choices" in json_line:
                        for choice in json_line["choices"]:
                            if "delta" in choice and "content" in choice["delta"]:
                                recipe_content = choice["delta"]["content"]
                                yield json.dumps({"status": "streaming", "recipe": recipe_content.strip()}) + "\n"
                except json.JSONDecodeError:
                    # 忽略非 JSON 格式的行
                    pass

        yield json.dumps({"status": "done", "message": "Recipe generation complete"}) + "\n"

    return response_stream()
