<template>
  <div class="dietitian">
    <aside class="sidebar">
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
              placeholder="Enter your request"
              class="input-box"
              v-model="userInput"
              @keyup.enter="handleInput"
          />
        </div>

        <div class="response-container" v-if="aiResponse">
          <p>AI Reply: {{ aiResponse }}</p>
        </div>

        <div class="button-container">
          <div class="icon-button" @click="showRecipe">📋</div>
          <div class="icon-button" @click="showVisualization">📊</div>
          <div class="icon-button" @click="showPhotoRecognition">📷</div>
        </div>
      </div>

      <div v-else>
        <button @click="goBack">Return to Main Page</button>

        <!-- 食谱页面 -->
        <div v-if="currentView === 'recipe'" class="recipe-background">
          <div class="input-container">
            <input
                type="text"
                placeholder="Generate new meals..."
                class="input-box"
                v-model="recipeInput"
                @keyup.enter="handleInput"
            />
          </div>

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
              <td class="interactive-cell">{{ meals.breakfast || 'Loading...' }}</td>
              <td class="interactive-cell">{{ meals.lunch || 'Loading...' }}</td>
              <td class="interactive-cell">{{ meals.dinner || 'Loading...' }}</td>
            </tr>
            </tbody>
          </table>

          <p>{{ aiResponse }}</p>
        </div>

        <!-- 可视化页面 -->
        <div v-if="currentView === 'visualization'" class="visualization-background">
          <p>Visualization Content:</p>
          <div class="features">
            <button @click="showChart('pie')">View Pie Chart</button>
            <button @click="showChart('line')">View Line Chart</button>
          </div>
          <div v-if="chartType" class="chart">
            <ChartComponent :type="chartType" />
          </div>
        </div>

        <!-- 图片识别页面 -->
        <div v-if="currentView === 'photo-recognition'" class="photo-recognition-background">
          <p>Photo Recognition Content...</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onBeforeMount, watch } from 'vue';
import { useStateStore } from '@/stores/stateStore';

const currentView = ref('main');
const chartType = ref(null);
const store = useStateStore();
const userInput = ref('');
const recipeInput = ref('');
const aiResponse = ref('');
const recipes = ref({});

// 随机生成食谱数据
const generateRandomRecipe = (customPrompt) => {
  const sampleMeals = [
    "Pancakes", "Omelette", "Smoothie", "Grilled Chicken", "Salad",
    "Soup", "Pasta", "Steamed Fish", "Sushi", "BBQ Ribs"
  ];

  const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
  const newRecipes = {};

  days.forEach(day => {
    newRecipes[day] = {
      breakfast: sampleMeals[Math.floor(Math.random() * sampleMeals.length)],
      lunch: sampleMeals[Math.floor(Math.random() * sampleMeals.length)],
      dinner: sampleMeals[Math.floor(Math.random() * sampleMeals.length)],
    };
  });

  recipes.value = newRecipes;

  if (customPrompt) {
    aiResponse.value = `New meals generated based on input: "${customPrompt}"`;
  }
};

// 设置请求超时时间
const TIMEOUT = 5000;

// 创建超时 Promise
const createTimeoutPromise = (timeout) => {
  return new Promise((_, reject) => {
    setTimeout(() => {
      reject(new Error('Request timed out'));
    }, timeout);
  });
};

// 向后端发送请求以获取动态食谱
const fetchDynamicRecipe = async (input) => {
  try {
    const baseURL = 'http://127.0.0.1:8000';
    const timeoutPromise = createTimeoutPromise(TIMEOUT);

    const response = await Promise.race([
      fetch(`${baseURL}/ai/back`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: "gemma2:2b",
          prompt: input
        })
      }),
      timeoutPromise
    ]);

    if (response.ok) {
      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');

      let recipesData = {};
      let processingMessage = '';

      const processStream = async () => {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value, { stream: true });
          const lines = chunk.split('\n').filter(line => line.trim());

          for (const line of lines) {
            try {
              const jsonLine = JSON.parse(line);
              if (jsonLine.status === 'processing') {
                processingMessage = jsonLine.message;
              } else if (jsonLine.status === 'streaming') {
                const recipeContent = jsonLine.recipe;
                // 使用正则表达式提取关键信息
                const regex = /{"day":"(.*?)","meal":"(.*?)","food":"(.*?)"/;
                const match = recipeContent.match(regex);
                if (match) {
                  const [_, day, meal, food] = match;
                  if (!recipesData[day]) {
                    recipesData[day] = {};
                  }
                  recipesData[day][meal] = food;
                }
              } else if (jsonLine.status === 'done') {
                recipes.value = recipesData;
                aiResponse.value = processingMessage;
                return;
              }
            } catch (error) {
              console.error('Error parsing stream data:', error);
            }
          }
        }
      };

      await processStream();
    } else {
      throw new Error('Failed to fetch dynamic recipe');
    }
  } catch (error) {
    console.error('Error fetching dynamic recipe:', error);
    generateRandomRecipe(input); // 使用默认的随机生成食谱数据
  }
};

const handleInput = async () => {
  if (!recipeInput.value.trim()) return;
  await fetchDynamicRecipe(recipeInput.value);
  recipeInput.value = ''; // 清空输入框
};

const showRecipe = () => {
  currentView.value = "recipe";
  generateRandomRecipe(); // 默认初始化食谱
};

const showVisualization = () => (currentView.value = 'visualization');
const showPhotoRecognition = () => (currentView.value = 'photo-recognition');
const goBack = () => {
  currentView.value = 'main';
  chartType.value = null;
};

const showChart = (type) => (chartType.value = type);

const marginLeftValue = ref(100);
onBeforeMount(() => {
  store.isOpenValue ? (marginLeftValue.value = 200) : (marginLeftValue.value = 69);
});

watch(
    () => store.isOpenValue,
    (newValue) => {
      if (newValue === 0) {
        marginLeftValue.value = 69;
      } else if (newValue === 1) {
        marginLeftValue.value = 200;
      }
    }
);
</script>


<style scoped>
.dietitian {
  display: flex;
  font-family: Arial, sans-serif;
  height: 100vh;
  background: linear-gradient(135deg, #8fefdd, #5eb3ff, #b78cff, #ff9de2);
  background-size: 400% 400%; /* Enlarge background size */
  animation: gradient-flow 7s ease infinite; /* Default no flow */
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
  width: 800px;
  margin: auto;
  border-radius: 10px; /* Rounded corners */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Optional, add shadow effect */
}

.whale-container {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

.whale-image {
  width: 350px;
  height: auto;
  transition: transform 0.3s ease;
  cursor: text;
}


.input-container {
  display: flex;
  align-items: center;
  margin-top: 15px;
}

.input-box {
  width: 400px;
  height: 50px;
  padding: 10px;
  border: 2px solid #ccc;
  border-radius: 20px;
  font-size: 16px;
  transition: border-color 0.3s;
}

.input-box:focus {
  border-color: #4f5bd5;
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
  background-color: #4f5bd5;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 20px;
}

button:hover {
  background-color: #646cff;
}

/* Recipe section styles */
.recipe-background {
  background-color: #FFC0CB;
  width: 1200px;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 15px;
  margin: auto;
}

.recipe-table {
  border-collapse: collapse;
  width: 95%;
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
  background-color: #4f5bd5;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.features button:hover {
  background-color: #646cff;
}

.chart {
  margin-top: 30px;
  width: 500px;
  height: 300px;
}
</style>
