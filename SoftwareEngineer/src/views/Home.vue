<!--<template>-->
<!--  <div class="camera-container">-->
<!--    <button @click="startCamera" class="start-button">开始录像</button>-->
<!--    <video ref="video" autoplay style="display: none;"></video>-->
<!--    <button @click="takePhoto" class="capture-button" v-if="cameraStarted">拍照</button>-->
<!--    <canvas ref="canvas" style="display: none;"></canvas>-->
<!--    <img v-if="photo" :src="photo" alt="Captured Photo" class="captured-photo" />-->
<!--    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>-->
<!--  </div>-->
<!--</template>-->

<!--<script setup>-->
<!--import { ref } from 'vue';-->

<!--const errorMessage = ref('');-->
<!--const photo = ref(null);-->
<!--const video = ref(null);-->
<!--const canvas = ref(null);-->
<!--const cameraStarted = ref(false);-->

<!--const startCamera = async () => {-->
<!--  try {-->
<!--    const stream = await navigator.mediaDevices.getUserMedia({ video: true });-->
<!--    video.value.srcObject = stream;-->
<!--    video.value.style.display = 'block';-->
<!--    cameraStarted.value = true;-->
<!--  } catch (error) {-->
<!--    errorMessage.value = `无法访问摄像头: ${error.message}`;-->
<!--  }-->
<!--};-->

<!--const takePhoto = () => {-->
<!--  const videoElement = video.value;-->
<!--  const canvasElement = canvas.value;-->
<!--  canvasElement.width = videoElement.videoWidth;-->
<!--  canvasElement.height = videoElement.videoHeight;-->
<!--  const context = canvasElement.getContext('2d');-->
<!--  context.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);-->
<!--  photo.value = canvasElement.toDataURL('image/png');-->
<!--};-->
<!--</script>-->

<!--<style scoped>-->
<!--.camera-container {-->
<!--  display: flex;-->
<!--  flex-direction: column;-->
<!--  align-items: center;-->
<!--  justify-content: center;-->
<!--  width: 100%;-->
<!--  height: 100%;-->
<!--}-->

<!--video {-->
<!--  width: 100%;-->
<!--  max-width: 640px;-->
<!--  border: 2px solid #ccc;-->
<!--  border-radius: 10px;-->
<!--}-->

<!--.start-button {-->
<!--  margin-top: 20px;-->
<!--  padding: 10px 20px;-->
<!--  font-size: 16px;-->
<!--  background-color: #28a745;-->
<!--  color: white;-->
<!--  border: none;-->
<!--  border-radius: 5px;-->
<!--  cursor: pointer;-->
<!--}-->

<!--.start-button:hover {-->
<!--  background-color: #218838;-->
<!--}-->

<!--.capture-button {-->
<!--  margin-top: 20px;-->
<!--  padding: 10px 20px;-->
<!--  font-size: 16px;-->
<!--  background-color: #007bff;-->
<!--  color: white;-->
<!--  border: none;-->
<!--  border-radius: 5px;-->
<!--  cursor: pointer;-->
<!--}-->

<!--.capture-button:hover {-->
<!--  background-color: #0056b3;-->
<!--}-->

<!--.captured-photo {-->
<!--  margin-top: 20px;-->
<!--  max-width: 640px;-->
<!--  border: 2px solid #ccc;-->
<!--  border-radius: 10px;-->
<!--}-->

<!--.error-message {-->
<!--  color: red;-->
<!--  margin-top: 20px;-->
<!--}-->
<!--</style>-->
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

<template>
  <div id="app">
    <h1>选择图片</h1>
    <div>
      <!-- 文件选择按钮 -->
      <input type="file" @change="handleFileChange" accept="image/*"/>

      <!-- 使用摄像头捕获图片 -->
      <button @click="openCamera">打开摄像头</button>
      <video ref="video" width="300" height="200" autoplay></video>


      <!-- 显示图片 -->
      <div v-if="imageBase64">
        <img :src="imageBase64" alt="图片预览" style="max-width: 300px;"/>
      </div>
    </div>

    <!-- 显示选择方式 -->
    <div v-if="imageBase64">
      <button @click="getImageAnswer">发送到后端</button>
    </div>

    <!-- 摄像头流 -->
    <div v-if="showCamera" style="margin-top: 20px;">

      <button @click="captureImage">捕获图片</button>
    </div>
  </div>
</template>

<script setup>
import {onBeforeMount, ref} from 'vue'
import {useStateStore} from "@/stores/stateStore";

// 图片的Base64编码和信息
const imageBase64 = ref('')
const imageInfo = ref({})

// 控制摄像头显示
const showCamera = ref(false)
const videoElement = ref(null)

// 是否有摄像头
const noCamera = ref(false)

// 处理文件选择
const handleFileChange = async (event) => {
  const file = event.target.files[0]
  if (file) {
    const base64 = await fileToBase64(file)
    imageBase64.value = base64
  }
}

// 文件转Base64
const fileToBase64 = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onloadend = () => resolve(reader.result)
    reader.onerror = reject
    reader.readAsDataURL(file)
  })
}

// 探测是否有摄像头
const detectCamera = async () => {
  const devices = await navigator.mediaDevices.enumerateDevices()
  const videoDevices = devices.filter(device => device.kind === 'videoinput')
  if (videoDevices.length > 0) {
    noCamera.value = false
  } else {
    ErrorPop("Camera not found");
  }
}

// 打开摄像头
const openCamera = async () => {
  await detectCamera()  // 检测摄像头
  if (noCamera.value) {
    return
  }

  showCamera.value = true
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({video: true})
        .then((stream) => {
          videoElement.value.srcObject = stream
        })
        .catch((error) => {
          console.error('摄像头访问失败:', error)
        })
  }
}

// 捕获摄像头图片
const captureImage = () => {
  const canvas = document.createElement('canvas')
  const context = canvas.getContext('2d')
  const video = videoElement.value

  canvas.width = video.videoWidth
  canvas.height = video.videoHeight
  context.drawImage(video, 0, 0, canvas.width, canvas.height)

  const base64Image = canvas.toDataURL('image/png')
  imageBase64.value = base64Image;
  closeCamera()
}

// 关闭摄像头
const closeCamera = () => {
  const stream = videoElement.value.srcObject
  const tracks = stream.getTracks()
  tracks.forEach(track => track.stop())
  showCamera.value = false
}

// 发送图片到后端
const getImageAnswer = async () => {
  console.log('发送图片')
  const timeout = 20000; // 设置超时时间（以毫秒为单位，例如10秒）
  let fileData = imageBase64.value
  imageBase64.value = ""

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
              asks.value[asks.value.length - 1].ai.text += parsedChunk.response;
              expandedMessage.value += parsedChunk.response;

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
/* 这里可以加入样式 */
</style>

