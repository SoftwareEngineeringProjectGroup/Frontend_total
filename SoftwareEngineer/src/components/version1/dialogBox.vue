<template>
  <div
      class="draggable-container"
      :style="{ top: `${position.y}px`, left: `${position.x}px`, position: 'absolute', transition: 'top 0.s ease, left 0.s ease' }"
      ref="draggableContainer"
  >
    <div class="drag-handle" @mousedown="startDrag">
      <el-icon><Rank /></el-icon>
    </div>
    <textarea @keydown="handleKeyDown" class="message-input" v-model="inputValue" placeholder="Please enter here" rows="1" @input="autoResize" style="height: auto;" ></textarea>
    <el-button type="success" :icon="Promotion" @click="sendToMain" size="large" circle/>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import {Promotion, Rank} from "@element-plus/icons-vue";
// import {  defineEmits } from 'vue';

//以下是发送信息给父组件


// 定义 emit 函数
const emit = defineEmits(['send-to-main']);

// 本地输入框的数据
let inputValue = ref('');

// 发送输入内容给父组件
const sendToMain = () => {
  console.log(`发送${inputValue.value}到main`);
  emit('send-to-main', inputValue.value);
  inputValue.value='';
};






//以下是挪动框实现
interface Position {
  x: number;
  y: number;
}

interface Offset {
  x: number;
  y: number;
}

const position = reactive<Position>({ x: window.innerWidth -900, y: window.innerHeight - 150 }) // 初始位置
const offset = reactive<Offset>({ x: 0, y: 0 })
let isDragging = ref<boolean>(false)
const draggableContainer = ref<HTMLDivElement | null>(null)

//更改大小
const autoResize = (event: Event): void => {
  const target = event.target as HTMLTextAreaElement;
  target.style.height = 'auto';
  target.style.height = `${target.scrollHeight}px`;
}

watch(inputValue, (newValue) => {
  const textarea = document.querySelector('.message-input') as HTMLTextAreaElement;
  if (textarea) {
    if (newValue === '') {
      textarea.rows = 1; // 当 inputValue 为空时将行数设为 1
    } else {
      // 根据内容自适应调整高度
      textarea.style.height = 'auto';
      textarea.style.height = `${textarea.scrollHeight}px`;
    }
  }
});



//以下是拖动输入框实现
const startDrag = (event: MouseEvent): void => {
  if (draggableContainer.value) {
    const rect = draggableContainer.value.getBoundingClientRect()
    isDragging.value = true
    offset.x = event.clientX - rect.left
    offset.y = event.clientY - rect.top
    document.addEventListener('mousemove', onDrag)
    document.addEventListener('mouseup', endDrag)
  }
}


const onDrag = (event: MouseEvent): void => {
  if (isDragging.value) {
    // 限制输入框的移动范围，使其在窗口可见区域内
    position.x = Math.max(0, Math.min(event.clientX - offset.x, window.innerWidth - (draggableContainer.value?.offsetWidth || 0)));
    position.y = Math.max(0, Math.min(event.clientY - offset.y, window.innerHeight - (draggableContainer.value?.offsetHeight || 0)));
  }
};

const endDrag = (): void => {
  isDragging.value = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', endDrag)
}


const handleKeyDown = (event: KeyboardEvent) => {
  if (event.ctrlKey && event.key === 'Enter') {
    sendToMain(); // 当按下 Ctrl + Enter 时发送消息
  }
};
</script>

<style scoped>
.draggable-container {
  display: flex;
  align-items: center;
  width: 600px;
  background-color: #f5f5f5;
  border-radius: 30px;
  padding: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #ddd;
  cursor: move;
  transition: box-shadow 0.3s ease, transform 0.3s ease;
}

.draggable-container:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  transform: translateY(-2px);
}

.drag-handle {
  margin-right: 10px;
  cursor: grab;
}

.drag-handle img {
  width: 24px;
  height: 24px;
}

.message-input {
  flex: 1;
  border: none;
  padding: 10px;
  outline: none;
  border-radius: 20px;
  font-size: 16px;
  font-family: 'Roboto', sans-serif; /* 添加好看的字体 */
  line-height: 1.5; /* 增加行高，使得文本看起来更整齐 */
  background-color: transparent;
}



.send-button svg {
  fill: #000;
}
</style>