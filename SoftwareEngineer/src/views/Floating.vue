<template>
  <div class="floating-window">
    <div class="drag-icon">
      <!-- 拖动图标，使用 GIF 图像 -->
      <img src="@/assets/test.gif" alt="drag icon" />
    </div>
  </div>
</template>

<script setup>
// import { ipcRenderer } from 'electron';
import { SwitchFilled } from "@element-plus/icons-vue";

function closeWindow() {
  ipcRenderer.send('close-floating-window');
}
</script>

<style scoped>
.floating-window {
  display: inline-flex; /* 使用 inline-flex 让容器大小根据内部元素内容变化 */
  padding: 5px; /* 内边距确保内容和边框之间的距离 */

  border-radius: 20px; /* 设置为 20px，使其形成圆角矩形 */
  overflow: hidden; /* 确保内部内容不会超出圆角边界 */
  position: relative;
  align-items: center; /* 垂直居中对齐 */
  justify-content: center; /* 水平居中对齐 */
  cursor: grab; /* 鼠标变为拖动样式 */
  -webkit-app-region: drag; /* 设置为可拖动区域 */


}

/* 拖动图标样式 */
/* 拖动图标样式 */
.drag-icon {
  width: 100px; /* 设置宽度 */
  height: 100px; /* 设置高度 */
  border-radius: 50%; /* 将图标也设置为圆形 */
  overflow: hidden; /* 隐藏超出的部分 */
  cursor: grab; /* 鼠标变为拖动样式 */
  -webkit-app-region: drag; /* 设置为可拖动区域 */
  display: flex; /* 使用 Flexbox 使内部图像居中对齐 */
  align-items: center;
  justify-content: center;

}

.drag-icon img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 确保图像充满容器并保持比例 */
}
</style>
