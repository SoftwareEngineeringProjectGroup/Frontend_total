<template>
  <div class="dietitian">
    <aside class="sidebar" >
      <SideBar />
    </aside>

    <main class="content" :style="{ marginLeft: marginLeftValue + 'px' }">
      <div v-if="currentView === 'main'" class="dialogue-box">
        <div class="whale-container">
          <img src="@/assets/whale.png" alt="Whale" class="whale-image" />
        </div>

        <h2>Your Personal Health Aide</h2>

        <div class="input-container">
          <input
              type="text"
              placeholder="请输入您的需求"
              class="input-box"
              v-model="userInput"
              @keyup.enter="handleInput"
          />
        </div>

        <div class="button-container">
          <div class="icon-button" @click="showRecipe">📋</div>
          <div class="icon-button" @click="showVisualization">📊</div>
          <div class="icon-button" @click="showPhotoRecognition">📷</div>
        </div>
      </div>

      <div v-else>
        <button @click="goBack">返回主界面</button>

        <div v-if="currentView === 'recipe'" class="recipe-background">
          <table class="recipe-table">
            <thead>
            <tr>
              <th>Day</th>
              <th>Breakfast</th>
              <th>Lunch</th>
              <th>Dinner</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(meals, day) in recipes" :key="day">
              <td class="interactive-cell">{{ day }}</td>
              <td class="interactive-cell">{{ meals.breakfast }}</td>
              <td class="interactive-cell">{{ meals.lunch }}</td>
              <td class="interactive-cell">{{ meals.dinner }}</td>
            </tr>
            </tbody>
          </table>
        </div>

        <div v-if="currentView === 'visualization'" class="visualization-background">
          <p>可视化界面内容：</p>
          <div class="features">
            <button @click="() => showChart('pie')">查看饼图</button>
            <button @click="() => showChart('line')">查看折线图</button>
          </div>
          <div v-if="chartType" class="chart">
            <chart-component :type="chartType" />
          </div>
        </div>

        <div v-if="currentView === 'photo-recognition'" class="photo-recognition-background">
          <p>拍照识别界面内容...</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import {ref, computed, onBeforeMount, watch} from 'vue';
import { useStateStore } from '@/stores/stateStore';
import SideBar from "@/components/SideBar.vue";
import ChartComponent from "@/components/dietitian_page/ChartComponent.vue";

const currentView = ref('main');
const chartType = ref(null);
const store = useStateStore();
const userInput = ref('');
const recipes = ref({}); // 存储食谱数据


// 假设从后端获取的食谱数据
const fetchRecipes = () => {
  recipes.value = {
    Monday: { breakfast: "Oatmeal", lunch: "Salad", dinner: "Grilled Chicken" },
    Tuesday: { breakfast: "Pancakes", lunch: "Sushi", dinner: "Pasta" },
    Wednesday: { breakfast: "Smoothie", lunch: "Tacos", dinner: "Steak" },
    Thursday: { breakfast: "Eggs", lunch: "Sandwich", dinner: "Fish" },
    Friday: { breakfast: "Yogurt", lunch: "Burger", dinner: "Pizza" },
    Saturday: { breakfast: "French Toast", lunch: "Quesadilla", dinner: "Curry" },
    Sunday: { breakfast: "Bagel", lunch: "Noodles", dinner: "Stir Fry" }
  };
};

fetchRecipes(); // 初始化时获取食谱数据

const handleInput = () => {
  // 处理输入内容（例如显示食谱等）
  console.log(userInput.value);
  userInput.value = ''; // 清空输入框
};

const showRecipe = () => {
  currentView.value = 'recipe';
};

const showVisualization = () => {
  currentView.value = 'visualization';
};

const showPhotoRecognition = () => {
  currentView.value = 'photo-recognition';
};

const showChart = (type) => {
  chartType.value = type;
};

const goBack = () => {
  currentView.value = 'main';
  chartType.value = null;
};

//以下是伸缩框变化的方法

//记录margin
let marginLeftValue = ref(100);

//挂载时更新margin
onBeforeMount(() => {
  store.isOpenValue ? marginLeftValue.value = 200 : marginLeftValue.value = 69;

});
const decreaseMargin = () => {
  let interval = setInterval(() => {
    if (marginLeftValue.value > 63) { // 最小的 margin-left 值
      marginLeftValue.value -= 10;
    } else {
      clearInterval(interval);
    }
  }, 20); // 每 30 毫秒调整10
};

// 渐渐增加 margin-left 的方法
const increaseMargin = () => {
  let interval = setInterval(() => {
    if (marginLeftValue.value < 200) { // 最大的 margin-left 值
      marginLeftValue.value += 20;
    } else {
      clearInterval(interval);
    }
  }, 20); // 每 30 毫秒调整10
};

//检测变化
watch(() => store.isOpenValue, (newValue) => {
  if (newValue === 0) {
    decreaseMargin();
  } else if (newValue === 1) {
    increaseMargin();
  }
});

</script>

<style scoped>
.dietitian {
  display: flex;
  font-family: Arial, sans-serif;
  height: 100vh;
  background: linear-gradient(135deg, #8fefdd, #5eb3ff, #b78cff, #ff9de2);
  background-size: 400% 400%; /* 放大背景尺寸 */
  animation: gradient-flow 7s ease infinite; /* 默认不流动 */
}

@keyframes gradient-flow {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.sidebar {
  /*background-color: #f0f4f8;
  width: 20%;
  padding: 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: width 0.3s;*/
  position: fixed;
}

.sidebar.collapsed {
  width: 60px;
}

.content {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100vw;
  height: 100vh;
}

.dialogue-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: white;
  padding: 20px;
  width: 400px;
  margin: auto;
  border-radius: 10px; /* 圆角设置 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 可选，增加阴影效果 */
}


.whale-container {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

.whale-image {
  width: 300px;
  height: auto;
  transition: transform 0.3s ease;
  cursor: text;
}

.whale-image:hover {
  transform: scale(1.2);
  cursor: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40"><text y="20" font-size="20">🥕</text></svg>') 1 10, auto;
}

.input-container {
  display: flex;
  align-items: center;
  margin-top: 15px;
}

.input-box {
  width: 600px;
  height: 50px;
  padding: 10px;
  border: 2px solid #ccc;
  border-radius: 20px;
  font-size: 16px;
  transition: border-color 0.3s;
}

.input-box:focus {
  border-color: #4caf50;
  outline: none;
}

.button-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.icon-button {
  font-size: 48px;
  margin: 0 20px;
  cursor: pointer;
  transition: transform 0.2s;
}

.icon-button:hover {
  transform: scale(1.1);
}

button {
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 20px;
}

button:hover {
  background-color: #45a049;
}

/* 食谱部分样式 */
.recipe-background {
  background-color: #FFC0CB;
  width: 1000px;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 15px;
  margin: auto;
}

.recipe-table {
  border-collapse: collapse;
  width: 100%;
  text-align: center;
}

.recipe-table th,
.recipe-table td {
  border: 1px solid #ccc;
  padding: 10px;
  transition: transform 0.3s;
}

.recipe-table th {
  background-color: #f2f2f2;
}

.interactive-cell:hover {
  transform: scale(1.1);
  background-color: #e0ffe0;
}

.visualization-background {
  background-color: #AFEEEE;
  width: 1000px;
  height: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 15px;
  margin: auto;
}

.photo-recognition-background {
  background-color: #7FFFD4;
  width: 1000px;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 15px;
  margin: auto;
}

.features {
  margin-top: 20px;
}

.features button {
  margin: 10px;
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.features button:hover {
  background-color: #45a049;
}

.chart {
  margin-top: 30px;
  width: 500px;
  height: 300px;
}
</style>