<template>
  <div class="container" :style="{ height: containerHeight + 'px' }">
    <!-- 输入框在最上方 -->
    <InputBox v-model="inputValue" @input="updateHeight" />
    <!-- 图标行 -->
    <div class="icon-row">
      <!-- MessageBox 靠左 -->
      <el-icon class="message-box">
        <MessageBox />
      </el-icon>
      <!-- Upload 靠右 -->
      <el-icon class="upload" @click="uploadContent">
        <Upload />
      </el-icon>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref, nextTick, onBeforeMount, defineEmits} from 'vue';
import axios from 'axios'; // 引入 Axios
import InputBox from "@/components/Programming_dev_1/InputBox.vue";
import { Upload, MessageBox } from "@element-plus/icons-vue";
import {useStateStore} from "@/stores/stateStore.ts";

const inputValue = ref(''); // 存储输入框的值
const containerHeight = ref(92); // 父容器初始高度

let isFirstTime = 0;
const emit = defineEmits(['firstUpload', 'uploadMessage']);

//设置baseURL
const stateStore = useStateStore();
let baseURL='';
onBeforeMount(() => {
  if(stateStore.baseUrl=="0"){
    alert("Please set an IPv4 address")
  }
  baseURL=stateStore.baseUrl;
});

// 动态调整容器高度
const updateHeight = () => {
  nextTick(() => {
    const inputBox = document.querySelector('.inputBox textarea');
    if (inputBox) {
      containerHeight.value = inputBox.scrollHeight + 62; // 根据输入框内容动态调整父容器高度
    }
  });
};

// 上传内容到后端
const uploadContent = async () => {
  if (inputValue.value.trim() === '') {
    alert('Please input some information'); // 提示用户输入内容
    return;
  }
  try {
    console.log(inputValue.value.trim());
    //1. 让整个initialmode组件宽度压缩到pagewithoutsidebar的左半边，在父组件中codeBox要出现在右半边
    if (isFirstTime === 0){
      console.log("WholeInputBox中的isFirstTime是0")
      emit("firstUpload",ref(1));
      isFirstTime = 1;
    }
    //2. 上传输入内容给initialmode，在chatbox弹出用户输入
    emit("uploadMessage", inputValue.value.trim());

    //3. 调用ollamaapi，左上方出现ai聊天框

    //最后输入框清零
    inputValue.value = '';
  }
  catch (error) {
    // 错误处理
    console.error('上传失败:', error);
    alert('上传失败，请稍后重试！');
  }
};
</script>



<style scoped>
.container {
  display: flex;           /* 使用 Flexbox 布局 */
  flex-direction: column;  /* 垂直排列 */
  background-color: #fafafa;
  border-radius: 8px;      /* 圆角 */
  box-shadow:  2px 4px 6px rgba(0.1, 0, 0, 0.5); /* 阴影效果 */
  width: 600px;            /* 宽度固定 */
  padding: 10px;           /* 内边距 */
  box-sizing: border-box;  /* 包括 padding 在内的总宽度计算 */
}

.icon-row {
  display: flex;           /* 水平排列 */
  justify-content: space-between; /* 两端对齐 */
  align-items: center;     /* 垂直居中 */
  margin-top: 10px;        /* 图标行与输入框之间的间距 */
  width: 100%;             /* 占满容器宽度 */
}

.message-box {
  font-size: 28px;         /* 调整 MessageBox 图标大小 */
  color: #737373;          /* 默认图标颜色 */
  cursor: pointer;         /* 鼠标悬停显示为手型 */
}

.message-box:hover {
  color: #ff0000;          /* 悬停时图标颜色变化 */
}

.upload {
  font-size: 28px;         /* 调整 Upload 图标大小 */
  color: #737373;          /* 默认图标颜色 */
  cursor: pointer;         /* 鼠标悬停显示为手型 */
}

.upload:hover {
  color: #007bff;          /* 悬停时图标颜色变化 */
}

</style>