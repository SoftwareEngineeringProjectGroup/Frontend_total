<template>
  <div class="chat-container">
    <!-- 消息显示区域 -->
    <div class="message-box" ref="messageBox">
      <div
          v-for="(message, index) in messages"
          :key="index"
          :class="['message', message.isUser ? 'user-message' : 'system-message']"
      >
        <!-- 系统消息头像 -->
        <template v-if="!message.isUser">
          <div class="avatar">
            <img src="https://via.placeholder.com/40" alt="System Avatar" />
          </div>
        </template>
        <span
            class="message-text"
            v-html="message.isMarkdown ? renderMarkdown(message.text) : message.text"
        ></span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue';
import { marked } from 'marked';

// 消息列表
const messages = ref([
  { text: '#### Welcome\nThis is **Markdown** content!', isUser: false, isMarkdown: true },
  { text: 'Write a mergesort in Python.', isUser: true, isMarkdown: false },
  { text: 'Here’s a Python implementation of the **mergesort** algorithm:   \n***As shown on the right*** ', isUser: false, isMarkdown: true },
]);

// 渲染 Markdown 内容
const renderMarkdown = (text: string) => {
  return marked(text);
};

// 滚动到最新消息
const scrollToBottom = () => {
  nextTick(() => {
    const messageBox = document.querySelector('.message-box');
    if (messageBox) {
      messageBox.scrollTop = messageBox.scrollHeight;
    }
  });
};

// 滚动到底部（初始化调用）
scrollToBottom();
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 700px;
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
  background-color: #f9f9f9;
}

/* 消息显示区域 */
.message-box {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  display: flex;
  flex-direction: column;
}

/* 单条消息 */
.message {
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 12px;
  max-width: 85%;
  display: flex;
  align-items: flex-start; /* 确保内容与头像对齐 */
  gap: 10px; /* 与头像的间距 */
}

/* 系统消息样式 */
.system-message {
  background-color: #f9f9f9;
  align-self: flex-start; /* 左对齐 */
  text-align: left;
}

/* 系统消息头像 */
.avatar {
  width: 20.8px;
  height: 20.8px;
  border-radius: 50%; /* 圆形头像 */
  overflow: hidden; /* 确保图片不会超出圆形范围 */
  flex-shrink: 0; /* 防止头像缩放 */
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 保持图片比例 */
}

/* 用户消息样式 */
.user-message {
  background-color: #f0f0f0;
  align-self: flex-end; /* 右对齐 */
  text-align: right;
}

</style>
