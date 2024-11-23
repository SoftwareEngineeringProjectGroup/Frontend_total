<template>
  <div class="chat-container">
    <div class="initiate">
      <InitialMode/>
    </div>
    <div class="chatBox">
      聊天框
    </div>
    <div class="input">
      <InputBox/>
    </div>
  </div>
</template>

<script setup lang="ts">
import InitialMode from "@/components/Programming_dev_1/InitialMode.vue";
import InputBox from "@/components/Programming_dev_1/InputBox.vue";
</script>

<style>
</style>
