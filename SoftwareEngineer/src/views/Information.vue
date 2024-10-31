<!--<script setup lang="ts">-->
<!--import SideBar from "@/components/SideBar.vue";-->
<!--</script>-->

<!--<template>-->
<!--  <SideBar/>-->
<!--</template>-->

<!--<style scoped>-->

<!--</style>-->
<template>
  <div>
    <button @click="openFloating">Open Floating Window</button>
  </div>
</template>

<script setup>
function openFloating() {

  window.electronAPI.openFloatingWindow();
  console.log("已按下");
}
</script>
