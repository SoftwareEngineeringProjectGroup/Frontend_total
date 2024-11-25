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
import SideBar from "@/components/SideBar.vue";
import Gather from "@/components/home_page/gather.vue";
</script>