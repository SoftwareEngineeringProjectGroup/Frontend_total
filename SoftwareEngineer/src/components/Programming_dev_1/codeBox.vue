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
  position: relative;
  background-color: #282c34; /* 深灰色背景 */
  color: #f8f8f2;
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
  font-family: 'Fira Code', monospace; /* 使用更现代的等宽字体 */
  font-size: 14px;
  line-height: 1.6;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3); /* 阴影效果提升立体感 */
  height: 100vh; /* 最大高度 80vh，防止代码块过高 */
}

/* 显示语言的头部 */
.header {
  font-size: 16px;
  font-weight: bold;
  color: #ffffff;
  background: #444c56;
  padding: 8px 16px;
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
  background-color: #3e444f; /* 行号背景色 */
  color: #999999; /* 行号颜色 */
  padding: 2px 10px;
  border-radius: 8px 0 0 8px;
  text-align: right;
  user-select: none;
  font-family: 'Fira Code', monospace;
}

.line-number {
  display: block;
  line-height: 1.6;
  font-size: 14px;
}

/* 代码块样式 */
.code-block {
  margin: 0;
  padding: 15px;
  background-color: #2c313c; /* 稍暗的背景色 */
  font-family: 'Fira Code', 'JetBrains Mono', Consolas, monospace; /* 使用专为编程设计的字体 */
  font-size: 16px; /* 增大字体大小，提升可读性 */
  white-space: pre-wrap;
  word-wrap: break-word;
  border-radius: 0 8px 8px 0;
  overflow-x: auto;
  line-height: 1.8; /* 增加行高，提高可读性 */
  color: #f8f8f2; /* 字体颜色 */
  width: 80vw; /* 改为宽度占屏幕 80% */
  letter-spacing: 0.5px; /* 增加字符间距，减少字符拥挤感 */
}


.button-group {
  position: fixed;
  bottom: 10px;
  right: 10px;
  display: flex;
  gap: 10px;
  z-index: 10;
  margin-right: 100px;
}

/* 按钮样式 */
.action-button {
  background-color: #5c6bc0; /* 淡紫蓝色 */
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  transition: background-color 0.3s ease;
}

.action-button:hover {
  background-color: #3f51b5; /* 更深的蓝色 */
}

/* 隐藏滚动条（Webkit 浏览器） */
.code-box::-webkit-scrollbar {
  display: none;
}

/* 隐藏滚动条（Firefox） */
.code-box {
  scrollbar-width: none;
}

</style>
