<template>
  <div class="back">
    <!-- 首页 -->
    <transition name="slide">
      <div class="home-page" v-if="currentPage === 'home'">
        <!-- Lambda 文字 -->
        <div class="lambda-container">
          <h1 class="lambda-text" @click="goToPage('about')">Lambda</h1>
        </div>
      </div>
    </transition>

    <!-- 说明页 -->
    <transition name="slide">
      <div v-if="currentPage === 'about'" class="page-about">

        <h1 class="ins">Instruction</h1>

        <div class="demo-collapse">
          <el-collapse accordion>

            <!--            聊天模块-->
            <el-collapse-item name="1">
              <template #title class="small-title">
                <el-icon class="header-icon">
                  <ChatRound/>
                </el-icon>
                &nbsp;Chat Module
              </template>
              <div v-html="renderIt(chatInfo)" class="markdown-body">
              </div>


            </el-collapse-item>

            <!--            信息模块-->
            <el-collapse-item name="2">

              <template #title class="small-title">
                <el-icon class="header-icon">
                  <SwitchFilled/>
                </el-icon>
                &nbsp;Information Retrieval Module
              </template>

              <div v-html="renderIt(infoRetrieveInfo)" class="markdown-body">
              </div>
            </el-collapse-item>

            <!--            编程模块-->
            <el-collapse-item name="3">
              <template #title class="small-title">
                <el-icon class="header-icon">
                  <Monitor/>
                </el-icon>
                &nbsp;Programming Assistant Module
              </template>
              <div v-html="renderIt(codeAssistantInfo)" class="markdown-body">
              </div>
            </el-collapse-item>

            <!--            营养师模块-->
            <el-collapse-item name="4">
              <template #title class="small-title">
                <el-icon class="header-icon">
                  <DishDot/>
                </el-icon>
                &nbsp;Nutritionist Module
              </template>
              <div v-html="renderIt(dietitianInfo)" class="markdown-body">
              </div>

            </el-collapse-item>

            <!--            反馈模块-->
            <el-collapse-item name="5">
              <template #title class="small-title">
                <el-icon class="header-icon">
                  <ChatDotSquare/>
                </el-icon>
                &nbsp;Feedback
              </template>
              <div v-html="renderIt(feedbackInfo)" class="markdown-body">
              </div>
            </el-collapse-item>

            <!--            设置模块-->
            <el-collapse-item name="6">
              <template #title class="small-title">
                <el-icon class="header-icon">
                  <Setting/>
                </el-icon>
                &nbsp;Setting
              </template>
              <div v-html="renderIt(settingInfo)" class="markdown-body">
              </div>

            </el-collapse-item>


          </el-collapse>
        </div>


        <el-button type="info" @click="goToPage('home')" plain size="large" class="fixed-button">Back</el-button>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import {ref} from "vue";
import {
  ChatRound,
  Setting,
  SwitchFilled,
  ChatDotSquare,
  Monitor,
  DishDot,
} from '@element-plus/icons-vue'
import MarkdownIt from "markdown-it";
import 'highlight.js/styles/github.css'; // 确保引入样式文件-->

const currentPage = ref('home'); // 定义当前页面
const md = new MarkdownIt()

// 页面切换函数
const goToPage = (page: string) => {
  currentPage.value = page;
};

//渲染
const renderIt=(a:string)=>{
  return md.render(a)
}

//介绍信息
const chatInfo = ref("## Text Input\n" +
    "\n" +
    "- **Typing:** You can easily type your message directly into the **text box** at the bottom of the page.\n" +
    "- **Voice Input:** If you prefer, you can use the **blue microphone button** on the right side of the input box. Just click it, and your voice will be converted into text in the input box.\n" +
    "\n" +
    "## Input Box Features\n" +
    "\n" +
    "- **Moving the Input Box:** Want to move the input box around? Just drag the **icon** on the left side to reposition it wherever you like.\n" +
    "- **Sending Messages:**\n" +
    "  - Simply press **Enter** on your keyboard, or\n" +
    "  - Click the **green send button** to send your message.\n" +
    "\n" +
    "## Responses from Local Models\n" +
    "\n" +
    "- **Chat Messages:** When the local model responds, its replies will appear as chat messages right on the page.\n" +
    "- **Audio Playback:** Each response will have a **play button** at the bottom-right corner. Click it to hear the message aloud.\n" +
    "  - You can even change the **voice** of the playback by clicking the **gray button** next to the play button.\n" +
    "\n" +
    "## Deleting Messages\n" +
    "\n" +
    "- **Double-Click to Delete:** If you want to remove a message, just **double-click** on the avatar of the message, and it will be deleted from the chat history.\n")
const infoRetrieveInfo = ref("## 1. Online vs Local Queries\n" +
    "\n" +
    "- **Select Query Type**: You can choose whether to perform an **online query** or a **local query** using the button on the **left side of the input box**.\n" +
    "  - **Online Query**: Retrieves information from the internet, but it may be slower compared to local queries.\n" +
    "  - **Local Query**: Processes the query using local resources, which is faster but may have a more limited scope of information.\n" +
    "\n" +
    "> **Note**: Online queries may take longer depending on your network speed, while local queries provide quicker responses with potentially less data.\n" +
    "\n" +
    "## 2. Image Information Extraction\n" +
    "\n" +
    "- **Image Upload/Analysis**: This page also supports **image information extraction and understanding**. You can upload or provide images, and the system will attempt to extract and interpret relevant details from the image.\n" +
    "\n" +
    "## 3. Managing Information Records\n" +
    "\n" +
    "- **Viewing and Deleting Records**: You can interact with the information records generated by the system:\n" +
    "  - **Click to View**: Click on a specific information record to view its details.\n" +
    "  - **Right-Click to Delete**: If you no longer need a record, simply **right-click** on it to delete it from the system.\n" +
    "\n" +
    "## 4. Floating Window for Quick Queries\n" +
    "\n" +
    "- **Accessing the Floating Window**: You can open an **additional floating window** by clicking the **gray button** on the right side of the input box.\n" +
    "  - In the floating window, you can enter requests to quickly search for information without interrupting your current session.\n" +
    "\n" +
    "> **Note**: The floating window provides a convenient way to perform quick searches or queries without leaving the current chat.\n")
const codeAssistantInfo = ref("## 1. Code Request and Generation\n" +
    "\n" +
    "- **User Input**: You can enter a **coding request** (like a coding problem or task description) into the input box.\n" +
    "- **Model Response**: The system will then generate the corresponding **code** and provide an explanation of how the code works.\n" +
    "  - The **explanation** will appear on the **left side** of the interface.\n" +
    "  - The **source code** will be displayed on the **right side**.\n" +
    "\n" +
    "## 2. Copying and Saving Code\n" +
    "\n" +
    "- **Copy Code**: You can easily copy the generated **code** to your clipboard by selecting the text and using the **copy** function.\n" +
    "- **Save Code**: Alternatively, you can **save the code** directly as a file on your computer.\n" +
    "\n" +
    "> **Note**: This feature makes it simple for you to work with the generated code—whether you want to copy it for immediate use or save it for future reference.\n" )
const dietitianInfo = ref("## 1. Input Health Information and Dietary Needs\n" +
    "\n" +
    "- **Personal Health Input**: Users can input their **personal health information** (e.g., age, weight, health goals) or specify their **dietary needs** (e.g., weight loss, muscle gain, vegetarian).\n" +
    "- **Generated Diet Plan**: Based on the input, the system will generate a **customized diet plan**, which includes:\n" +
    "  - A **diet table** detailing the meals and food items.\n" +
    "  - A **pie chart** visualizing the nutritional content of the foods in the diet plan.\n" +
    "\n" +
    "## 2. Food Recognition and Information Detection\n" +
    "\n" +
    "- **Upload or Capture Images**: Users can either **upload pictures** or use their device's camera to **take pictures** of the food they have on hand.\n" +
    "- **Food Detection**: The system will analyze the images to detect the types and nutritional information of the foods, providing relevant details about the food items.\n" +
    "\n" +
    "> **Note**: This feature helps users track and understand the nutritional content of the foods they are planning to eat, providing an easy way to ensure they align with their diet plan.\n")
const feedbackInfo = ref("## 1. Providing Feedback\n" +
    "\n" +
    "- **Input Box**: On the **feedback page**, you can type any **feedback**, suggestions, or comments that you would like to share.\n" +
    "- **Submit Feedback**: Once you’ve entered your feedback, simply **send** it by clicking the **send button**.\n" +
    "\n" +
    "## 2. What You Can Provide\n" +
    "\n" +
    "- **Suggestions**: Let us know if you have ideas on how we can improve the service.\n" +
    "- **Comments**: Share your experience, thoughts, or any issues you may have encountered.\n" +
    "- **General Feedback**: Any general comments are always appreciated to help us better serve you.\n" +
    "\n" +
    "> **Note**: Your feedback is important to us and helps improve the overall experience.\n")
const settingInfo = ref("## 1. Set Your User Profile\n" +
    "\n" +
    "- **Profile Picture**: You can upload and set your **user profile picture** to personalize your account.\n" +
    "- **Gender**: Set your **gender** preference in the profile settings.\n" +
    "- **Personal Prompt**: Enter a **personal prompt** that will be used to customize your interactions. This can include a short description or any details you'd like the system to know about you.\n" +
    "\n" +
    "## 2. Extension Port for Advanced Models\n" +
    "\n" +
    "- **Access Powerful Models**: This page also features an **extension port** that will allow you to connect to **more powerful models** in the future. As these models become available, you will be able to access enhanced features and capabilities to improve your experience.\n" +
    "\n" +
    "> **Note**: The personal prompt helps tailor your interactions with the system, and the extension port ensures that your account can grow with new capabilities as they are introduced.\n" )
</script>

<style scoped>
.back {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

/* 页面样式 */
.home-page, .page {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

/* Lambda样式 */
.lambda-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  cursor: pointer; /* 添加点击手势 */
}

.lambda-text {
  font-size: 4rem;
  font-weight: bold;
  font-family: 'Arial', sans-serif;
  background: linear-gradient(90deg, #ff6b6b, #fddb92, #4dabf7, #a29bfe);
  background-size: 400%;
  -webkit-background-clip: text;
  color: transparent;
  text-shadow: 0px 0px 15px rgba(255, 255, 255, 0.8), 0px 0px 30px rgba(255, 255, 255, 0.6), 0px 0px 45px rgba(255, 255, 255, 0.4);
  animation: glow 5s ease-in-out infinite alternate, moveGlow 15s linear infinite;
}

/* 光晕闪动动画 */
@keyframes glow {
  from {
    text-shadow: 0px 0px 15px rgba(255, 255, 255, 0.6), 0px 0px 30px rgba(255, 255, 255, 0.4), 0px 0px 45px rgba(255, 255, 255, 0.3);
  }
  to {
    text-shadow: 0px 0px 30px rgba(255, 255, 255, 1), 0px 0px 45px rgba(255, 255, 255, 0.8), 0px 0px 60px rgba(255, 255, 255, 0.6);
  }
}

/* 背景位置动画实现光流动效果 */
@keyframes moveGlow {
  0% {
    background-position: 0%;
  }
  100% {
    background-position: 400%;
  }
}

/* 滑动动画效果 */
.slide-enter-active, .slide-leave-active {
  transition: transform 0.5s ease;
}

.slide-enter-from {
  transform: translateX(100%);
}

.slide-leave-to {
  transform: translateX(-100%);
}

/*说明书效果*/
.demo-collapse {
  border-radius: 12px; /* 圆角 */
  background-color: #ffffff;
  padding: 10px; /* 组件内边距 */
  color: white; /* 字体颜色 */
  margin: 20px auto; /* 上下边距 */
  margin-top: 5vh; /* 设置距离页面顶部10vh的位置 */
  width: 95%; /* 设置宽度为90%，居中显示 */
}


.small-title {
  text-align: center; /* 标题居中 */
  color: white; /* 标题字体颜色 */
  font-weight: bold; /* 加粗标题 */
}

.fixed-button {
  position: fixed; /* 固定位置 */
  bottom: 20px; /* 距离屏幕底部的距离 */
  right: 20px; /* 距离屏幕右侧的距离 */
  z-index: 1000; /* 使按钮在其他内容之上 */
}

.ins {
  text-align: center; /* 标题居中 */
  color: white; /* 标题字体颜色 */
  font-weight: bold; /* 加粗标题 */
  margin-top: 30px;
}
.markdown-body {
  box-sizing: border-box;
  min-width: 200px;
  max-width: 980px;
  margin: 0 auto;
  padding: 15px;
  max-height: 550px;
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
