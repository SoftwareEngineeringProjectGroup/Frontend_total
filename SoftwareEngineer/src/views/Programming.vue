<template>
  <div>
    <!-- 按钮点击时触发文件选择框 -->
    <button @click="triggerFileInput">选择图片</button>

    <!-- 隐藏的文件输入框 -->
    <input ref="fileInput" type="file" @change="onFileChange" style="display: none" />

    <!-- 显示选择的图片 -->
    <div v-if="imageUrl">
      <img :src="imageUrl" alt="上传的图片" style="max-width: 100%; height: auto;" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 响应式数据，存储图片的 URL
const imageUrl = ref('');

// 使用 ref 获取文件输入框
const fileInput = ref(null);

// 手动触发文件选择框
const triggerFileInput = () => {
  fileInput.value.click(); // 触发隐藏的文件输入框
};

// 处理文件选择
const onFileChange = (event) => {
  const file = event.target.files[0]; // 获取选中的文件
  if (file) {
    const reader = new FileReader(); // 创建 FileReader 实例
    reader.onload = (e) => {
      imageUrl.value = e.target.result; // 图片读取完成后设置 imageUrl 为文件内容（base64 编码）
    };
    reader.readAsDataURL(file); // 将文件读取为 Data URL（base64 编码）
  }
};
</script>

<style scoped>
button {
  margin-bottom: 10px;
}

img {
  margin-top: 10px;
  max-width: 100%; /* 保证图片在屏幕宽度内显示 */
  height: auto;
}
</style>
