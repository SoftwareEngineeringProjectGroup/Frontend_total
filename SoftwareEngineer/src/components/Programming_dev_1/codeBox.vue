<template>
  <div class="code-box">
    <!-- 显示当前编程语言 -->
    <div class="header">
      {{ props.language.toUpperCase() }}
    </div>

    <!-- 代码块与行号 -->
    <div class="code-with-lines">
      <!-- 行号部分 -->
      <div class="line-numbers">
        <span
            v-for="line in totalLines"
            :key="line"
            class="line-number"
        >{{ line }}</span>
      </div>
      <!-- 高亮代码块 -->
      <pre class="code-block">
        <code v-html="highlightedCode"></code>
      </pre>
    </div>

    <!-- 右下角按钮区域 -->
    <div class="button-group">
      <button class="action-button copy-button" @click="copyCode">
        Copy
      </button>
      <button class="action-button download-button" @click="downloadCode">
        Download
      </button>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, watch, defineProps } from 'vue';
import hljs from 'highlight.js'; // 引入 highlight.js
import 'highlight.js/styles/monokai.css'; // 更清晰的 Monokai 样式

// 高亮后的 HTML 内容
const highlightedCode = ref('');
const totalLines = ref<number[]>([]); // 存储行号数组

// 定义 Props
const props = defineProps({
  code: {
    type: String,
    required: true, // 必须传递代码内容
  },
  language: {
    type: String,
    default: 'javascript', // 默认代码语言为 JavaScript
  },
});

// 更新行号和高亮代码
const updateCode = (newCode: string) => {
  if (newCode && props.language) {
    try {
      highlightedCode.value = hljs.highlight(newCode, { language: props.language }).value;
      totalLines.value = Array.from({ length: newCode.split('\n').length }, (_, i) => i + 1);
    } catch (error) {
      console.error('Highlight.js Error:', error);
      highlightedCode.value = newCode; // 如果高亮失败，显示原始代码
      totalLines.value = Array.from({ length: newCode.split('\n').length }, (_, i) => i + 1);
    }
  }
};

// 监听 code 属性变化并更新高亮和行号
watch(() => props.code, updateCode, { immediate: true },);

// 复制代码的功能
const copyCode = () => {
  navigator.clipboard.writeText(props.code).then(() => {
    alert('Code copied to clipboard!');
  });
};

// 下载代码的功能
const downloadCode = () => {
  const blob = new Blob([props.code], { type: 'text/plain' }); // 创建文件 Blob
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob); // 创建 Blob URL
  if (props.language == 'python'){
    link.download = `code.py`; // 设置文件名，后缀为语言名
  }
  else {
    link.download = `code.${props.language}`; // 设置文件名，后缀为语言名
  }
  link.click();
};
</script>

<style scoped>
/* 主容器样式 */
.code-box {
  position: relative; /* 使按钮组定位相对于该容器 */
  background-color: #2d2d2d; /* 深色背景 */
  color: #f8f8f2; /* 字体颜色 */
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto; /* 支持水平滚动 */
  font-family: 'Courier New', Courier, monospace; /* 等宽字体 */
  font-size: 14px;
  line-height: 1.5;
  height: 100vh;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2); /* 添加阴影 */
}

/* 显示语言的头部 */
.header {
  font-size: 16px;
  font-weight: bold;
  color: #ffffff;
  background: #444444;
  padding: 8px;
  border-radius: 4px;
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 1;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* 行号和代码块的容器 */
.code-with-lines {
  display: flex;
  margin-top: 40px;
}

/* 行号部分 */
.line-numbers {
  background-color: #333333; /* 行号背景 */
  color: #888888; /* 行号颜色 */
  padding: 2px 12px;
  border-radius: 8px 0 0 8px;
  text-align: right;
  user-select: none; /* 禁止选中行号 */
}

.line-number {
  display: block;
  line-height: 1.5;
  font-size: 14px;
}

/* 代码块样式 */
.code-block {
  margin: 0;
  padding: 0px 10px;
  background: transparent;
  font-size: 14px;
  white-space: pre-wrap;
  overflow-x: auto;
  border-radius: 0 8px 8px 0;
}

/* 按钮组样式 */
.button-group {
  position: absolute; /* 按钮组定位在父容器内部 */
  bottom: 10px;      /* 距离容器底部 10px */
  right: 10px;       /* 距离容器右侧 10px */
  display: flex;
  gap: 8px;          /* 按钮间距 */
  z-index: 10;       /* 确保按钮在其他内容之上 */
}

/* 按钮样式 */
.action-button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.action-button:hover {
  background-color: #0056b3;
}
</style>
