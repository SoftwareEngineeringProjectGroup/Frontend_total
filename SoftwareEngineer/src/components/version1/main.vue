<template>
  <!--  对话页面-->
  <div class="chat-page" ref="chatContainer">
    <!--    对话框-->
    <div
        v-for="(message, index) in messages"
        :key="index"
        class="message-item"
        :class="message.isUser ? 'user-message' : 'ai-message'"
    >

      <div class="avatar">
        <img v-if="message.isUser" :src=userAvatar alt="Image"/>
        <img v-else :src=aiAvatar alt="Image">

      </div>


      <div class="message-content" v-loading="message.loading" element-loading-background="rgba(255, 255, 255, 1)">
        <!--      确定是否加载-->
        <div >
          <div v-if="!message.isUser" class="message-text markdown-body" v-html="renderedText(message.text)"></div>
          <div v-else class="message-text">{{ message.text }}</div>
        </div>
        <div class="message-time">{{ message.time }}</div>

      </div>

    </div>
  </div>

</template>

<script setup>
import {ref, nextTick, computed, onBeforeMount} from 'vue';
import MarkdownIt from 'markdown-it'; //渲染markdown
import hljs from 'highlight.js'; // 引入代码高亮库
import 'github-markdown-css';
import {useStateStore} from "@/stores/stateStore.ts"; //状态获取
import 'highlight.js/styles/github.css'; // 确保引入样式文件

// 使用 ref 定义响应式变量
const userAvatar = ref("/static/userDefault.jpg");  // 用户头像
const aiAvatar = ref("/static");      // AI 头像
const messages = ref([
  {text: '你是？', isUser: true, time: '2024/10/11 16:39:40', loading: false},
  {text: '##  👋 你好！这是你的本地 AI 助手。\n' +
        '\n' +
        '**你正在体验一个本地 AI 聊天机器人，它不受网络限制，随时随地和你交流。**\n' +
        '\n' +
        '**无需担心网络连接，无需使用互联网。** 只要输入你的想法或问题，它都能尽力帮助你。', isUser: false, time: '2024/10/11 16:39:41', loading: false},
]);
//loading用来记录是否正在加载

let newMessage = ref(''); //发送的数据
const chatContainer = ref(null); //聊天框对象
// 获取 Pinia Store
const stateStore = useStateStore();


// 初始化 MarkdownIt 实例，并启用代码高亮功能
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


// 发送用户消息
const sendMessage = async () => {
  if (newMessage.value.trim() !== '') {
    // 用户信息推入
    messages.value.push({
      text: newMessage.value,
      isUser: true,
      time: new Date().toLocaleString(),
      loading: false
    });
    await nextTick();
    scrollToBottom();
    await sendAIMessage(); //  AI 回复
  }
};

// AI 回复
const sendAIMessage = async () => {
  setTimeout(async () => {
    // ai信息推入
    messages.value.push({
      text: '',
      isUser: false,
      time: new Date().toLocaleString(),
      loading: true
    });
    scrollToBottom();
    await getAnswer();
    await nextTick();

  }, 500);
};
const getAnswer = async () => {
  // console.log("已发送", newMessage.value);
  try {
    // 向本地服务器发送 POST 请求，获取生成的数据
    const response = await fetch("http://localhost:11434/api/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "gemma2:2b",
        prompt: newMessage.value,
      }),
    });


    // 检查响应是否包含 body
    if (!response.body) {
      throw new Error("ReadableStream not supported in this environment.");
    }

    // 获取响应的流式读取器
    //response.body 是一个流式的接口，通过 getReader() 来逐步读取到服务器返回的数据。在流结束之前，数据是分段到达的，并不是一次性获取到完整的响应
    //reader类似于一个生成器
    const reader = response.body.getReader();

    //创造解码器对象
    const decoder = new TextDecoder("utf-8");
    let done = false;

    let incompleteChunk = ""; // 用于存储未完整解析的数据块

    messages.value[messages.value.length - 1].loading = false; //读取到解除加载
    // 循环读取响应数据，直到读取完成
    while (!done) {
      const {value, done: readerDone} = await reader.read();
      done = readerDone;

      if (value) {
        // 将数据块解码为字符串
        const chunk = decoder.decode(value, {stream: true});
        //存储字符串
        incompleteChunk += chunk;


        try {
          //解析字符串生成的是单个返回的JSON对象
          const parsedChunk = JSON.parse(incompleteChunk);

          // 将解析后的内容追加到 messages 中
          messages.value[messages.value.length - 1].text += parsedChunk.response;

          scrollToBottom();//滚动
          // 重置未解析的部分
          incompleteChunk = "";
        } catch (parseError) {
          console.error("JSON解析失败: ", parseError);
        }
      }
    }

    console.log(messages.value[messages.value.length - 1].text)
    console.log("流结束"); // 打印流结束的消息
  } catch (error) {
    console.error("错误: ", error); // 打印错误信息
  }
};


//返回markdown
const renderedText = (text) => {
  return md.render(text);
};


// 滚动到底部
const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
  }
};

//头像载入
onBeforeMount(() => {
  aiAvatar.value = stateStore.aiImagePath;
  userAvatar.value = stateStore.userImagePath;

  // console.log('Value from store:', state.value, isCollapse.value);
});

// 一再接受inputValue
import {defineProps, watch} from 'vue';


// 接收来自父组件的 props
const props = defineProps({
  receivedInput: String
});

// 监听 props 的变化
watch(() => props.receivedInput, (newValue) => {
  if (newValue) {
    handleReceivedInput(newValue);
  }
});

// 处理收到的数据
const handleReceivedInput = (inputValue) => {
  // console.log('子组件main处理收到的数据:', inputValue);
  newMessage.value = inputValue;
  sendMessage();
};
</script>

<style scoped>
.chat-page {
  display: flex;
  flex-direction: column;
  padding: 0px;
  height: 92vh;
  overflow-y: auto;
  flex-grow: 1;
  scroll-behavior: smooth;
}

.message-item {
  display: flex;
  align-items: flex-end;
  margin-bottom: 10px;
}

.user-message {
  flex-direction: row-reverse;
  text-align: left;
}

.ai-message {
  flex-direction: row;
}

.avatar {
  width: 40px;
  height: 40px;
  margin: 0 10px;
}

.avatar img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
}

.message-content {
  max-width: 60%;
  background-color: #ffffff;
  border-radius: 10px;
  padding: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', 'Helvetica', sans-serif; /* 设置字体 */
  font-size: 16px; /* 字体大小 */
  line-height: 1.0; /* 行间距，使内容更易读 */
  color: #333; /* 字体颜色 */
}

.user-message .message-content {
  background-color: #d1e7dd;
}

.ai-message .message-content {
  font-size: 100px; /* AI 回复字体大小 */
}

.message-time {
  font-size: 12px;
  color: #888;
  margin-top: 5px;
}

.markdown-body {
  box-sizing: border-box;
  min-width: 200px;
  max-width: 980px;
  margin: 0 auto;
  padding: 15px;
}

@media (max-width: 767px) {
  .markdown-body {
    padding: 15px;
  }
}


</style>