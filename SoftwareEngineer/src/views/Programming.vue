<template>
  <div>
    <!-- 按钮 -->
    <el-button
        type="primary"
        @click="togglePopover"
        ref="popoverButton"
        circle
    >
      点击我
    </el-button>

    <!-- Popover 定义 -->
    <el-popover
        v-model:visible="visible"
        trigger="manual"
        placement="bottom"
        :reference="popoverButton"
        width="150"
    >
      <div>
        <el-button type="text" class="option-item" @click="handleOptionClick('Option1')">Option1</el-button>
        <el-button type="text" class="option-item" @click="handleOptionClick('Option2')">Option2</el-button>
        <el-button type="text" class="option-item" @click="handleOptionClick('Option3')">Option3</el-button>
        <el-button type="text" class="option-item" @click="handleOptionClick('Option4')">Option4</el-button>
        <el-button type="text" class="option-item" @click="handleOptionClick('Option5')">Option5</el-button>
      </div>
    </el-popover>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 定义 Popover 的可见状态
const visible = ref(false);

// 获取按钮引用
const popoverButton = ref(null);

// 点击按钮切换 Popover 显示状态
const togglePopover = () => {
  visible.value = !visible.value;
};

// 处理选项点击
const handleOptionClick = (option) => {
  console.log('你选择了:', option);
  visible.value = false; // 选择之后隐藏 Popover
};
</script>

<style scoped>
.option-item {
  display: block;
  width: 100%;
  text-align: left;
  padding: 10px 16px;
}
</style>
