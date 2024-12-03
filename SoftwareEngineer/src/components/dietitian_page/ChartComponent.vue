<template>
  <div class="container">
    <!-- 食物列表，位于左侧 -->
    <div class="food-list">
      <table>
        <thead>
        <tr>
          <th v-for="index in 3" :key="index">Food Option{{ index }}</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(row, rowIndex) in foodRows" :key="rowIndex">
          <td v-for="(food, colIndex) in row" :key="colIndex" @click="selectFood(food)">
            <div class="food-item">
              <div class="food-name">{{ food.name }}</div>
              <div class="food-category">{{ food.category }}</div>
            </div>
          </td>
        </tr>
        </tbody>
      </table>
    </div>

    <!-- 饼图显示区域，位于右侧 -->
    <div class="chart-container-wrapper">
      <div ref="chart" class="chart-container"></div>
    </div>
  </div>
</template>

<script setup>
import {onMounted, watch, ref, defineExpose} from 'vue';
import * as echarts from 'echarts';

const props = defineProps({
  type: {
    type: String,
    required: true,
  },
});

const chart = ref(null);

const foodData = ref([
  {name: 'Avocado', category: 'Fruit', nutrients: {Protein: 2, Fat: 15, Carbohydrates: 9, Fiber: 7, Sugars: 0.2}},
  {
    name: 'Chicken Breast',
    category: 'Poultry',
    nutrients: {Protein: 31, Fat: 3.6, Carbohydrates: 0, Fiber: 0, Sugars: 0}
  },
  {name: 'Salmon', category: 'Fish', nutrients: {Protein: 25, Fat: 14, Carbohydrates: 0, Fiber: 0, Sugars: 0}},
  {
    name: 'Spinach',
    category: 'Vegetable',
    nutrients: {Protein: 2.9, Fat: 0.4, Carbohydrates: 3.6, Fiber: 2.2, Sugars: 0.4}
  },
  {name: 'Quinoa', category: 'Grain', nutrients: {Protein: 4.1, Fat: 1.9, Carbohydrates: 21, Fiber: 2.8, Sugars: 0.9}},
  {name: 'Eggs', category: 'Dairy', nutrients: {Protein: 6, Fat: 5, Carbohydrates: 0.6, Fiber: 0, Sugars: 0.6}},
  {
    name: 'Broccoli',
    category: 'Vegetable',
    nutrients: {Protein: 2.6, Fat: 0.4, Carbohydrates: 6, Fiber: 2.4, Sugars: 1.5}
  },
  {name: 'Beef', category: 'Meat', nutrients: {Protein: 26, Fat: 15, Carbohydrates: 0, Fiber: 0, Sugars: 0}},
  {name: 'Almonds', category: 'Nuts', nutrients: {Protein: 21, Fat: 49, Carbohydrates: 22, Fiber: 12, Sugars: 3.9}},
  {name: 'Yogurt', category: 'Dairy', nutrients: {Protein: 3.5, Fat: 4, Carbohydrates: 17, Fiber: 0, Sugars: 10.5}},
  {
    name: 'Sweet Potato',
    category: 'Vegetable',
    nutrients: {Protein: 2, Fat: 0.1, Carbohydrates: 20, Fiber: 3, Sugars: 4.2}
  },
  {name: 'Greek Yogurt', category: 'Dairy', nutrients: {Protein: 10, Fat: 5, Carbohydrates: 6, Fiber: 0, Sugars: 4}},
  {name: 'Apple', category: 'Fruit', nutrients: {Protein: 0.5, Fat: 0.3, Carbohydrates: 25, Fiber: 4.4, Sugars: 19}},
  {name: 'Oats', category: 'Grain', nutrients: {Protein: 16.9, Fat: 6.9, Carbohydrates: 66, Fiber: 10.6, Sugars: 0.4}},
  {
    name: 'Carrot',
    category: 'Vegetable',
    nutrients: {Protein: 0.9, Fat: 0.2, Carbohydrates: 9.6, Fiber: 2.8, Sugars: 4.7}
  },
]);

const selectedFood = ref(null);

const getPieOption = (data) => {
  return {
    title: {
      text: `${data.name} Nutrient Distribution`,
      left: 'center',
      top: '5%',
      textStyle: {
        fontSize: 16,
      }
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      bottom: '0%',
      left: 'center',
      itemWidth: 7,
      itemHeight: 7,
    },
    series: [
      {
        name: `${data.name} Components`,
        type: 'pie',
        radius: ['30%', '50%'],
        data: [
          {value: data.nutrients.Protein, name: 'Protein'},
          {value: data.nutrients.Fat, name: 'Fat'},
          {value: data.nutrients.Carbohydrates, name: 'Carbohydrates'},
          {value: data.nutrients.Fiber, name: 'Fiber'},
          {value: data.nutrients.Sugars, name: 'Sugars'},
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
        },
      },
    ],
  };
};

const initChart = (data) => {
  const chartInstance = echarts.init(chart.value);
  const option = getPieOption(data);
  chartInstance.setOption(option);
};

const selectFood = (food) => {
  selectedFood.value = food;
  initChart(food);
};

// 随机生成食物数据
const generateRandomFood = () => {
  const randomName = `Based on table, the`;  // 随机食物名称
  const categories = ['Fruit', 'Vegetable', 'Meat', 'Poultry', 'Grain', 'Dairy', 'Nuts', 'Fish'];
  const randomCategory = categories[Math.floor(Math.random() * categories.length)];  // 随机选择类别

  // 随机生成营养成分
  const randomNutrients = {
    Protein: Math.floor(Math.random() * 50),
    Fat: Math.floor(Math.random() * 30),
    Carbohydrates: Math.floor(Math.random() * 60),
    Fiber: Math.floor(Math.random() * 10),
    Sugars: Math.floor(Math.random() * 30),
  };

  return {name: randomName, category: randomCategory, nutrients: randomNutrients};
};

const isRandomData = ref(false); // 是否使用随机数据

// 更新饼图
const updateChart = async () => {
  const isRandomData = true;
  console.log("chartComponentRef已被调用")
  const randomFood = generateRandomFood();  // 随机生成食物数据
  selectedFood.value = randomFood;
  initChart(randomFood);  // 更新饼图
  return isRandomData;
};

// 暴露给父组件的函数
defineExpose({
  updateChart,
});

// onMounted钩子
onMounted(() => {
  if (updateChart()) {
    console.log("isRandomData为True");
    updateChart();  // 使用随机数据初始化
  } else if (foodData.value.length > 0) {
    selectedFood.value = foodData.value[0];  // 获取第一个食物数据
  }
  initChart(selectedFood.value);  // 使用 selectedFood 初始化饼图
});

const foodRows = ref([]);
onMounted(() => {
  const rows = [];
  for (let i = 0; i < foodData.value.length; i += 3) {
    rows.push(foodData.value.slice(i, i + 3));
  }
  foodRows.value = rows;
});
</script>

<style scoped>
.container {
  width: 870px;
  max-width: 1200px;
  margin-top: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 30px;
  background: linear-gradient(135deg, #ff7f50, #1e90ff);
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.1);
  animation: fadeIn 1s ease-out;
}

.food-list {
  width: 54%;
  padding: 20px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  display: block;
  transition: transform 0.3s ease;
}

.food-list:hover {
  transform: scale(1.05);
}

.food-list table {
  width: 100%;
  border-collapse: collapse;
}

.food-list th,
.food-list td {
  padding: 12px 15px;
  text-align: center;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.food-list th {
  background-color: #ff7f50;
  color: white;
  border-radius: 12px;
}

.food-list td {
  background-color: #f9f9f9;
  border-radius: 12px;
}

.food-list td:hover {
  background-color: #cce7ff;
  transform: scale(1.05);
}

.food-list td:active {
  transform: scale(0.98);
}

.food-item {
  cursor: pointer;
  padding: 10px;
}

.food-name {
  font-size: 16px;
  font-weight: bold;
  color: #1e90ff;
  transition: color 0.3s ease;
}

.food-category {
  font-size: 12px;
  color: gray;
  transition: color 0.3s ease;
}

.food-name:hover {
  color: #ff6347;
}

.chart-container-wrapper {
  width: 60%; /* 饼图容器宽度为一半 */
  height: 450px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  padding: 20px;
  box-sizing: border-box;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: transform 0.3s ease;
}

.chart-container-wrapper:hover {
  transform: scale(1.05);
}

.chart-container {
  width: 100%;
  height: 100%;
}

.chart-container-wrapper .echarts-title {
  font-size: 18px;
  font-weight: bold;
  color: #1e90ff;
  text-align: center;
  margin-bottom: 20px;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

</style>