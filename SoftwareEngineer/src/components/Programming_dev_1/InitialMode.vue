<template>
  <div class="container">
    <div class="content">
      <!-- 条件渲染：显示闪烁动画或打字文字 -->
      <h1 v-if="!isTypingStarted">
        <span class="dot">!</span>
      </h1>
      <h1 v-else>{{ displayedText }}</h1>
      <WholeInputBox />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import WholeInputBox from "@/components/Programming_dev_1/WholeInputBox.vue";

const fullText = "What can I help with?"; // 完整标题内容
const displayedText = ref(""); // 当前展示的文字
const typingSpeed = 100; // 打字速度，单位：毫秒
const initialDelay = 3000; // 延迟时间：3秒
const isTypingStarted = ref(false); // 控制打字动画是否开始

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
