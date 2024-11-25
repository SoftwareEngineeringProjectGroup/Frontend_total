<template>
  <div>
<!--  <el-button :type="type" @click="change" round class="top-button">{{ text }}</el-button>-->
  <!--  <button @click="send0">点</button>-->
  <el-menu
      :default-active="$route.path"
      class="el-menu-vertical-demo"
      :collapse="isCollapse"
      router

  >
    <!-- 首页 -->
    <el-menu-item index="/">
      <el-icon>
        <House/>
      </el-icon>
      <template #title>Home</template>
    </el-menu-item>

    <!-- 模式选择 -->
    <el-sub-menu index="2">
      <template #title>
        <el-icon>
          <icon-menu/>
        </el-icon>
        <span>Option</span>
      </template>

      <!-- 模式选择的菜单 -->
      <el-menu-item-group>
        <template #title><span>Mode</span></template>

        <!-- 聊天 -->
        <el-menu-item index="/chat">
          <el-icon>
            <ChatRound/>
          </el-icon>
          <template #title>Chat</template>
        </el-menu-item>

        <!-- 信息检索 -->
        <el-menu-item index="/information">
          <el-icon>
            <SwitchFilled/>
          </el-icon>
          <template #title>Information</template>
        </el-menu-item>

        <!-- 编程助理 -->
        <el-menu-item index="/programming">
          <el-icon>
            <Monitor/>
          </el-icon>
          <template #title>Programming</template>
        </el-menu-item>

        <!-- 营养师 -->
        <el-menu-item index="/dietitian">
          <el-icon>
            <DishDot/>
          </el-icon>
          <template #title>Nutritionist</template>
        </el-menu-item>
      </el-menu-item-group>
    </el-sub-menu>

    <!-- 用户评论，目前禁用 -->
    <el-menu-item index="3">
      <el-icon>
        <chat-dot-square/>
      </el-icon>
      <template #title>Feedback</template>
    </el-menu-item>

    <!-- 设置 -->
    <el-menu-item index="/setting">
      <el-icon>
        <setting/>
      </el-icon>
      <template #title>Setting</template>
    </el-menu-item>
<!--    <el-button :type="type" @click="change" round class="top-button">{{ text }}</el-button>-->

<!--    展开按钮-->
    <el-menu-item @click="change">
      <el-icon v-if="isCollapse">
        <ArrowRightBold/>
      </el-icon>
      <el-icon v-else>
        <ArrowLeftBold/>
      </el-icon>
      <template #title>{{text}}</template>
    </el-menu-item>

  </el-menu>
  </div>
</template>

<script lang="ts" setup>
import {ref, onBeforeMount} from 'vue'
import {useStateStore} from '@/stores/stateStore';
import {
  ChatRound,
  Menu as IconMenu,
  Setting,
  House,
  SwitchFilled,
  ChatDotSquare,
  Monitor,
  DishDot,
  ArrowRightBold,
  ArrowLeftBold
} from '@element-plus/icons-vue'

const isCollapse = ref<boolean | null>(null) // 是否伸缩
let text = ref<string | null>(null) // 标签上的字
// let type = ref<string | null>(null)


// 获取 Pinia Store
const stateStore = useStateStore();

// 用于在组件中存储获取到的状态
const state = ref<number | null>(null);

// 在组件挂载时提取信息
onBeforeMount(() => {
  state.value = stateStore.isOpenValue;

  if (state.value) {
    isCollapse.value = false;
    text.value = "Collapse";

  } else {
    isCollapse.value = true;
    text.value = "Expand";

  }
  // console.log('Value from store:', state.value, isCollapse.value);
});


//伸缩变色和字
const change = () => {
  isCollapse.value = !isCollapse.value
  if (text.value === "Expand") {
    text.value = "Collapse"

    stateStore.setisOpenValue(1);
  } else {
    text.value = "Expand";
    stateStore.setisOpenValue(0);
  }
  // console.log("变化后", stateStore.value, isCollapse.value);

}


// 伸缩触发
// const handleOpen = (key: string, keyPath: string[]) => {
//   // console.log(key, keyPath)
// }
// const handleClose = (key: string, keyPath: string[]) => {
//   // console.log(key, keyPath)
// }
</script>

<style>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 670px;
}

.el-menu-vertical-demo:not(.el-menu--expand) {
  min-height: 100vh;
}

.el-menu-vertical-demo {
  flex: 1;
  overflow: auto; /* 让菜单部分可滚动 */
  margin-top: 0px;
}

.top-button {
  margin-bottom: 10px; /* 距离下方内容 20 像素 */
}
</style>
