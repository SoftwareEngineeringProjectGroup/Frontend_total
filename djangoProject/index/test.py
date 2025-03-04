from aip import AipImageClassify
import time

d = time.time()
# 设置App ID、API Key、Secret Key
APP_ID = '116491847'
API_KEY = 'jpc9DXCrVhNYnMwYInFfBOpq'
SECRET_KEY = 'KQjLTdmVA7ZxSNvY1LaUzuytAkArve73'

# 初始化AipOcr对象
client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)
""" 读取图片 """

a = time.time()


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


image = get_file_content('veg.jpg')
b = time.time()
""" 如果有可选参数 """
options = {}
options["top_num"] = 1
# options["filter_threshold"] = "0.7"
# options["baike_num"] = 5

""" 带参数调用菜品识别 """
result = client.dishDetect(image, options)
c = time.time()
print(d-a)
print("log:", b - a)
print("get", c - b)
print(result)
