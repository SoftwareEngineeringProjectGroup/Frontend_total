<template>
  <div class="container" :style="{ height: containerHeight + 'px' }">
    <!-- 文件选择显示区域，放在输入框上方 -->
    <div v-if="selectedFile" class="file-info">
      <span class="file-name">{{ selectedFile.name }}</span>
      <button @click="removeFile" class="delete-btn">Delete</button>
    </div>

    <!-- 输入框在最下方 -->
    <InputBox
        v-model="inputValue"
        @input="updateHeight"
        @keydown="handleKeyDown"
    />

    <!-- 图标行 -->
    <div class="icon-row">
      <!-- MessageBox, 让点击图标触发文件选择 -->
      <el-icon class="message-box" @click="triggerFileUpload">
        <MessageBox />
      </el-icon>
      <!-- Upload 靠右 -->
      <el-icon class="upload" @click="uploadContent">
        <Upload />
      </el-icon>
    </div>

    <!-- 隐藏的文件输入框，用于文件选择，只允许上传编程文件 -->
    <input
        type="file"
        ref="fileInput"
        style="display: none"
        @change="handleFileChange"
        accept=".js,.py,.java,.cpp,.go,.ts,.html,.css,.rb,.php"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onBeforeMount, defineEmits } from 'vue';
import InputBox from "@/components/Programming_dev_1/InputBox.vue";
import { Upload, MessageBox } from "@element-plus/icons-vue";
import { useStateStore } from "@/stores/stateStore.ts";

const inputValue = ref(''); // 存储输入框的值
const containerHeight = ref(92); // 父容器初始高度

let isFirstTime = 0;
const emit = defineEmits(['firstUpload', 'uploadMessage']);

// 文件信息
const selectedFile = ref<File | null>(null);

// 设置baseURL
const stateStore = useStateStore();
let baseURL = '';
onBeforeMount(() => {
  if (stateStore.baseUrl == "0") {
    alert("Please set an IPv4 address")
  }
  baseURL = stateStore.baseUrl;
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
    // 1. 让整个initialmode组件宽度压缩到pagewithoutsidebar的左半边，在父组件中codeBox要出现在右半边
    if (isFirstTime === 0) {
      console.log("WholeInputBox中的isFirstTime是0")
      emit("firstUpload", ref(1));
      isFirstTime = 1;
    }
    // 2. 上传输入内容给initialmode，在chatbox弹出用户输入
    emit("uploadMessage", inputValue.value.trim());

    // 3. 调用ollamaapi，左上方出现ai聊天框

    // 最后输入框清零
    inputValue.value = '';
    containerHeight.value = 92;

    // 上传文件
    if (selectedFile.value) {
      const formData = new FormData();
      formData.append("file", selectedFile.value);

      // 上传文件
      const response = await fetch(`${baseURL}/upload`, {
        method: "POST",
        body: formData
      });

      if (response.ok) {
        console.log("文件上传成功");
        alert("文件上传成功");
      } else {
        console.error("文件上传失败");
        alert("文件上传失败，请重试");
      }
    }
  }
  catch (error) {
    // 错误处理
    console.error('上传失败:', error);
    alert('上传失败，请稍后重试！');
  }
};

// 处理按键事件
const handleKeyDown = (event: KeyboardEvent) => {
  // 如果按下的是 Shift + Enter
  if (event.shiftKey && event.key === 'Enter') {
    // 允许换行，默认行为
    return;
  }

  // 如果按下的是 Enter
  if (event.key === 'Enter') {
    event.preventDefault(); // 阻止换行行为
    uploadContent(); // 触发上传
  }
};

// 文件上传功能
const triggerFileUpload = () => {
  // 触发文件选择框
  const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement;
  if (fileInput) {
    fileInput.click();
  }
};

// 处理文件选择
const handleFileChange = async (event: Event) => {
  const input = event.target as HTMLInputElement;
  const files = input?.files;

  if (files && files.length > 0) {
    const file = files[0];

    // 检查文件类型
    const allowedExtensions = ['js', 'py', 'java', 'cpp', 'go', 'ts', 'html', 'css', 'rb', 'php'];
    const fileExtension = file.name.split('.').pop()?.toLowerCase();

    if (!fileExtension || !allowedExtensions.includes(fileExtension)) {
      alert('Only programming files are allowed: .js, .py, .java, .cpp, .go, .ts, .html, .css, .rb, .php');
      return;
    }

    // 检查是否只选择了一个文件
    if (files.length > 1) {
      alert('Please upload only one file');
      return;
    }

    // 选择文件
    selectedFile.value = file;
    console.log("文件选择：", file);
  }
};

// 删除选中的文件
const removeFile = () => {
  selectedFile.value = null;
};
</script>
<style scoped>
.container {
  display: flex; /* 使用 Flexbox 布局 */
  flex-direction: column; /* 垂直排列 */
  background-color: #fafafa;
  border-radius: 8px; /* 圆角 */
  box-shadow: 2px 4px 6px rgba(0.1, 0, 0, 0.5); /* 阴影效果 */
  width: 600px; /* 宽度固定 */
  padding: 10px; /* 内边距 */
  box-sizing: border-box; /* 包括 padding 在内的总宽度计算 */
}

.icon-row {
  display: flex; /* 水平排列 */
  justify-content: space-between; /* 两端对齐 */
  align-items: center; /* 垂直居中 */
  margin-top: 10px; /* 图标行与输入框之间的间距 */
  width: 100%; /* 占满容器宽度 */
}

.message-box {
  font-size: 28px; /* 调整 MessageBox 图标大小 */
  color: #737373; /* 默认图标颜色 */
  cursor: pointer; /* 鼠标悬停显示为手型 */
}

.message-box:hover {
  color: #ff0000; /* 悬停时图标颜色变化 */
}

.upload {
  font-size: 28px; /* 调整 Upload 图标大小 */
  color: #737373; /* 默认图标颜色 */
  cursor: pointer; /* 鼠标悬停显示为手型 */
}

.upload:hover {
  color: #007bff; /* 悬停时图标颜色变化 */
}

input[type="file"] {
  display: none;
}

.file-info {
  display: flex;
  justify-content: flex-start; /* 靠左对齐 */
  align-items: center;
  margin-bottom: 10px;
  font-size: 14px;
}

.file-name {
  font-weight: bold;
  color: #333;
  margin-right: 10px;
}

.delete-btn {
  background-color: red;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
}

.delete-btn:hover {
  background-color: darkred;
}
</style>