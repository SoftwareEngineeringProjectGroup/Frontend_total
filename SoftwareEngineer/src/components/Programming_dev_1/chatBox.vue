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
            <img src="@/assets/aiDefault.jpg" alt="System Avatar" />
          </div>
        </template>

        <!-- 显示消息内容 -->
        <span
            class="message-text markdown-body"
            v-html="message.isMarkdown ? renderMarkdown(message.text) : message.text"
        ></span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, defineProps, watch, onMounted, onBeforeUnmount } from 'vue';
import 'highlight.js/styles/github.css';
import hljs from "highlight.js";
import MarkdownIt from "markdown-it";

const props = defineProps({
  message: String, // 用户消息
  msg: String,     // 流式返回的消息内容
  isComplete: Boolean, // 是否已完成返回
  finalmessage: String, // 最终消息
});

// 用于存储当前正在拼接的流式返回的内容
let currentResponse = ref('');
let currentExplanation = ref('');
let isFirstMsg = ref(true); // 临时变量，用来判断是否是第一次流式返回

// 消息列表，初始有一条欢迎消息
const messages = ref([
  { text: '#### Welcome ! ! !\nI\'m your personal **AI Programming Assistant**, what can I do for you?', isUser: false, isMarkdown: true },
]);

// 动态添加信息的函数
// 动态添加信息的函数
const addMessage = (text: any, isUser = false, isMarkdown = false) => {
  if (typeof text !== 'string') {
    console.error("Invalid message content:", text);
    return; // 如果消息内容无效，则不添加
  }
  messages.value.push({ text, isUser, isMarkdown });
};

// 删除上一条消息并替换
const updateMessage = (newText: any) => {
  if (typeof newText !== 'string') {
    console.error("Invalid message content:", newText);
    return; // 如果新的消息内容无效，则不进行替换
  }

  const lastMessage = messages.value[messages.value.length - 1];
  if (!lastMessage.isUser) {
    messages.value.splice(messages.value.length - 1, 1); // 只有在最后一条是系统消息时才删除
  }
  addMessage(newText, false, true);
};


// 监听父组件传递的 message 属性变化
watch(
    () => props.message,
    (newMessage) => {
      if (newMessage) {
        addMessage(newMessage, true, true); // 用户消息
      }
    },
    { immediate: true }
);

// 监听 msg 属性变化并将其合并
watch(
    () => props.msg,
    (newMsg) => {
      if (newMsg && typeof newMsg === 'string') {
        // 只有当 newMsg 是有效的字符串时才处理
        currentResponse.value += newMsg;
        console.log("currentResponse.value: " + currentResponse.value);

        if (isFirstMsg.value) {
          // 如果是第一次更新，直接添加流式消息
          addMessage(newMsg, false, true);
          isFirstMsg.value = false;
        } else {
          // 不是第一次，删除上一条并更新
          updateMessage(currentResponse.value);
        }

        // 判断流数据是否包含换行符等，判断是否可以拼接完整
        if (newMsg.includes('\n')) {
          if (currentResponse.value.trim().startsWith('```')) {
            updateMessage(currentResponse.value);
          } else {
            currentExplanation.value += newMsg;
          }
          currentResponse.value = ''; // 清空当前流响应，准备下一次拼接
        }

        if (props.isComplete) {
          // 如果已经完成流式数据，更新最终消息
          if (currentExplanation.value) {
            updateMessage(props.finalmessage);
            currentExplanation.value = ''; // 清空当前解释内容
          }
          isFirstMsg.value = true; // 重置状态
        }
      } else {
        console.warn("Received invalid msg data:", newMsg);
      }
    },
    { immediate: true }
);


// 渲染 Markdown 内容
const md = new MarkdownIt({
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return `<pre class="hljs"><code>${hljs.highlight(str, {language: lang}).value}</code></pre>`;
      } catch (__) {
      }
    }
    return `<pre class="hljs"><code>${md.utils.escapeHtml(str)}</code></pre>`;
  },
});

const renderMarkdown = (text: any) => {
  // 确保传入的参数是字符串
  if (typeof text !== 'string') {
    console.error("Invalid input for Markdown rendering:", text);
    return '';  // 返回空字符串，防止渲染错误
  }
  return md.render(text);
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

// 使用 MutationObserver 监听 message-box 内容变化，确保自动滚动到底部
let observer;
onMounted(() => {
  const messageBox = document.querySelector('.message-box');

  if (messageBox) {
    observer = new MutationObserver(() => {
      scrollToBottom(); // 每当 DOM 更新时滚动到底部
    });

    // 配置 MutationObserver 监听子节点变化
    observer.observe(messageBox, {
      childList: true,
      subtree: true,
    });
  }
});

onBeforeUnmount(() => {
  // 销毁 MutationObserver
  if (observer) {
    observer.disconnect();
  }
});

// 初始滚动到底部
scrollToBottom();
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 40vw;

  border-radius: 8px;
  overflow: hidden;
  background-color: #f9f9f9;
  padding: 10px;
  box-sizing: border-box;
}

/* 消息显示区域 */
.message-box {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  padding-bottom: 200px; /* 保证底部有至少 200px 的空白 */
  display: flex;
  flex-direction: column;
  gap: 10px;
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
  max-width: 95%; /* 限制消息宽度 */
}

/* 用户消息样式 */
.user-message {
  background-color: #f0f0f0;
  align-self: flex-end; /* 右对齐 */
  text-align: right;
  max-width: 80%; /* 限制消息宽度 */
  padding: 0px;
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

/* 打字效果 */
.message-text {
  display: inline-block;
  word-wrap: break-word;
}


.markdown-body {
  box-sizing: border-box;
  min-width: 50px;
  max-width: 500px;
  margin: 2px auto;
  padding: 15px;
  border-radius: 15px;
  font-size: 16px;
  overflow: auto;
}

@media (max-width: 767px) {
  .markdown-body {
    padding: 15px;
  }
}

/* 隐藏滚动条（Webkit 浏览器） */
.markdown-body::-webkit-scrollbar {
  display: none;
}

/* 隐藏滚动条（Firefox） */
.markdown-body {
  scrollbar-width: none; /* Firefox */
}
</style>
