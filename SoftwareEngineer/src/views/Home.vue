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
<template>
 <Gather/>
</template>
<script setup>

import Gather from "@/components/home_page/gather.vue";
</script>

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


