<template>
  <div class="speech-demo">
    <h1>Text-to-Speech Demo</h1>
    <textarea v-model="textToSpeak" placeholder="Enter text here"></textarea>
    <button @click="speakMessage(textToSpeak)">🔊 Speak Text</button>
    <button @click="startRecognition">🎙️ Voice Input</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 使用 ref 定义响应式变量
const textToSpeak = ref("");

// 语音播放功能
const speakMessage = (text) => {
  console.time("SpeechSynthesis Start Time"); // 开始计时

  const synth = window.speechSynthesis;
  if (synth.speaking) {
    console.error('SpeechSynthesis is already speaking.');
    return;
  }

  if (text !== '') {
    const utterThis = new SpeechSynthesisUtterance(text);
    utterThis.onstart = () => {
      console.timeEnd("SpeechSynthesis Start Time"); // 结束计时并打印耗时
      console.log('SpeechSynthesisUtterance has started speaking.');
    };
    utterThis.onend = () => {
      console.log('SpeechSynthesisUtterance has finished speaking.');
    };
    utterThis.onerror = (event) => {
      console.error('SpeechSynthesisUtterance error: ', event);
    };

    // 选择语音 (可根据需要进行自定义)
    const voices = synth.getVoices();
    utterThis.voice = voices.find(voice => voice.lang === 'en-US') || voices[0];

    synth.speak(utterThis);
  }
};


// 语音识别功能
const startRecognition = () => {
  // 使用浏览器内置的 Web Speech API 进行语音识别
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = 'en-US';
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    textToSpeak.value = transcript;
    console.log('Voice input recognized: ', transcript);
  };

  recognition.onerror = (event) => {
    console.error('SpeechRecognition error: ', event);
  };

  recognition.start();
};
</script>

<style scoped>
.speech-demo {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
}

textarea {
  width: 300px;
  height: 100px;
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 10px;
}

button:hover {
  background-color: #45a049;
}
</style>
