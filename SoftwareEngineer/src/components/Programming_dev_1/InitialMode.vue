<template>
  <div class="container"
       :style="{
      width: isShrink !== 0 ? '40vw' : '100%',
      alignSelf: isShrink !== 0 ? 'flex-start' : 'center',
    }"
  >
    <div
        v-if="isShrink !== 0"
        class="chatBox"
        :style="{
          overflowY: 'auto'
        }"
    >
      <chatBox :message="userMessage" :msg="responseMessage" :isComplete="isComplete"/>
    </div>
    <div
        class="content"
        :style="{
          transform: isShrink !== 0 ? 'translateY(-50px)' : 'translateY(-50px)',
          bottom: isShrink !== 0 ? '50px' : 'auto',
          position: isShrink !== 0 ? 'absolute' : 'static'
        }"
    >
      <!-- 条件渲染：显示闪烁动画或打字文字 -->
      <h1 v-if="!isTypingStarted && isShrink === 0">
        <span class="dot">!</span>
      </h1>
      <h1 v-if="isTypingStarted && isShrink === 0">{{ displayedText }}</h1>
      <WholeInputBox @firstUpload="firstUploadShrinkSpace" @uploadMessage="uploadMessageToOllama"/>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, defineEmits , onBeforeMount} from 'vue';
import WholeInputBox from "@/components/Programming_dev_1/WholeInputBox.vue";
import chatBox from "@/components/Programming_dev_1/chatBox.vue";
import axios from "axios";
import {useStateStore} from "@/stores/stateStore.ts";

const fullText = "What can I help with?"; // 完整标题内容
const displayedText = ref(""); // 当前展示的文字
const typingSpeed = 100; // 打字速度，单位：毫秒
const initialDelay = 3000; // 延迟时间：3秒
const isTypingStarted = ref(false); // 控制打字动画是否开始
const emit = defineEmits(['codeBoxAppear','uploadMessageToPage','getcode','getlang'])

//设置baseURL
const stateStore = useStateStore();
let baseURL='';
onBeforeMount(() => {
  if(stateStore.baseUrl=="0"){
    alert("Please set an IPv4 address")
  }
  // 正确的 baseURL 应该是你后端服务的地址
  // baseURL = "http://10.252.130.135:8000/ai/back";
  baseURL = stateStore.baseUrl+"/ai/back";
});

let userMessage = ref('')
let responseMessage = ref('')
let isComplete = ref(false);

let uploadMessage = ref("");

// 定义上传消息到 Ollama 的函数
const uploadMessageToOllama = async (message) => {
  uploadMessage.value = message;
  console.log("uploadMessage的值是:", uploadMessage.value);
  userMessage.value = uploadMessage.value;

// 查找 "and the code is this: " 的位置
  const delimiter = "and the code is this: ";

// 如果 userMessage 中存在 "and the code is this: "，就提取前面的部分
  if (userMessage.value.includes(delimiter)) {
    const extractedMessage = userMessage.value.split(delimiter)[0];  // 获取分隔符之前的部分
    userMessage.value = extractedMessage.trim();  // 去掉前后空格
    userMessage.value = "***[File] is uploaded***" + userMessage.value;
  }

  console.log("提取后的 userMessage:", userMessage.value);

  try {
    const requestData = {
      model: "gemma2:2b",
      prompt: "you are a programming assistant, please give the code and explanation: " + uploadMessage.value + "if there is a code, write the code again with explanation. if there is nothing, just write a helloworld program",
    };

    // 使用 fetch 来处理流式返回内容
    const response = await fetch(baseURL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    });
    userMessage.value = '';
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    // 处理流式响应
    const reader = response.body?.getReader();
    if (reader) {
      const decoder = new TextDecoder('utf-8');
      let done = false;
      let accumulatedResponse = ref('');
      let longestCode = ''; // 用来保存最长的代码块
      let selectedCode = ''; // 用来保存最终选择的代码块
      let languageDetected = false; // 标记是否检测到带有语言的代码块

      while (!done) {
        const { value, done: readerDone } = await reader.read();
        if (value) {
          const chunk = decoder.decode(value, { stream: true });

          // 处理流中多个 JSON 字符串
          const jsonChunks = chunk.split('\n').filter(line => line.trim() !== ''); // 过滤掉空行
          jsonChunks.forEach(jsonChunk => {
            try {
              const parsedChunk = JSON.parse(jsonChunk);
              if (parsedChunk.response) {
                accumulatedResponse.value += parsedChunk.response; // 拼接响应内容
                // 处理并提取代码块
                const { code, language } = extractCodeBlock(accumulatedResponse.value);

                if (code) {
                  // 如果检测到语言，优先选择这个代码块
                  if (language && !languageDetected) {
                    selectedCode = code; // 使用带有语言的代码块
                    languageDetected = true;
                    console.log(`选择的代码（带有语言）：${selectedCode}`);
                    console.log(`代码语言：${language}`);
                    emit('getcode', selectedCode);
                    emit('getlang', language);
                  } else {
                    // 如果没有语言，选择最长的代码块
                    if (code.length > longestCode.length) {
                      longestCode = code;
                      console.log(`选择的代码（最长的代码）：${longestCode}`);
                      emit('getcode', longestCode);
                    }
                  }
                }

                responseMessage.value = accumulatedResponse.value;
              }
            } catch (error) {
              console.error('Error parsing JSON chunk:', error);
            }
          });
        }
        done = readerDone;
        isComplete.value = done;
      }

      // 在流传输结束时，从 accumulatedResponse 中去掉选定的 code
      if (selectedCode) {
        responseMessage.value = accumulatedResponse.value.replace(selectedCode, '').trim();
      } else if (longestCode) {
        responseMessage.value = accumulatedResponse.value.replace(longestCode, '').trim();
      }
      // responseMessage.value = accumulatedResponse.value.replace("```", '').trim();
      console.log('所有内容已接收，最终的 responseMessage:', responseMessage.value);
    }
  } catch (error) {
    // 错误处理
    console.error('上传失败:', error);
    alert('上传失败，请稍后重试！');
  }
};



// 提取 Markdown 格式中的代码块及其语言
const extractCodeBlock = (text) => {
  const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;  // 匹配代码块的正则表达式，支持可选的语言标记
  let match;
  let extractedCode = '';
  let language = '';

  // 查找所有的代码块
  while ((match = codeBlockRegex.exec(text)) !== null) {
    language = match[1] || 'unknown';  // 如果没有指定语言，默认为 unknown
    extractedCode = match[2];  // 提取代码块内容
  }

  return { code: extractedCode, language };
};


let isShrink = ref(0);
console.log(isShrink.value) //页面初始化时的值
const firstUploadShrinkSpace = (message) => {
  if(message != 0){
    isShrink.value=1;
    console.log("InitialMode want to shrink his size!");  //此时监听到了第一次的上传
    sendToParent();
  }
}

const sendToParent = () => {
  console.log("sendToParent被触发")
  emit('codeBoxAppear',ref(1));
}

// 打字效果逻辑
const typeText = () => {
  let index = 0; // 当前字符的索引
  const interval = setInterval(() => {
    if (index < fullText.length) {
      displayedText.value += fullText[index]; // 每次增加一个字符
      index++;
    } else {
      clearInterval(interval); // 当文字全部展示完毕，停止定时器
    }
  }, typingSpeed);
};

// 在组件挂载时显示闪烁动画，延迟3秒后开始打字
onMounted(() => {
  setTimeout(() => {
    isTypingStarted.value = true; // 停止闪烁动画，显示打字动画
    typeText(); // 开始打字效果
  }, initialDelay);
});
</script>

<style scoped>
/* 全屏容器，使用 Flexbox 来居中内容 */
.container {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center;     /* 垂直居中 */
  height: 100vh;           /* 高度占满整个视口 */
}

/* 内容区域 */
.content {
  text-align: center;  /* 文字居中 */
  padding: 20px;
  transform: translateY(-50px); /* 向上移动50px */
}

/* 标题样式 */
h1 {
  font-size: 36px;
  color: #333;
  margin-bottom: 20px; /* 标题和输入框之间的间距 */
  white-space: nowrap; /* 防止自动换行 */
  overflow: hidden;    /* 隐藏超出的文字 */
}

/* 黑点闪烁动画 */
.dot {
  font-size: 60px;
  color: #333;
  animation: blink 2s infinite; /* 闪烁动画，每秒闪烁一次 */
}

@keyframes blink {
  0% {
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}
</style>