<template>
  <div class="back_color">
    <div class="left">
      <Left/>
    </div>
    <div class="content-container" :style="{ marginLeft: marginLeftValue + 'px' }">
      <page/>
    </div>
  </div>
</template>

<script setup lang="ts">
import {onBeforeMount, ref, watch} from 'vue'
import Left from "../components/SideBar.vue";
import page from "../components/Programming_dev_1/pageWithoutSidebar.vue";
import {useStateStore} from "@/stores/stateStore.ts";

let marginLeftValue = ref(85)
// 获取 Pinia Store
const stateStore = useStateStore();
// 监听 stateStore.isOpenValue 的变化


onBeforeMount(() => {
  stateStore.isOpenValue ? marginLeftValue.value = 200 : marginLeftValue.value = 64;

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
    if (marginLeftValue.value > 64) { // 最小的 margin-left 值
      marginLeftValue.value -= 10;
    } else {
      marginLeftValue.value = 64;
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
      marginLeftValue.value = 200;
      clearInterval(interval);
    }
  }, 20); // 每 30 毫秒调整10
};
</script>

<style scoped>
.left {
  position: fixed; /* 固定在页面左边 */
  /* 不需要应用 fade 动画 */
}

@keyframes fade {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
@keyframes gradient-flow {
  0% {
    background-position: 0% 50%;
  }
  100% {
    background-position: 100% 50%;
  }
}

/* 只在 .back_color 上应用动画 */
.content-container {
  height: 100vh;
  background: linear-gradient(90deg, #c0ffc0, #ffffb9, #ffb0b0, #ffb0b0, #c2c6ff);
  background-size: 400% 400%;
  animation: fade 3s, gradient-flow 7s 5s ease forwards;
}
</style>
