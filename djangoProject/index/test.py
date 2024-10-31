import speech_recognition as sr
import time


# 初始化识别器
recognizer = sr.Recognizer()

# 加载音频文件并读取为二进制流
audio_file_path = "../output.mp3"  # 替换为你的音频文件路径
with open(audio_file_path, 'rb') as audio_file:
    audio_data_bytes = audio_file.read()  # 读取二进制流

# 将二进制流转换为 sr.AudioData
# 参数说明：`sample_rate` 为采样率，`sample_width` 为采样宽度，这两个参数可以根据实际情况调整
# 对于大多数音频文件，可以假设采样率为 16000，采样宽度为 2（16-bit PCM）
audio_data = sr.AudioData(audio_data_bytes, sample_rate=16000, sample_width=2)

# 测量识别时间
start_time = time.time()
try:
    # 使用 Google Web Speech API
    text = recognizer.recognize_google(audio_data)
    print("识别结果:", text)
except sr.UnknownValueError:
    print("未能识别音频")
except sr.RequestError as e:
    print(f"请求错误; {e}")
end_time = time.time()

print(f"识别时间: {end_time - start_time:.2f} 秒")


