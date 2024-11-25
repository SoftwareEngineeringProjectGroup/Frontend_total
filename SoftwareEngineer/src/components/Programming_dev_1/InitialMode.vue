<template>
  <div class="container"
       :style="{
      width: isShrink !== 0 ? '800px' : '100%',
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
      <chatBox />
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
      <WholeInputBox @firstUpload="firstUploadShrinkSpace"/>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, defineEmits } from 'vue';
import WholeInputBox from "@/components/Programming_dev_1/WholeInputBox.vue";
import chatBox from "@/components/Programming_dev_1/chatBox.vue";

const fullText = "What can I help with?"; // 完整标题内容
const displayedText = ref(""); // 当前展示的文字
const typingSpeed = 100; // 打字速度，单位：毫秒
const initialDelay = 3000; // 延迟时间：3秒
const isTypingStarted = ref(false); // 控制打字动画是否开始
const emit = defineEmits(['codeBoxAppear'])

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
