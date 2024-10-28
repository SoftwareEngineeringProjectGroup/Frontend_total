<template>
  <div class="common-layout page-content" :style="pageStyle">
<!--    <button @click="toggleInvert">切换主题</button>-->
<!--    状态栏-->
      <div class="left">
        <Left/>
      </div>

<!--      主体-->
      <div class="content-container" :style="{ marginLeft: marginLeftValue + 'px' }">
        <Main/>
      </div>

  </div>
</template>


<script setup lang="ts">
import {onBeforeMount, ref, watch,computed} from 'vue'
import Main from './main_container.vue'
import Left from "../SideBar.vue";
import {useStateStore} from "@/stores/stateStore.ts";

let marginLeftValue=ref(60)
// 获取 Pinia Store
const stateStore = useStateStore();
// 监听 stateStore.isOpenValue 的变化



onBeforeMount(() => {
  stateStore.isOpenValue? marginLeftValue.value=240:marginLeftValue.value=60;

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
    if (marginLeftValue.value > 60) { // 最小的 margin-left 值
      marginLeftValue.value -= 10;
    } else {
      clearInterval(interval);
    }
  }, 20); // 每 30 毫秒调整10
};

// 渐渐增加 margin-left 的方法
const increaseMargin = () => {
  let interval = setInterval(() => {
    if (marginLeftValue.value < 240) { // 最大的 margin-left 值
      marginLeftValue.value += 20;
    } else {
      clearInterval(interval);
    }
  }, 20); // 每 30 毫秒调整10
};

const isInverted = ref(false)

// 计算属性，动态应用反转样式
const pageStyle = computed(() => ({
  filter: isInverted.value ? 'invert(1)' : 'none'
}))

// 切换颜色反转的函数
const toggleInvert = () => {
  isInverted.value = !isInverted.value
}
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

</style>