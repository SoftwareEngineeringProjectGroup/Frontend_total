

<!--<template>-->

<!--  <SideBar/>-->
<!--  <div class="centered-div">-->
<!--    <el-input v-model="baseUrl" style="width: 240px" placeholder="Input iPv4 Address" size="large" @keydown.enter="setUrl"/>-->

<!--    <el-button type="primary" round @click="setUrl" class="b" size="large">Set Address</el-button>-->
<!--  </div>-->

<!--</template>-->

<!--<script setup>-->
<!--import SideBar from "@/components/SideBar.vue";-->
<!--import { ref } from 'vue'-->
<!--const baseUrl = ref('')-->
<!--import {useStateStore} from "@/stores/stateStore";-->
<!--let stateStore=useStateStore()-->
<!--const setUrl=()=>{-->
<!--  stateStore.setbaseUrl(baseUrl.value);-->
<!--  console.log("设定为",baseUrl.value);-->
<!--  baseUrl.value='';-->
<!--}-->

<!--</script>-->


<!--<style scoped>-->
<!--.centered-div {-->
<!--  position: absolute;-->
<!--  top: 40%;-->
<!--  left: 40%;-->
<!--}-->

<!--.b{-->
<!--  margin-left: 10px;-->
<!--}-->
<!--</style>-->

<template>
  <div class="message-text markdown-body" v-html="renderedText(message)"></div>
</template>
<script setup>
import {ref} from "vue";
import MarkdownIt from "markdown-it";
import 'highlight.js/styles/github.css'; // 确保引入样式文件
let message=ref('##  👋 Hi! This is your local AI assistant.\n' +
    '\n' +
    '**You are experiencing a local AI chatbot that is not restricted by the network and can communicate with you anytime, anywhere.**\n' +
    '\n' +
    '**No need to worry about the network connection, no need to use the Internet** As long as you input your ideas or questions, I will do my best to help you.')


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

const renderedText = (text) => {
  return md.render(text);
};
</script>

<style scoped>
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