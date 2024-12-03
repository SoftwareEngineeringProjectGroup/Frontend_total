<template>
  <div class="camera-container">
    <!-- 按钮用于开始录像，未开始录像时显示 -->
    <button @click="startCamera" class="start-button" v-if="!cameraStarted">开始录像</button>

    <!-- 视频元素，用于显示实时视频流 -->
    <video ref="video" autoplay style="display: none;"></video>

    <!-- 按钮用于拍照，开始录像后显示 -->
    <button @click="takePhoto" class="capture-button" v-if="cameraStarted">拍照</button>

    <!-- 隐藏的画布元素，用于在拍照时渲染图像 -->
    <canvas ref="canvas" style="display: none;"></canvas>

    <!-- 显示拍摄的照片 -->
    <img v-if="photo" :src="photo" alt="Captured Photo" class="captured-photo" />

    <!-- 上传图片功能 -->

      <input type="file" accept="image/*" @change="handleFileUpload" />


    <!-- 显示错误信息 -->
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 错误信息，用于显示无法访问摄像头时的错误
const errorMessage = ref('');

// 拍摄的照片，保存在此变量中
const photo = ref(null);

// 对应的 DOM 元素引用：视频元素、画布元素、流对象等
const video = ref(null);
const canvas = ref(null);
const cameraStarted = ref(false); // 用于标识是否已经启动摄像头
const stream = ref(null); // 保存媒体流，用于停止摄像头

// 启动摄像头并显示视频流
const startCamera = async () => {
  try {
    // 请求获取用户摄像头权限并返回视频流
    stream.value = await navigator.mediaDevices.getUserMedia({ video: true });

    // 将视频流绑定到 video 元素的 srcObject 上
    video.value.srcObject = stream.value;

    // 显示视频元素
    video.value.style.display = 'block';

    // 更新状态，表示摄像头已经启动
    cameraStarted.value = true;
  } catch (error) {
    // 如果获取摄像头失败，显示错误信息
    errorMessage.value = `无法访问摄像头: ${error.message}`;
  }
};

// 停止摄像头的媒体流
const stopCamera = () => {
  if (stream.value) {
    const tracks = stream.value.getTracks(); // 获取所有视频轨道
    tracks.forEach(track => track.stop()); // 停止每一个视频轨道
  }
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

// 处理文件上传
const handleFileUpload = (event) => {
  const file = event.target.files[0]; // 获取上传的文件

  if (file && file.type.startsWith('image')) {
    // 创建一个 FileReader 来读取文件
    const reader = new FileReader();

    // 读取文件完成后，将其显示为图片
    reader.onload = () => {
      photo.value = reader.result; // 保存图片数据
    };

    // 读取文件
    reader.readAsDataURL(file);
  } else {
    errorMessage.value = '请选择一个有效的图片文件';
  }
};
</script>


<style scoped>
.camera-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
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
</style>


<!--<template>-->
<!-- <Gather/>-->
<!--</template>-->
<!--<script setup>-->

<!--import Gather from "@/components/home_page/gather.vue";-->
<!--</script>-->

<!--<template>-->
<!--  <div>-->
<!--    <h2>上传图片</h2>-->
<!--    <input type="file" @change="handleFileChange" />-->
<!--    <div v-if="imageUrl">-->
<!--      <h3>预览:</h3>-->
<!--      <img :src="imageUrl" alt="Uploaded Image" style="max-width: 200px;" />-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->

<!--<script setup>-->
<!--import { ref } from 'vue'-->
<!--import { useStateStore } from "@/stores/stateStore"-->

<!--// 使用 Pinia 状态管理-->
<!--const store = useStateStore()-->
<!--const imageUrl = ref(null)-->

<!--// 监听 store 中的图片变化-->
<!--imageUrl.value = store.imageUrl-->

<!--// 处理文件选择，转换为 Base64 并存储到 Pinia store-->
<!--const handleFileChange = (event) => {-->
<!--  const file = event.target.files[0]-->
<!--  if (file) {-->
<!--    const reader = new FileReader()-->

<!--    reader.onloadend = () => {-->
<!--      // 将 Base64 字符串存储到 Pinia-->
<!--      store.setuserImagePath(reader.result)-->
<!--    }-->

<!--    reader.readAsDataURL(file) // 将文件转换为 Base64-->
<!--    console.log(store.userImagePath)-->
<!--  }-->

<!--}-->
<!--</script>-->

<!--<template>-->
<!--  <div id="app">-->
<!--    <h1>选择图片</h1>-->
<!--    <div>-->
<!--      &lt;!&ndash; 文件选择按钮 &ndash;&gt;-->
<!--      <input type="file" @change="handleFileChange" accept="image/*"/>-->

<!--      &lt;!&ndash; 使用摄像头捕获图片 &ndash;&gt;-->
<!--      <button @click="openCamera">打开摄像头</button>-->
<!--      <video ref="video" width="300" height="200" autoplay></video>-->


<!--      &lt;!&ndash; 显示图片 &ndash;&gt;-->
<!--      <div v-if="imageBase64">-->
<!--        <img :src="imageBase64" alt="图片预览" style="max-width: 300px;"/>-->
<!--      </div>-->
<!--    </div>-->

<!--    &lt;!&ndash; 显示选择方式 &ndash;&gt;-->
<!--    <div v-if="imageBase64">-->
<!--      <button @click="getImageAnswer">发送到后端</button>-->
<!--    </div>-->

<!--    &lt;!&ndash; 摄像头流 &ndash;&gt;-->
<!--    <div v-if="showCamera" style="margin-top: 20px;">-->

<!--      <button @click="captureImage">捕获图片</button>-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->

<!--<script setup>-->
<!--import {onBeforeMount, ref} from 'vue'-->
<!--import {useStateStore} from "@/stores/stateStore";-->

<!--// 图片的Base64编码和信息-->
<!--const imageBase64 = ref('')-->
<!--const imageInfo = ref({})-->

<!--// 控制摄像头显示-->
<!--const showCamera = ref(false)-->
<!--const videoElement = ref(null)-->

<!--// 是否有摄像头-->
<!--const noCamera = ref(false)-->

<!--// 处理文件选择-->
<!--const handleFileChange = async (event) => {-->
<!--  const file = event.target.files[0]-->
<!--  if (file) {-->
<!--    const base64 = await fileToBase64(file)-->
<!--    imageBase64.value = base64-->
<!--  }-->
<!--}-->

<!--// 文件转Base64-->
<!--const fileToBase64 = (file) => {-->
<!--  return new Promise((resolve, reject) => {-->
<!--    const reader = new FileReader()-->
<!--    reader.onloadend = () => resolve(reader.result)-->
<!--    reader.onerror = reject-->
<!--    reader.readAsDataURL(file)-->
<!--  })-->
<!--}-->

<!--// 探测是否有摄像头-->
<!--const detectCamera = async () => {-->
<!--  const devices = await navigator.mediaDevices.enumerateDevices()-->
<!--  const videoDevices = devices.filter(device => device.kind === 'videoinput')-->
<!--  if (videoDevices.length > 0) {-->
<!--    noCamera.value = false-->
<!--  } else {-->
<!--    ErrorPop("Camera not found");-->
<!--  }-->
<!--}-->

<!--// 打开摄像头-->
<!--const openCamera = async () => {-->
<!--  await detectCamera()  // 检测摄像头-->
<!--  if (noCamera.value) {-->
<!--    return-->
<!--  }-->

<!--  showCamera.value = true-->
<!--  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {-->
<!--    navigator.mediaDevices.getUserMedia({video: true})-->
<!--        .then((stream) => {-->
<!--          videoElement.value.srcObject = stream-->
<!--        })-->
<!--        .catch((error) => {-->
<!--          console.error('摄像头访问失败:', error)-->
<!--        })-->
<!--  }-->
<!--}-->

<!--// 捕获摄像头图片-->
<!--const captureImage = () => {-->
<!--  const canvas = document.createElement('canvas')-->
<!--  const context = canvas.getContext('2d')-->
<!--  const video = videoElement.value-->

<!--  canvas.width = video.videoWidth-->
<!--  canvas.height = video.videoHeight-->
<!--  context.drawImage(video, 0, 0, canvas.width, canvas.height)-->

<!--  const base64Image = canvas.toDataURL('image/png')-->
<!--  imageBase64.value = base64Image;-->
<!--  closeCamera()-->
<!--}-->

<!--// 关闭摄像头-->
<!--const closeCamera = () => {-->
<!--  const stream = videoElement.value.srcObject-->
<!--  const tracks = stream.getTracks()-->
<!--  tracks.forEach(track => track.stop())-->
<!--  showCamera.value = false-->
<!--}-->

<!--// 发送图片到后端-->
<!--const getImageAnswer = async () => {-->
<!--  console.log('发送图片')-->
<!--  const timeout = 20000; // 设置超时时间（以毫秒为单位，例如10秒）-->
<!--  let fileData = imageBase64.value-->
<!--  imageBase64.value = ""-->

<!--  const timeoutPromise = new Promise((_, reject) =>-->
<!--      setTimeout(() => reject(new Error("请求超时")), timeout)-->
<!--  );-->

<!--  try {-->

<!--    const response = await Promise.race([-->
<!--      fetch(baseURL + "/image/recognition", {-->
<!--        method: "POST",-->
<!--        headers: {-->
<!--          "Content-Type": "application/json",-->
<!--        },-->
<!--        body: JSON.stringify({-->
<!--          model: "gemma2:2b",-->
<!--          prompt: "food",-->
<!--          image: fileData-->
<!--        }),-->
<!--      }),-->
<!--      timeoutPromise, // 如果 fetch 未完成，此 promise 将优先返回超时错误-->
<!--    ]);-->


<!--    if (!response.body) {-->
<!--      throw new Error("流式返回没有body");-->
<!--    }-->

<!--    const reader = response.body.getReader();-->
<!--    const decoder = new TextDecoder("utf-8");-->
<!--    let done = false;-->


<!--    while (!done) {-->
<!--      const {value, done: readerDone} = await reader.read();-->
<!--      done = readerDone;-->

<!--      if (value) {-->
<!--        // 解码数据块并按行分割-->
<!--        const chunk = decoder.decode(value, {stream: true});-->
<!--        // console.log("chunk",chunk);-->
<!--        const lines = chunk.split("\n");-->

<!--        // 逐行解析并处理-->
<!--        lines.forEach((line) => {-->
<!--          if (line.trim()) { // 忽略空行-->
<!--            try {-->
<!--              const parsedChunk = JSON.parse(line);-->
<!--              asks.value[asks.value.length - 1].ai.text += parsedChunk.response;-->
<!--              expandedMessage.value += parsedChunk.response;-->

<!--            } catch (parseError) {-->
<!--              console.warn("JSON解析失败，跳过该行: ", line);-->
<!--            }-->
<!--          }-->
<!--        });-->
<!--      }-->
<!--    }-->


<!--    // console.log("流结束");-->
<!--  } catch (error) {-->
<!--    console.error("错误: ", error);-->

<!--    if (error.message === "请求超时") {-->
<!--      ErrorPop("Timeout");-->
<!--    } else {-->
<!--      ErrorPop("404 Warning");-->
<!--    }-->
<!--  }-->
<!--};-->

<!--const stateStore = useStateStore();-->
<!--let baseURL = ""-->
<!--onBeforeMount(() => {-->
<!--  baseURL = stateStore.baseUrl;-->
<!--})-->

<!--//错误弹窗-->
<!--const ErrorPop = (info, time = 3000) => {-->
<!--  ElMessage({-->
<!--    showClose: true,-->
<!--    message: info,-->
<!--    type: 'error',-->
<!--    duration: time-->
<!--  })-->
<!--}-->
<!--</script>-->

<!--<style scoped>-->
<!--/* 这里可以加入样式 */-->
<!--</style>-->

