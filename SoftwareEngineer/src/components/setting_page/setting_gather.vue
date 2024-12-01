<template>
  <div class="back_color">
    <div class="left">
      <SideBar/>
    </div>
    <!--      主体-->
    <div class="content-container" :style="{ marginLeft: marginLeftValue + 'px' }">
      <SettingMain/>
    </div>

  </div>
</template>


<script setup lang="ts">
import SideBar from "@/components/SideBar.vue";
import SettingMain from "@/components/setting_page/setting_main.vue";
import {onBeforeMount, ref, watch} from "vue";
import {useStateStore} from "@/stores/stateStore.ts";

let marginLeftValue = ref(100)
// 获取 Pinia Store
const stateStore = useStateStore();
// 监听 stateStore.isOpenValue 的变化


onBeforeMount(() => {
  stateStore.isOpenValue ? marginLeftValue.value = 200 : marginLeftValue.value = 69;

  // console.log('Value from store:', state.value, isCollapse.value);
});
watch(() => stateStore.isOpenValue, (newValue) => {
  if (newValue === 0) {
    decreaseMargin();
  } else if (newValue === 1) {
    increaseMargin();
  }
});

// 渐渐减小 margin-left 的方法
const decreaseMargin = () => {
  let interval = setInterval(() => {
    if (marginLeftValue.value > 69) { // 最小的 margin-left 值
      marginLeftValue.value -= 10;
    } else {
      clearInterval(interval);
    }
  }, 20); // 每 30 毫秒调整10
};

// 渐渐增加 margin-left 的方法
const increaseMargin = () => {
  let interval = setInterval(() => {
    if (marginLeftValue.value < 200) { // 最大的 margin-left 值
      marginLeftValue.value += 20;
    } else {
      clearInterval(interval);
    }
  }, 20); // 每 30 毫秒调整10
};
</script>


<style scoped>
.left {
  position: fixed; /* 固定在页面左边 */
}

.content-container {
  margin-left: 120px; /* 使内容区域与侧边栏保持合适的距离 */

  box-sizing: border-box;
  flex: 1;
  overflow: hidden; /* 如果内容过多则可以滚动 */
}

.page-content {
  transition: filter 0.3s ease; /* 动画过渡，使反转更平滑 */
}

.back_color {
  width: 100vw; /* 视口宽度 */
  height: 100vh; /* 视口高度 */
  /*background: linear-gradient(135deg, #4f5bd5, #962fbf, #d62976, #f58529, #ffcc70);*/
  overflow: hidden; /* 防止滚动条 */
  margin: 0;
  background-size: 400% 400%; /* 放大背景尺寸 */
  /*animation: gradient-flow 7s ease infinite; 更快的动画速度 */
  background: linear-gradient(135deg, #ffb6c1, #ff8c00); /* 漂亮的渐变背景 */
}

@keyframes gradient-flow {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

</style>