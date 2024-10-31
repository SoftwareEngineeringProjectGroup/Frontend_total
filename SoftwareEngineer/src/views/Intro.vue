<template>
  <div class="app" @click="handleClick">
    <!-- 第一步：HELLO 动画 -->
    <div v-if="currentStep === 1" class="text" :class="{ visible: clickCount === 1, move: clickCount === 2, 'tracking-in-contract': clickCount === 1 }">HELLO</div>

    <!-- 第二步：显示文字 “I'm your personal health AI-de!” -->
    <div v-if="currentStep === 2" class="subtext" :class="{ 'show-subtext': showSubtext }">I'm your personal
      health AI-de!
    </div>

    <!-- 第三步：显示 “Plzzz tell me sth about you!” -->
    <div v-if="currentStep === 3" class="final-text" :class="{ 'final-move': clickCount === 3, 'text-focus-in': clickCount === 3 }">
      Plzzz tell me sth about you!
    </div>

    <!-- 第四步：性别选择界面 -->
    <div v-if="currentStep === 4" class="gender-selection">
      <h2>PLEASE SELECT YOUR GENDER</h2>
      <div class="buttons-container">
        <button class="gender-button male" :class="{ selected: selectedGender === 'male' }" @click.stop="selectGender('male')">&#9794;</button>
        <button class="gender-button female" :class="{ selected: selectedGender === 'female' }" @click.stop="selectGender('female')">&#9792;</button>
      </div>
    </div>

    <!-- 第五步：Try It Now 按钮界面 -->
    <div v-if="currentStep === 5" class="try-now">
      <button class="button" @click.stop="redirectToExample">
        Try It Now :)
        <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
          <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zm4.28 10.28a.75.75 0 000-1.06l-3-3a.75.75 0 10-1.06 1.06l1.72 1.72H8.25a.75.75 0 000 1.5h5.69l-1.72 1.72a.75.75 0 101.06 1.06l3-3z" clip-rule="evenodd"></path>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const clickCount = ref(0)
const currentStep = ref(1)
const showSubtext = ref(false)
const selectedGender = ref(null)

const handleClick = () => {
  clickCount.value++
  if (clickCount.value === 1) {
    currentStep.value = 1
  } else if (clickCount.value === 2) {
    currentStep.value = 2
    setTimeout(() => {
      showSubtext.value = true
    }, 100)
  } else if (clickCount.value === 3) {
    currentStep.value = 3
  } else if (clickCount.value === 4) {
    currentStep.value = 4
  } else if (clickCount.value === 5) {
    currentStep.value = 5
  }
}

const selectGender = (gender) => {
  selectedGender.value = gender
}

const redirectToExample = () => {
  router.push({ name: 'DietitianMain' });
};

</script>

<style scoped>
/* 全局样式 */
.app {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  font-family: Arial, sans-serif;
  cursor: pointer;
  flex-direction: column;
  background: rgb(255,253,169);
  background: radial-gradient(circle, rgba(255,253,169,1) 0%, rgba(178,249,145,1) 100%);
}
/* 新增 .text-focus-in 动画样式 */
.text-focus-in {
  animation: text-focus-in 1s cubic-bezier(0.55, 0.085, 0.68, 0.53) both;
}

@-webkit-keyframes text-focus-in {
  0% {
    -webkit-filter: blur(12px);
    filter: blur(12px);
    opacity: 0;
  }
  100% {
    -webkit-filter: blur(0);
    filter: blur(0);
    opacity: 1;
  }
}

@keyframes text-focus-in {
  0% {
    -webkit-filter: blur(12px);
    filter: blur(12px);
    opacity: 0;
  }
  100% {
    -webkit-filter: blur(0);
    filter: blur(0);
    opacity: 1;
  }
}

/* HELLO 动画样式 */
.text {
  font-size: 7.5rem;
  font-weight: bold;
  opacity: 0;
  transition: opacity 1s ease, transform 1s ease;
  transform: scale(0.5);
}

.visible {
  opacity: 1;
  transform: scale(2);
}

.move {
  opacity: 0.2;
  transform: scale(0.5) translate(-150px, -150px);
  transition: opacity 2s ease, transform 2s ease;
}

/* 第二步的子文字 */
.subtext {
  font-size: 5rem;
  opacity: 0;
  transition: opacity 1s ease, transform 1s ease;
}

.show-subtext {
  opacity: 1;
  transform: scale(1.5);
}

/* 第三步文字动画 */
.final-text {
  font-size: 8rem;
  position: absolute;
  left: -100%;
  opacity: 0;
  transition: transform 2s ease, opacity 2s ease;
}

.final-move {
  left: 50%;
  transform: translateX(-50%);
  opacity: 1;
}

/* 性别选择框样式 */
.gender-selection {
  text-align: center;
  padding: 20px;
  border-radius: 10px;
  background: linear-gradient(135deg, #56ab2f, #a8e063);
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  animation: fadeIn 1s ease;
}

.gender-selection h2 {
  font-size: 20px;
  color: #efffee;
  margin-bottom: 20px;
}

.buttons-container {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.gender-button {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: 3px solid rgba(255, 255, 255, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30px;
  font-weight: bold;
  color: rgb(4, 96, 59);
  cursor: pointer;
  transition: transform 0.2s;
  background-color: hsl(117, 47%, 80%);
}

.gender-button:hover {
  transform: scale(1.1);
}

.gender-button.selected {
  background-color: hsl(117, 47%, 50%);
  color: #fff;
  border-color: rgba(255, 255, 255, 1);
}

/* Try It Now 按钮样式 */
.try-now .button {
  position: relative;
  padding: 0.5rem 1.25rem;
  background-color: #82ce8e;
  border-radius: 9999px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  gap: 10px;
  font-weight: bold;
  border: 3px solid #89ffc64d;
  font-size: 15px;
  cursor: pointer;
  box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.2);
  outline: none;
  overflow: hidden;
  transition: all 0.3s ease-in-out;
}

.icon {
  width: 24px;
  height: 24px;
  transition: all 0.3s ease-in-out;
}

.button:hover {
  transform: scale(1.05);
  border-color: #fff9;
}

.button:hover .icon {
  transform: translate(4px);
}

.button:hover::before {
  animation: shine 1.5s ease-out infinite;
}

.button::before {
  content: "";
  position: absolute;
  width: 100px;
  height: 100%;
  background-image: linear-gradient(120deg, rgba(255, 255, 255, 0) 30%, rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0) 70%);
  top: 0;
  left: -100px;
  opacity: 0.6;
}
/* 新增 .tracking-in-contract 动画样式 */
.tracking-in-contract {
  animation: tracking-in-contract 0.8s cubic-bezier(0.215, 0.61, 0.355, 1.000) both;
}

@keyframes tracking-in-contract {
  0% {
    letter-spacing: 1em;
    opacity: 0;
  }
  40% {
    opacity: 0.6;
  }
  100% {
    letter-spacing: normal;
    opacity: 1;
  }
}

@keyframes shine {
  0% {
    left: -100px;
  }
  60% {
    left: 100%;
  }
  to {
    left: 100%;
  }
}
</style>
