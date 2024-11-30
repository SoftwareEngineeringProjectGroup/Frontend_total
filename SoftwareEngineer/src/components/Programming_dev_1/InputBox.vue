<template>
  <el-input class="inputBox"
      v-model="textarea1"
      style="width: 600px"
      size="large"
      autosize
      type="textarea"
      placeholder="Message Lambda"
      resize="none"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
const textarea1 = ref('')
</script>

<style scoped>
.inputBox {
  border-radius: 0; /* 设置和父组件一样的圆角 */
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center;     /* 垂直居中 */
  border:0;
  padding-left: 0;
}
.inputBox :deep(.el-textarea__inner){
  background-color: #fafafa;
  box-shadow: 0 0 0 0;
}
</style>