<template>
  <div class="floating-window" @contextmenu.prevent="onRightClick">
    <div class="drag-icon" @dblclick="toggleInput">
      <img :src="gifNow" alt="drag icon"/>
    </div>
    <!-- 当 showInput 为 true 时显示输入框 -->
    <div v-if="showInput" class="input-container">
      <input
          type="text"
          class="rounded-input"
          placeholder="Please enter..."
          v-model="inputText"
          @input="showDoubt"
          @keyup.enter="toggleEnter"/>
    </div>
    <div class="message-text markdown-body" v-html="renderedText(message)" v-if="showAnswer"></div>
  </div>
</template>

<script setup lang="ts">
import {ref, onBeforeMount} from 'vue';
import MarkdownIt from 'markdown-it';
import 'highlight.js/styles/github.css';
import {useStateStore} from '@/stores/stateStore';
import sleepingGif from '@/assets/lamb/sleeping.gif';
import successGif from '@/assets/lamb/success.gif';
import shakingGif from '@/assets/lamb/shaking.gif';
import doubtGif from '@/assets/lamb/doubt.gif';
import hljs from "highlight.js";

let baseURL = "" //共有url
let store = useStateStore()
let wi=ref<number>(0)
let he=ref<number>(0)


onBeforeMount(() => {
  baseURL = store.baseUrl; //先设置成默认url
});

let gifNow = ref(sleepingGif);

let gifType = ref({
  sleeping: sleepingGif,
  success: successGif,
  shaking: shakingGif,
  doubt: doubtGif,
});

const showInput = ref(false);
const showAnswer = ref(false)
const inputText = ref('');
const message = ref("");

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

const renderedText = (text:string) => {
  return md.render(text);
};

//激活输入框
const toggleInput = () => {
  showInput.value = !showInput.value;
};

//问号
const showDoubt = () => {
  gifNow.value = gifType.value.doubt;
}

//回车触发
const toggleEnter = () => {
  if(inputText.value===""){
    showAnswer.value=false;
    gifNow.value = gifType.value.doubt;
    return;
  }
  gifNow.value = gifType.value.shaking//接收到了前的动作
  fetchAnswer(inputText.value);
  inputText.value=""
}


//发送请求
const fetchAnswer = async (input:string) => {
  const timeout = 10000; // 设置超时时间（以毫秒为单位，例如10秒）
  const timeoutPromise = new Promise((_, reject) =>
      setTimeout(() => reject(new Error("请求超时")), timeout)
  );
  try {
    const response = await Promise.race([
      fetch(baseURL + "/ai/back", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          model: "gemma2:2b",
          prompt: input,
        }),
      }),
      timeoutPromise, // 如果 fetch 未完成，此 promise 将优先返回超时错误
    ]);
    if (!response.body) {
      throw new Error("流式返回没有body");
    }
    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let done = false;
    message.value = ""//清空上次的
    gifNow.value = gifType.value.success//接收到了后的动作
    showAnswer.value=true

    while (!done) {
      const {value, done: readerDone} = await reader.read();
      done = readerDone;

      if (value) {
        // 解码数据块并按行分割
        const chunk = decoder.decode(value, {stream: true});
        const lines = chunk.split("\n");

        // 逐行解析并处理
        lines.forEach((line) => {
          if (line.trim()) { // 忽略空行
            try {
              const parsedChunk = JSON.parse(line);
              message.value += parsedChunk.response; //data注入

            } catch (parseError) {
              console.warn("JSON解析失败，跳过该行: ", line);
            }
          }
        });
      }
    }

  } catch (error) {
    console.error('Error fetching dynamic recipe:', error);
    if (error.message === "请求超时") {
      ErrorPop("Timeout");
    } else {
      ErrorPop("404 Warning");
    }
  }
};

//右击触发
const onRightClick = (event) => {
  if (showInput.value) {
    showAnswer.value = false;
    showInput.value = false;
    gifNow.value=gifType.value.sleeping;
    changeSize(390,85);
  } else {
    showInput.value = true;
    changeSize(390,900);
    // showAnswer.value = true
    // console.log("触发", event);
  }
}

const ErrorPop=(text)=>{
  gifNow.value=gifType.value.doubt;
  message.value=text
}

//窗口大小
const changeSize=(width:number,height:number)=>{
  window.electronAPI.resizeFloatingWindow(width,height);
}

</script>

<style scoped>
.floating-window {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  border-radius: 20px;
  overflow: hidden;
  position: relative;
  cursor: grab;
  /*background-color: #4f5bd5;*/
  pointer-events: auto;
}

.drag-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  overflow: hidden;
  cursor: grab;
  display: flex;
  align-items: center;
  justify-content: center;
  /*background-color: #00cba9;*/
  -webkit-app-region: drag;
}

.drag-icon img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.input-container {
  margin-top: 0px;
  width: 100%;
  display: flex;
  justify-content: center;
}

.rounded-input {
  padding: 5px 10px;
  border: 1px solid #00cba9;
  border-radius: 50px;
  outline: none;
  font-size: 16px;
  height: 40px;
  min-width: 100px; /* 设置最小宽度 */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: width 0.2s ease-in-out;
}

.markdown-body {
  box-sizing: border-box;
  min-width: 50px;
  max-width: 500px;
  margin: 2px auto;
  padding: 15px;
  border-radius: 15px;
  max-height: 700px;
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
