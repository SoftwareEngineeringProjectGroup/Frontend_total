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
      <div v-if="currentPage === 'about'" class="page about">

        <h1 class="ins">Instruction</h1>

        <div class="demo-collapse">
          <el-collapse accordion>

            <!--            聊天模块-->
            <el-collapse-item name="1" class="small-title">
              <template #title class="small-title">
                <el-icon class="header-icon">
                  <ChatRound/>
                </el-icon>
                Chat Module
              </template>

              <div>
                This page facilitates chat interactions between users and local models, allowing users to input text directly or use the blue microphone button on the right side of the input box for voice input, which converts to text in the input box. The input box can be moved by dragging the icon on its left side, and users can send messages by pressing Enter or clicking the green send button. Responses from the local model are displayed as chat messages on the page, each with a play button in the bottom-right corner to play the message aloud; users can switch playback voices using the gray button. Double-clicking a message's avatar twice will delete that message.
              </div>


            </el-collapse-item>

            <!--            信息模块-->
            <el-collapse-item name="2">

              <template #title class="small-title">
                <el-icon class="header-icon">
                  <SwitchFilled/>
                </el-icon>
                Information Retrieval Module
              </template>

              <div>
                Visual feedback: reflect current state by updating or rearranging
                elements of the page.
              </div>
            </el-collapse-item>

            <!--            编程模块-->
            <el-collapse-item name="3">
              <template #title class="small-title">
                <el-icon class="header-icon">
                  <Monitor/>
                </el-icon>
                Programming Assistant Module
              </template>
              <div>
                Easy to identify: the interface should be straightforward, which helps
                the users to identify and frees them from memorizing and recalling.
              </div>
            </el-collapse-item>

            <!--            营养师模块-->
            <el-collapse-item name="4">
              <template #title class="small-title">
                <el-icon class="header-icon">
                  <DishDot/>
                </el-icon>
                Nutritionist Module
              </template>
              <div>
                Decision making: giving advices about operations is acceptable, but do
                not make decisions for the users;
              </div>

            </el-collapse-item>

            <!--            反馈模块-->
            <el-collapse-item name="5">
              <template #title class="small-title">
                <el-icon class="header-icon">
                  <ChatDotSquare/>
                </el-icon>
                Feedback
              </template>
              <div>
                Decision making: giving advices about operations is acceptable, but do
                not make decisions for the users;
              </div>
            </el-collapse-item>

            <!--            设置模块-->
            <el-collapse-item name="6">
              <template #title class="small-title">
                <el-icon class="header-icon">
                  <Setting/>
                </el-icon>
                Setting
              </template>
              <div>
                Decision making: giving advices about operations is acceptable, but do
                not make decisions for the users;
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

const currentPage = ref('home'); // 定义当前页面

// 页面切换函数
const goToPage = (page: string) => {
  currentPage.value = page;
};
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
  animation: glow 3s ease-in-out infinite alternate, moveGlow 3s linear infinite;
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


</style>
