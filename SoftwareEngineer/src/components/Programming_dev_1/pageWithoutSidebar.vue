<template>
  <div
      class="chat-container"
      :class="{ 'codeBox-active': is_codeBox === 1 }"
  >
    <!-- Initiate 组件 -->
    <div class="initiate">
      <InitialMode @codeBoxAppear="codeBoxAppearance" @uploadMessageToPage="uploadMessageToBackend" @getcode="changecode" @getlang="changelang"/>
    </div>

    <!-- CodeBox 组件 -->
    <div v-if="is_codeBox !== 0" class="codeBox">
      <codeBox :code="exampleCode" :language="codelanguage" :message="messageUser"/>
    </div>
  </div>
</template>

<script setup lang="ts">
import InitialMode from "@/components/Programming_dev_1/InitialMode.vue";
import codeBox from "@/components/Programming_dev_1/codeBox.vue"
import { ref } from "vue";

const is_codeBox = ref(0);

const messageUser = ref('')
const uploadMessageToBackend = (message) => {
  //1. 接受wholeinputbox的message
  messageUser.value = message;
  //2. 将这个发给chatbox
}

const changecode = (message) => {
  exampleCode.value = '\n' + message;
  // exampleCode.value = message;
  console.log(exampleCode.value)
}

const changelang = (message) => {
  codelanguage.value = message
}

const exampleCode = ref(`
print("Hello world!")`);
const codelanguage = ref("python")

const codeBoxAppearance = (message) => {
  is_codeBox.value = message.value;
  console.log(message.value);
};
</script>


<style>
.chat-container {
  position: relative;
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
}


/* 仅在 is_codeBox === 1 时生效的样式 */
.codeBox-active .initiate {
  position: absolute;
  width: 100vw;
  left: 20px;
  z-index: 1;
}

.codeBox-active .codeBox {
  position: absolute;
  width: 45vw;
  height: 100vh;
  right: 20px;
  z-index: 1;
}

</style>