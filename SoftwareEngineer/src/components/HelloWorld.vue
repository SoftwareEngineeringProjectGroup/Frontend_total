<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

defineProps<{ msg: string }>()

const count = ref(0)

const testAxios=()=>{
  axios.get("/data.json")
      .then((result) => {
        // result不是直接的返回结果
        console.log("数据：",result);
        // result.data才是真正的返回结果
        console.log("真正的数据：",result.data);
      })
      .catch((err) => {
        console.log(err);
      });
}
</script>

<template>
  <h1>{{ msg }}</h1>

  <div class="card">
    <el-button type="primary" @click="count++">count is {{ count }}</el-button>
    <el-button type="warning" @click="testAxios">测试axios</el-button>
    <p>
      Edit
      <code>components/HelloWorld.vue</code> to test HMR
    </p>
  </div>

  <p>
    Check out
    <a href="https://vuejs.org/guide/quick-start.html#local" target="_blank"
      >create-vue</a
    >, the official Vue + Vite starter
  </p>
  <p>
    Learn more about IDE Support for Vue in the
    <a
      href="https://vuejs.org/guide/scaling-up/tooling.html#ide-support"
      target="_blank"
      >Vue Docs Scaling up Guide</a
    >.
  </p>
  <p class="read-the-docs">Click on the Vite and Vue logos to learn more</p>
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
