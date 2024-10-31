<template>
  <div class="floating-window">
    <div class="drag-icon">
      <!-- 拖动图标，可以是任何图标或样式的元素 -->
      <SwitchFilled/>
    </div>
    <div class="content">
      <!-- 悬浮窗内容 -->
      This is a movable floating window.
    </div>
  </div>
</template>

<script setup>
// import { ipcRenderer } from 'electron';
import{SwitchFilled} from "@element-plus/icons-vue";

function closeWindow() {
  ipcRenderer.send('close-floating-window');
}
</script>

<style scoped>
.floating-window {
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

/* 拖动图标样式 */
.drag-icon {
  width: 30px;
  height: 30px;
  position: absolute;
  top: 10px;
  left: 10px;
  cursor: grab; /* 鼠标变为拖动样式 */
  -webkit-app-region: drag; /* 设置为可拖动区域 */
}

.drag-icon img {
  width: 100%;
  height: 100%;
}

/* 其他内容样式 */
.content {
  padding: 20px;
}
</style>
<!--<template></template>-->
<!--<script></script>-->
