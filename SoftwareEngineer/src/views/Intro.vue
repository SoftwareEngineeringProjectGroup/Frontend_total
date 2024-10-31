<template>
  <div class="app" @click="nextState" @mousemove="moveGlow">
    <div class="glow" :style="{ left: glowPosition.x + 'px', top: glowPosition.y + 'px' }"></div>
    <div v-if="state === 1" class="state state1">
      <h1 class="glow whale-hover" style="z-index: 10; margin-top: 5px; margin-bottom: 100px;">Bonjour!</h1>
      <img src="@/assets/whale.png" alt="Whale Logo" class="whale-logo large-whale mirror whale-hover" style="z-index: 10;" />
    </div>
    <div v-if="state === 2" class="state state2">
      <h1 class="glow gray-text whale-hover" style="z-index: 10; margin-top: 5px; margin-bottom: 100px;">Bonjour,</h1>
      <h2 class="whale-hover" style="z-index: 10;margin-top: 100px; margin-bottom: 100px;">I'm your personal health AI-de!</h2>
      <img src="@/assets/whale.png" alt="Whale Logo" class="whale-logo mirror whale-hover" style="z-index: 10; margin-top: 10px;" />
    </div>
    <div v-if="state === 3" class="state state3">
      <h2 class="whale-hover" style="z-index: 10;">PLZzzz tell me something about you!</h2>
      <div class="image-boxes">
        <div class="gray-box">
          <img src="@/assets/diet.png" alt="Diet" class="gray-image" />
        </div>
        <div class="gray-box">
          <img src="@/assets/exercise.png" alt="Exercise" class="gray-image" />
        </div>
        <div class="gray-box">
          <img src="@/assets/sleep.png" alt="Sleep" class="gray-image" />
        </div>
      </div>
    </div>
    <div v-if="state === 4" class="state state4">
      <h2 class="whale-hover" style="z-index: 10;">Your Personal Health Aide</h2>
      <input type="text" placeholder="Enter your question..." v-model="userInput" @keyup.enter="goToDietitian" class="input-box" />
      <img src="@/assets/whale.png" alt="Whale Logo" class="whale-logo whale-hover" style="z-index: 10;" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      state: 1,
      userInput: "",
      glowPosition: { x: 0, y: 0 }
    };
  },
  methods: {
    nextState() {
      if (this.state < 4) {
        this.state++;
      }
    },
    goToDietitian() {
      if (this.userInput) {
        this.$router.push({ name: "DietitianMain" });
      }
    },
    moveGlow(event) {
      this.glowPosition.x = event.clientX - 100;
      this.glowPosition.y = event.clientY - 100;
    }
  }
};
</script>

<style scoped>
.app {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #afeeee;
  font-family: Arial, sans-serif;
  cursor: pointer;
  position: relative;
}

.state {
  text-align: center;
}

.glow {
  position: absolute;
  width: 200px;
  height: 200px;
  border-radius: 80%;
  background: radial-gradient(circle, rgba(255, 255, 0, 0.3), rgba(255, 255, 0, 0) 70%);
  pointer-events: none;
  transition: opacity 0.3s ease;
  z-index: 1;
}

.state1 h1,
.state2 h1 {
  font-size: 3em;
  color: #4a4a4a;
}

.state2 h1.gray-text {
  color: #7d7d7d;
}

.state2 h2,
.state3 h2,
.state4 h2 {
  font-size: 2em;
  color: #333333;
}

.image-boxes {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.gray-box {
  width: 420px;
  height: 320px;
  background-color: #cccccc;
  margin: 0 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.gray-image {
  width: 400px;
  height: auto;
  transition: transform 0.3s ease;
}

.gray-image:hover {
  transform: scale(1.1);
}

.whale-logo {
  width: 200px;
  margin-top: 20px;
  transition: transform 0.5s ease-in-out;
}

.large-whale {
  width: 300px;
}

.mirror {
  transform: scaleX(-1);
}

.input-box {
  width: 300px;
  padding: 10px;
  font-size: 1.2em;
  margin-top: 20px;
  border: 2px solid #ccc;
  border-radius: 20px;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.input-box:focus {
  border-color: #4caf50;
  outline: none;
  box-shadow: 0 0 5px rgba(76, 175, 80, 0.5);
}

.whale-hover:hover,
.whale-hover:focus {
  transform: scale(1.1);
}
</style>