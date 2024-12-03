<template>
  <div class="container">
    <!-- 左侧：figure-container -->
    <div class="figure-container">
      <!-- 按钮用于开始录像，未开始录像时显示 -->
      <button @click="getCamera" class="start-button">{{ promptC }}</button>

      <!-- 视频元素，用于显示实时视频流 -->
      <video ref="video" autoplay style="display: none;"></video>

      <!-- 隐藏的画布元素，用于在拍照时渲染图像 -->
      <canvas ref="canvas" style="display: none;"></canvas>

      <!-- 显示拍摄的照片 -->
      <img v-if="photo" :src="photo" alt="Captured Photo" class="captured-photo"/>

      <!-- 上传图片功能 -->
      <button class="capture-button" @click="triggerFileInput">
        {{ promptF }}
      </button>
      <el-button size="large" @click="getImageAnswer" v-if="photo" style="margin-top: 10px">Search</el-button>

      <input type="file" accept="image/*" @change="onFileChange" ref="fileInput" style="display: none"/>
    </div>

    <!-- 右侧：show-text -->
    <div class="show-text">
      <div class="answer markdown-body" v-html="renderIt(answer)" v-if="answer"></div>
    </div>
  </div>
</template>

<script setup>
import {ref, onBeforeMount} from 'vue';
import {ElMessage} from "element-plus";
import hljs from "highlight.js";
import MarkdownIt from 'markdown-it';
import 'highlight.js/styles/github.css';
import {useStateStore} from "@/stores/stateStore";

const md = new MarkdownIt({
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return `<pre class="hljs"><code>${hljs.highlight(str, {language: lang}).value}</code></pre>`;
      } catch (__) {
      }
    }
    return `<pre class="hljs"><code>${md.utils.escapeHtml(str)}</code></pre>`;
  },
});

// 错误信息，用于显示无法访问摄像头时的错误
const errorMessage = ref('');

// 拍摄的照片，保存在此变量中
const photo = ref(null);

// 对应的 DOM 元素引用：视频元素、画布元素、流对象等
const video = ref(null);
const canvas = ref(null);
const cameraStarted = ref(false); // 用于标识是否已经启动摄像头
const stream = ref(null); // 保存媒体流，用于停止摄像头
let promptC = ref("Camera")
let promptF = ref("File")
let answer = ref("")


const getCamera = () => {
  if (cameraStarted.value) {
    takePhoto();
    promptC.value = "Delete"
  } else {
    if (photo.value) {
      photo.value = "";
      promptC.value = "Camera"
      console.log(photo.value);
    } else {
      startCamera();
      promptC.value = "Photo"
    }
  }
}

const renderIt = (text) => {
  return md.render(text)
}

// 启动摄像头并显示视频流
const startCamera = async () => {
  try {
    // 请求获取用户摄像头权限并返回视频流
    stream.value = await navigator.mediaDevices.getUserMedia({video: true});

    // 将视频流绑定到 video 元素的 srcObject 上
    video.value.srcObject = stream.value;

    // 显示视频元素
    video.value.style.display = 'block';

    // 更新状态，表示摄像头已经启动
    cameraStarted.value = true;
  } catch (error) {
    // 如果获取摄像头失败，显示错误信息
    errorMessage.value = `无法访问摄像头: ${error.message}`;
    ErrorPop("No camera!!!")
  }
};

// 停止摄像头的媒体流
const stopCamera = () => {
  if (stream.value) {
    const tracks = stream.value.getTracks(); // 获取所有视频轨道
    tracks.forEach(track => track.stop()); // 停止每一个视频轨道
  }
  ;
  cameraStarted.value = false;
};

// 拍照功能：将视频中的当前帧绘制到画布，并生成图片数据
const takePhoto = () => {
  const videoElement = video.value;
  const canvasElement = canvas.value;

  // 设置画布的大小为视频的宽高
  canvasElement.width = videoElement.videoWidth;
  canvasElement.height = videoElement.videoHeight;

  // 获取画布的绘图上下文
  const context = canvasElement.getContext('2d');

  // 将视频当前帧绘制到画布上
  context.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);

  // 将画布内容转化为图片数据并保存
  photo.value = canvasElement.toDataURL('image/png');

  // 停止摄像头录像
  stopCamera();

  // 隐藏视频元素并显示拍摄的照片
  video.value.style.display = 'none';
};

// 使用 ref 获取文件输入框
const fileInput = ref(null);

// 手动触发文件选择框
const triggerFileInput = () => {

  if (photo.value) {
    photo.value = "";
    promptF.value = "File";
    return;
  }
  fileInput.value.click(); // 触发隐藏的文件输入框
  promptF.value = "Delete";
};

// 处理文件选择
const onFileChange = (event) => {
  const file = event.target.files[0]; // 获取选中的文件
  if (file) {
    const reader = new FileReader(); // 创建 FileReader 实例
    reader.onload = (e) => {
      photo.value = e.target.result; // 图片读取完成后设置 imageUrl 为文件内容（base64 编码）

      // console.log(imageUrl.value);
    };
    reader.readAsDataURL(file); // 将文件读取为 Data URL（base64 编码）

    // 重置文件输入框的值，这样即使选择相同的文件也能触发 change 事件
    event.target.value = '';
  }
};


// 发送图片到后端
const getImageAnswer = async () => {
  console.log('发送图片')
  const timeout = 20000; // 设置超时时间（以毫秒为单位，例如10秒）
  let fileData = photo.value
  // photo.value = ""
  answer.value = "";
  // promptC.value = "Camera"
  // promptF.value = "File"

  const timeoutPromise = new Promise((_, reject) =>
      setTimeout(() => reject(new Error("请求超时")), timeout)
  );

  try {

    const response = await Promise.race([
      fetch(baseURL + "/image/recognition", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          model: "gemma2:2b",
          prompt: "food",
          image: fileData
        }),
      }),
      timeoutPromise, // 如果 fetch 未完成，此 promise 将优先返回超时错误
    ]);


    if (!response.body) {
      throw new Error("流式返回没有body");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let done = false;


    while (!done) {
      const {value, done: readerDone} = await reader.read();
      done = readerDone;

      if (value) {
        // 解码数据块并按行分割
        const chunk = decoder.decode(value, {stream: true});
        // console.log("chunk",chunk);
        const lines = chunk.split("\n");

        // 逐行解析并处理
        lines.forEach((line) => {
          if (line.trim()) { // 忽略空行
            try {
              const parsedChunk = JSON.parse(line);

              answer.value += parsedChunk.response;

            } catch (parseError) {
              console.warn("JSON解析失败，跳过该行: ", line);
            }
          }
        });
      }
    }
    // console.log("流结束");
  } catch (error) {
    console.error("错误: ", error);

    if (error.message === "请求超时") {
      ErrorPop("Timeout");
    } else {
      ErrorPop("404 Warning");
    }
  }
};


const stateStore = useStateStore();
let baseURL = ""
onBeforeMount(() => {
  baseURL = stateStore.baseUrl;
})

//错误弹窗
const ErrorPop = (info, time = 3000) => {
  ElMessage({
    showClose: true,
    message: info,
    type: 'error',
    duration: time
  })
}
</script>


<style scoped>
/* 设置容器的布局 */
.container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  height: 100%;
}

.figure-container {
  flex: 1; /* 占据父容器的1份宽度 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.show-text {
  flex: 1; /* 占据父容器的1份宽度 */
  padding: 20px;
  overflow-y: auto; /* 如果内容超出，添加垂直滚动条 */
  max-width: 50%;
}

video {
  width: 100%;
  max-width: 640px;
  border: 2px solid #ccc;
  border-radius: 10px;
}

.start-button {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.start-button:hover {
  background-color: #218838;
}

.capture-button {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.capture-button:hover {
  background-color: #0056b3;
}

.captured-photo {
  margin-top: 20px;
  max-width: 640px;
  border: 2px solid #ccc;
  border-radius: 10px;
}

.error-message {
  color: red;
  margin-top: 20px;
}

.markdown-body {
  box-sizing: border-box;
  min-width: 50px;
  max-width: 500px;
  margin: 2px auto;
  padding: 15px;
  border-radius: 15px;
  max-height: 700px;
  font-size: 16px;
  overflow: auto;
}

@media (max-width: 767px) {
  .container {
    flex-direction: column; /* 屏幕小于767px时，改为上下布局 */
  }

  .figure-container, .show-text {
    max-width: 100%; /* 确保宽度100% */
    margin: 0 auto; /* 居中对齐 */
  }

  .show-text {
    max-height: 60%; /* 限制show-text的最大高度 */
  }
}

/* 隐藏滚动条（Webkit 浏览器） */
.markdown-body::-webkit-scrollbar {
  display: none;
}

/* 隐藏滚动条（Firefox） */
.markdown-body {
  scrollbar-width: none; /* Firefox */
}

</style>