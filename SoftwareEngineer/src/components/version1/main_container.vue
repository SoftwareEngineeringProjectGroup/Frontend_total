<template>
  <div class="common-layout">
        <Main :receivedInput="sharedInput"/>
      <Bottom @send-to-main="handleSendToMain"/>
  </div>
</template>

<script setup lang="ts">
import Bottom from "./dialogBox.vue";
import Main from "./main.vue";
import {ref} from 'vue'

let sharedInput = ref('');

// 处理 bottom 子组件的发送动作，将数据传递给 main 子组件
const handleSendToMain = (inputValue:any) => {
  // console.log("main收到");
  sharedInput.value = inputValue;
  // console.log(sharedInput.value);
};
</script>

<style scoped>


</style>