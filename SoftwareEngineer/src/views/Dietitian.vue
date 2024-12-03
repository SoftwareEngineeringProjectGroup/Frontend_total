<template>
  <div class="dietitian">
    <aside class="sidebar">
      <SideBar/>
    </aside>

    <main class="content" :style="{ marginLeft: marginLeftValue + 'px' }">
      <div v-if="currentView === 'main'" class="dialogue-box">
        <div class="whale-container">
          <img src="@/assets/whale.png" alt="Whale" class="whale-image"/>
        </div>

        <h2>Your Personal Health Aide</h2>

        <div class="input-container">
          <input
              type="text"
              placeholder="Enter your request"
              class="input-box"
              v-model="recipeInput"
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
        <button @click="goBack">Return to Main Page</button>

        <!-- 食谱页面 -->
        <div v-if="currentView === 'recipe'" class="recipe-background">
          <div v-if="tableVisible">
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
              <tr v-for="(meals, day) in recipes" :key="day" @click="updateChartWithRandomFood">
                <td class="interactive-cell">{{ day }}</td>
                <td class="interactive-cell">{{ meals.breakfast || 'Loading...' }}</td>
                <td class="interactive-cell">{{ meals.lunch || 'Loading...' }}</td>
                <td class="interactive-cell">{{ meals.dinner || 'Loading...' }}</td>
              </tr>
              </tbody>
            </table>
            <!--            <button @click="updateChartWithRandomFood">test</button>-->
          </div>
        </div>

        <!-- 可视化页面 -->
        <div v-show="currentView === 'visualization'" class="visualization-background">
          <div v-show="chartType === 'pie'" class="chart">
            <ChartComponent :type="chartType" ref="chartComponentRef" />
          </div>
        </div>

        <!-- 图片识别页面 -->
        <div v-if="currentView === 'photo-recognition'" class="photo-recognition-background">
          <foodRecognize/>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onBeforeMount, watch, nextTick} from 'vue';
import { useStateStore } from '@/stores/stateStore';
import { ElMessage } from "element-plus";
import ChartComponent from "@/components/dietitian_page/ChartComponent.vue";
import SideBar from "@/components/SideBar.vue";
import foodRecognize from "@/components/dietitian_page/foodRecognize.vue"

const currentView = ref('main');
const chartType = ref(null);
const store = useStateStore();
const recipeInput = ref('');
const aiResponse = ref('');
const recipes = ref({}); // 动态食谱存储
let recipeData = ref(''); // 每次接收到的动态数据
let baseURL = ''; // 共有url

const tableVisible = ref(false); // 控制表格是否可见，初始为不可见

onBeforeMount(() => {
  baseURL = store.baseUrl;
});

const chartComponentRef = ref(null); // 子组件引用
const updateChartWithRandomFood = async () => {
  await nextTick();  // 确保 DOM 更新完成
  console.log('chartComponentRef:', chartComponentRef.value); // 打印是否正常引用
  if (chartComponentRef.value) {
    chartComponentRef.value.updateChart();  // 更新饼图
  }
};

// 正则表达式去除markdown样式和提示内容
const cleanText = (text) => {
  text = text.replace(/\*{1,2}/g, '').trim(); // 去除 * 和 **（Markdown）
  return text;
};

// 随机生成食谱数据（作为备用）
const generateRandomRecipe = (customPrompt) => {
  const sampleMeals = [
    "Oatmeal Pancakes with Fresh Berries and a Dollop of Greek Yogurt – A balanced breakfast with fiber, antioxidants, and protein to boost energy and support digestion.",
    "Vegetable Egg White Omelette with Sautéed Spinach and Whole Grain Toast – High in protein and fiber, this meal supports muscle recovery and provides lasting energy.",
    "Green Smoothie with Kale, Banana, Chia Seeds, and Almond Milk – A nutrient-packed smoothie with vitamins, potassium, and omega-3s for digestion and heart health.",
    "Grilled Chicken Breast with Quinoa and Steamed Broccoli – Lean protein from chicken, complete protein from quinoa, and fiber from broccoli for a balanced meal.",
    "Mixed Vegetable Salad with Avocado, Cherry Tomatoes, and Lemon-Tahini Dressing – A fresh salad with healthy fats, vitamins, and fiber for a nutrient boost.",
    "High-Fiber Tofu Soup with Carrots, Mushrooms, and Barley – A warm soup with plant-based protein, fiber, and vitamins to support gut health and immunity.",
    "Whole Wheat Pasta with Grilled Zucchini, Cherry Tomatoes, and Basil Pesto – A satisfying dish with fiber, vegetables, and healthy fats from pesto.",
    "Steamed Salmon with Brown Rice, Asparagus, and a Light Dill Sauce – Omega-3 rich salmon with fiber-rich brown rice and asparagus for heart health.",
    "Vegetable Sushi Rolls with Cucumber, Carrot, and Avocado – Light sushi with fiber, healthy fats, and antioxidants for a nutritious snack or meal.",
    "Baked Lean Ribs with Sweet Potato Mash and a Side of Coleslaw – Protein-rich ribs with fiber-packed sweet potatoes and a crunchy, vitamin-filled side."
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

  tableVisible.value = true; // 显示表格
};

const fetchDynamicRecipe = async (input) => {
  const timeout = 10000; // 设置超时时间（10秒）

  const timeoutPromise = new Promise((_, reject) =>
      setTimeout(() => reject(new Error("请求超时")), timeout)
  );

  try {
    const response = await Promise.race([
      fetch(baseURL + "/ai/back", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          model: "gemma2:2b",
          prompt: 'Please provide a balanced and healthy weekly meal plan in the format of Monday{Breakfast:()Lunch:()Dinner:()}.'
              +input,
        }),
      }),
      timeoutPromise, // 如果 fetch 未完成，则返回超时错误
    ]);

    if (!response.body) {
      throw new Error("流式返回没有body");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let done = false;
    recipeData.value = ""; // 每次接收前先清空

    while (!done) {
      const { value, done: readerDone } = await reader.read();
      done = readerDone;

      if (value) {
        // 解码数据块并按行分割
        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split("\n");

        // 逐行解析并处理
        lines.forEach((line) => {
          if (line.trim()) { // 忽略空行
            try {
              const parsedChunk = JSON.parse(line);
              let responseText = parsedChunk.response || '';
              responseText = cleanText(responseText); // 清除markdown和提示内容
              recipeData.value += responseText + " "; // 将返回的食谱数据添加到食谱data
              if (responseText) {
                console.log("正在接收食谱中,这次接收到：", responseText);
              }
            } catch (parseError) {
              console.warn("JSON解析失败，跳过该行: ", line);
            } finally {
              // console.log("接收完成");
              console.log("最终接收结果（recipeData）：", recipeData.value);

              // 正则表达式匹配格式：Day{Breakfast:()Lunch:()Dinner:()}
              const updateRecipeFromDynamicData = (data) => {
                const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
                const newRecipes = {};

                // 为每一天提取 Breakfast、Lunch 和 Dinner
                days.forEach(day => {
                  // 定义正则表达式匹配每一天的 Breakfast, Lunch 和 Dinner
                  const dayRegex = new RegExp(
                      `${day}\\s*:\\s*Breakfast\\s*:\\s*([\\s\\S]+?)\\s*Lunch\\s*:\\s*([\\s\\S]+?)\\s*Dinner\\s*:\\s*([\\s\\S]+?)` +
                      `(?=\\s*(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|Tips|Notes|Important|General|Remember|$))`,
                      'i'
                  );

                  const match = data.match(dayRegex);

                  if (match) {
                    // 提取每天的三餐数据
                    newRecipes[day] = {
                      breakfast: match[1]?.trim() || '',
                      lunch: match[2]?.trim() || '',
                      dinner: match[3]?.trim() || '',
                    };
                  } else {
                    // 如果没有匹配到数据，保留为空
                    newRecipes[day] = {
                      breakfast: '',
                      lunch: '',
                      dinner: '',
                    };
                  }
                });

                // 更新食谱并显示
                recipes.value = newRecipes;
                tableVisible.value = true; // 数据加载完毕后显示表格
                console.log('更新后的食谱:', recipes.value);
              };

              // 更新食谱
              updateRecipeFromDynamicData(recipeData.value);

            }
          }
        });
      }
    }

  } catch (error) {
    console.error('Error fetching dynamic recipe:', error);
    generateRandomRecipe(input); // 如果请求失败，则生成随机食谱
    if (error.message === "请求超时") {
      ErrorPop("Timeout");
    } else {
      ErrorPop("404 Warning");
    }
  }
};

const ErrorPop = (info, time = 3000) => {
  ElMessage({
    showClose: true,
    message: info,
    type: 'error',
    duration: time
  });
};

const handleInput = async () => {
  const inputvalue = recipeInput.value;  // 获取输入框的值并赋给变量
  // 先清空输入框
  recipeInput.value = '';

  // 获取用户输入并传递给 fetchDynamicRecipe
  if (inputvalue.trim()) {
    await fetchDynamicRecipe(inputvalue); // 获取动态食谱
  }
};

const showRecipe = () => {
  currentView.value = "recipe";
  generateRandomRecipe(); // 默认初始化食谱
};

const showVisualization = () => {
  currentView.value = 'visualization'; // 显示可视化页面
  chartType.value = 'pie';             // 默认显示饼图
};

const showPhotoRecognition = () => (currentView.value = 'photo-recognition');
const goBack = () => {
  currentView.value = 'main';
  chartType.value = null;
};

const marginLeftValue = ref(100);
onBeforeMount(() => {
  store.isOpenValue ? (marginLeftValue.value = 200) : (marginLeftValue.value = 69);
});

watch(() => store.isOpenValue, (newValue) => {
  if (newValue === 0) {
    decreaseMargin();
  } else if (newValue === 1) {
    increaseMargin();
  }
});

// 渐渐减小 margin-left 的方法
const decreaseMargin = () => {
  let interval = setInterval(() => {
    if (marginLeftValue.value > 69) { // 最小的 margin-left 值
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
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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
  width: 400px;
  height: 50px;
  padding: 10px;
  border: 2px solid #ccc;
  border-radius: 20px;
  font-size: 16px;
  transition: border-color 0.3s;
}

button {
  padding: 12px 24px;
  background: linear-gradient(135deg, #646cff, #4f5bd5);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  box-shadow: 0 4px 15px rgba(79, 91, 213, 0.4);
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 20px;
}

button:hover {
  background: linear-gradient(135deg, #4f5bd5, #646cff);
  box-shadow: 0 6px 20px rgba(79, 91, 213, 0.6);
  transform: translateY(-2px);
}

button:active {
  transform: translateY(0);
  box-shadow: 0 2px 10px rgba(79, 91, 213, 0.4);
}

.icon-button {
  font-size: 48px;
  margin: 0 20px;
  cursor: pointer;
  transition: transform 0.2s, color 0.2s;
}

.icon-button:hover {
  transform: scale(1.1);
  color: #4f5bd5;
}

.input-box:focus {
  border-color: #4f5bd5;
  outline: none;
  box-shadow: 0 0 8px rgba(79, 91, 213, 0.6);
}

.button-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

/* Recipe section styles */
.recipe-background {
  background: linear-gradient(135deg, rgba(255, 192, 203, 0.8), rgba(255, 105, 180, 0.8)); /* 静态渐变背景色 */
  width: 1400px;
  height: 700px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 15px;
  margin: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); /* 添加柔和的阴影效果 */
  position: relative;
  overflow: hidden;
}

/* 玻璃化效果 */
.recipe-background::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.1); /* 半透明的覆盖层 */
  backdrop-filter: blur(10px); /* 添加模糊效果 */
  border-radius: 15px; /* 保证与父容器的圆角一致 */
  z-index: -1; /* 将模糊层放到后面 */
}

.recipe-table {
  border-collapse: collapse;
  width: 95%;
  text-align: center;
  margin: 0 auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  overflow: hidden;
}

.recipe-table th,
.recipe-table td {
  border: 1px solid #ddd;
  padding: 12px 15px;
  font-family: 'Roboto', sans-serif;
  font-size: 14px;
  color: #333;
  transition: transform 0.3s, background-color 0.3s ease-in-out, box-shadow 0.3s ease; /* 更流畅的过渡效果 */
}

.recipe-table th {
  background-color: #3875d7;
  color: #fff;
  font-weight: bold;
}

.recipe-table td {
  background-color: #fff;
  color: #555;
}

.recipe-table tr:nth-child(even) td {
  background-color: #f9f9f9;
}

.recipe-table tr:nth-child(odd) td {
  background-color: #ffffff;
}

.interactive-cell {
  position: relative;
  cursor: pointer;
  border-radius: 8px;
}

.interactive-cell:hover {
  transform: scale(1.05);
  color: #3875d7;
  background-color: #f0f8ff;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.2);
}

.interactive-cell:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.5);
}

.recipe-table th:hover {
  background-color: #0056b3;
  cursor: pointer;
}

@media (max-width: 768px) {
  .recipe-table {
    width: 100%;
  }
  .recipe-table th, .recipe-table td {
    padding: 10px;
    font-size: 12px;
  }

  .recipe-table th {
    font-size: 13px;
  }
}

.visualization-background {
  background: linear-gradient(135deg, #AFEEEE, #4ac1f7);
  width: 1200px;
  height: 700px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 15px;
  margin: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.photo-recognition-background {
  background: linear-gradient(45deg, #FF6A00, #FFD700);
  width: 1400px;
  height: 700px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 15px;
  margin: auto;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  position: relative;
  overflow: hidden;
}

.features {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 5px;
}

.features button {
  margin-top: 10px;
  margin-left: 0;
  padding: 10px 20px;
  background-color: #4f5bd5;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  position: absolute;
  left: 30px;
  top: 30px;
}

.features button:hover {
  background-color: #646cff;
}

.chart {
  margin-top: 0;
  width: 850px;
  height: 550px;
}
</style>