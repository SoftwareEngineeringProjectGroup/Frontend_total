

<template>

  <SideBar/>
  <div class="centered-div">
    <el-input v-model="baseUrl" style="width: 240px" placeholder="Input iPv4 Address" size="large" @keydown.enter="setUrl"/>

    <el-button type="primary" round @click="setUrl" class="b" size="large">Set Address</el-button>
  </div>

</template>

<script setup>
import SideBar from "@/components/SideBar.vue";
import { ref } from 'vue'
const baseUrl = ref('')
import {useStateStore} from "@/stores/stateStore";
let stateStore=useStateStore()
const setUrl=()=>{
  stateStore.setbaseUrl(baseUrl.value);
  console.log("设定为",baseUrl.value);
  baseUrl.value='';
}

</script>


<style scoped>
.centered-div {
  position: absolute;
  top: 40%;
  left: 40%;
}

.b{
  margin-left: 10px;
}
</style>