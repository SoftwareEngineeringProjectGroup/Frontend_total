from aip import AipImageClassify
import time
d = time.time()
# 设置App ID、API Key、Secret Key
APP_ID = '116492337'
API_KEY = 'WMu29FmfSnE8RmTb0FnhXdEX'
SECRET_KEY = 'duodCnpj8EhDiDqthBHdIb6ScjuIbYK1'

# 初始化AipOcr对象
client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)

a = time.time()
""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

image = get_file_content('cat.png')
b = time.time()

""" 调用动物识别 """
options = {}
options["top_num"] = 1
result=client.animalDetect(image,options)
c = time.time()
print("log:", b - a)
print("get", c - b)
print(result["result"][0]["name"])
