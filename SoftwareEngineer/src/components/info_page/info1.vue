<template>
  <div class="chat-page">

    <!--    悬浮球-->
    <div class="float-ball" ref="ball">
      <div v-if="showPetals" v-for="n in 5" :key="n" class="petal"></div>
      <div v-if="expandedMessageTip" class="expanded-message message-text markdown-body" ref="expandedMessageDiv"
           v-html="renderedText(expandedMessage)"></div>
    </div>

    <!--    过往信息显示-->

    <div class="past-info">
      <el-button
          v-for="(ask, index) in asks"
          :key="index"
          class="question-bubble"
          @click="handleBubbleClick(index)"
          @dblclick="handleDoubleClick(index)"
          size="large"
      >
        {{ ask.user.text }}
      </el-button>
    </div>

<!--    <button @click="fileDelete">恢复</button>-->
    <!--    输入框-->
    <div class="input-container">

      <!--      网络按钮-->
      <el-button type="primary" @click="sendToModel" :icon="InterIcon" size="large" style="font-size: 24px;" circle>
      </el-button>

      <input class="message-input" v-model="inputValue" placeholder="Please enter here" ref="messageInput"
             @keydown="handleKeyDown">

      <!--      发送按钮-->
      <el-button :type="sendColor" :icon="sendIcon" @click="sendToModel" size="large" style="font-size: 20px;" circle/>

      <!--      图片上传按钮-->
      <el-button :type=fileColor size="large" class="dropdown-button" :icon="fileIcon" style="font-size: 20px;"
                 @click="triggerFileInput" circle/>

      <!--      悬浮窗按钮-->
      <el-button type="info" size="large" class="dropdown-button" :icon="More" style="font-size: 20px;" @click="openFloating" circle/>

      <!-- 隐藏的文件输入框 -->
      <input ref="fileInput" type="file" @change="onFileChange" style="display: none"/>

      <!-- 显示选择的图片 -->
      <div v-if="imageUrl">
        <img :src="imageUrl" alt="上传的图片" style="max-width: 100%; height: auto;"/>
      </div>
    </div>

  </div>
</template>

<script lang="ts" setup>
import {ref, onMounted, watch, nextTick, onBeforeMount} from 'vue';
import gsap from 'gsap';
import {More, Picture, Promotion, Delete} from "@element-plus/icons-vue";
import {ElMessage} from "element-plus";
// Markdown 逻辑
import MarkdownIt from "markdown-it";
import 'highlight.js/styles/github.css'; // 确保引入样式文件
import InterIcon from '@/assets/informationPage/internet-yes.svg'
import Close from '@/assets/informationPage/close.svg'
import {useStateStore} from "@/stores/stateStore.ts";


//模型回复的加载标记
let isAILoading = ref(false)

//输入信息
let inputValue = ref("")
//信息列表
//过去的询问列表
let asks = ref([{
  "user": {text: 'What date today', internet: true, isPhoto: false, photoUrl: ''},
  "ai": {text: "19th October"}
}, {
  "user": {text: 'Tell some news', internet: true, isPhoto: false, photoUrl: ''},
  "ai": {text: "Okay, here's a quick rundown on some current events:\n" +
        "\n" +
        "**International:**\n" +
        "\n" +
        "*  **The World Cup is heating up:**   We are heading into the knockout stages in football, with incredible matches and\n" +
        "drama.  Who do you think will make it through? ⚽\n" +
        "* **Global inflation remains high:** This means that prices for everyday goods are going up everywhere. 📈\n" +
        "* **Climate change is a major focus:** There are protests and discussions worldwide about how to move towards more\n" +
        "sustainable practices, with many eyes on the next UN climate summit in December. 🌍\n" +
        "\n" +
        "\n" +
        "**US:**\n" +
        "\n" +
        "* **Politics is still front and center:** There are ongoing debates around several key issues, including healthcare\n" +
        "and immigration.\n" +
        "* **Elon Musk's Twitter takeover continues:**  He's making big changes to the platform and sparking mixed reactions\n" +
        "from users and experts alike. 🤔\n" +
        "**Other notable things going on:**\n" +
        "\n" +
        "* **Record-breaking weather in some places:** From wildfires in California to floods in Europe, there are extreme\n" +
        "weather events happening worldwide. 🌦️\n" +
        "* **SpaceX continues its missions!**  We're getting closer to a future with regular space tourism and commercial lunar\n" +
        "ventures. 🚀\n" +

        "Let me know if you want more details on any of these topics or have specific news areas you'd like me to focus on! 📰"}
}, {
  "user": {text: 'Summarize', internet: true, isPhoto: false, photoUrl: ''},
  "ai": {text: "I will try"}
}, {
  "user": {text: 'Weather?', internet: true, isPhoto: false, photoUrl: ''},
  "ai": {
    text: 'The weather in Foshan today is looking a bit mixed:\n' +
        '\n' +
        '* **Partly sunny** with some clouds throughout the day.\n' +
        '* **High temperature:** around 28°C (82°F)\n' +
        '* **Low temperature:** about 21°C (70°F)\n' +
        '* **Windy**, so be prepared for a bit of breeze!\n' +
        '\n' +
        '\n' +
        'Enjoy your time in Foshan! 😊'
  }
}

]);

//点击气泡信息后输出历史信息
const handleBubbleClick = (index: number) => {
  // 输出点击的气泡对应的 ai.text
  console.log(asks.value[index].ai.text);
  expandedMessage.value = asks.value[index].ai.text;
  expandBall();
};

//显示信息的区域
let showHTML = ref("");


//发送信息
const sendToModel = () => {
  // 展开时关闭展开
  if (expandedMessageTip) {
    sendNormal();
    revertBall();
    return;
  }
  if (inputValue.value === "") {
    ErrorPop("Please enter something", 2000);
    return;
  }
  asks.value.push({
    "user": {text: inputValue.value, internet: true, isPhoto: false, photoUrl: ''},
    "ai": {text: ""}
  });
  getAnswer();
  const temp_text = inputValue.value;
  inputValue.value = '';
  sendCartoon(temp_text);
  startScaling();
};


//ai返回
const getAnswer = async () => {
  const timeout = 10000; // 设置超时时间（以毫秒为单位，例如10秒）

  const timeoutPromise = new Promise((_, reject) =>
      setTimeout(() => reject(new Error("请求超时")), timeout)
  );
  expandedMessage.value = ""//确保清空

  try {

    const response = await Promise.race([
      fetch(baseURL + "/ai/back", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          model: "gemma2:2b",
          prompt: inputValue.value,
        }),
      }),
      timeoutPromise, // 如果 fetch 未完成，此 promise 将优先返回超时错误
    ]);

    if (!response.body) {
      throw new Error("流式返回没有body");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let done = false;

    isAILoading.value = false; // 解除加载

    tempChangeBallColor();


    while (!done) {
      const {value, done: readerDone} = await reader.read();
      done = readerDone;

      if (value) {
        // 解码数据块并按行分割
        const chunk = decoder.decode(value, {stream: true});
        // console.log("chunk",chunk);
        const lines = chunk.split("\n");

        // 逐行解析并处理
        lines.forEach((line) => {
          if (line.trim()) { // 忽略空行
            try {
              const parsedChunk = JSON.parse(line);
              asks.value[asks.value.length - 1].ai.text += parsedChunk.response;
              expandedMessage.value += parsedChunk.response;
            } catch (parseError) {
              console.warn("JSON解析失败，跳过该行: ", line);
            }
          }
        });
      }
    }
    stopScaling();//停止抖动
    await expandBall();


    console.log("流结束");
  } catch (error) {
    console.error("错误: ", error);
    asks.value.pop(); //直接删去最后一个
    await revertBall();
    if (error.message === "请求超时") {
      ErrorPop("Timeout");
      stopScaling();
    } else {
      ErrorPop("404 Warning");
      stopScaling();
    }
  }
};

//错误弹窗
const ErrorPop = (info: string, time = 3000) => {
  ElMessage({
    showClose: true,
    message: info,
    type: 'error',
    duration: time
  })
}


//动态效果的实现
let expandedMessageTip = false;
let expandedMessage = ref("");

// 初始化 MarkdownIt 实例
const md = new MarkdownIt();
const renderedText = (text: string) => {
  return md.render(text);
};

// 定义响应式变量
const ball = ref(null);
const expandedMessageDiv = ref(null);
const messageInput = ref(null);
const isBallWobbling = ref(true);
const showPetals = ref(true);
let scalingTween = null; // 用来存放综缩动画的参考

// 发送消息的抖动效果
const sendCartoon = (text: string) => {
  if (text.trim() === '') return;

  const inputBox = messageInput.value.getBoundingClientRect();
  const ballBox = ball.value.getBoundingClientRect();

  const messageClone = document.createElement('div');
  messageClone.innerText = text;
  messageClone.style.position = 'fixed';
  messageClone.style.left = `${inputBox.left + inputBox.width / 2}px`;
  messageClone.style.top = `${inputBox.top}px`;
  messageClone.style.transform = 'translate(-50%, -50%)';
  messageClone.style.whiteSpace = 'nowrap';
  messageClone.style.background = 'rgba(255, 255, 255, 0.8)';
  messageClone.style.padding = '5px';
  messageClone.style.borderRadius = '5px';
  document.body.appendChild(messageClone);

  gsap.to(messageClone, {
    x: ballBox.left + ballBox.width / 2 - (inputBox.left + inputBox.width / 2),
    y: ballBox.top + ballBox.height / 2 - inputBox.top,
    scale: 0.2,
    duration: 1,
    ease: 'power2.inOut',
    onComplete: () => {
      document.body.removeChild(messageClone);
      const tl = gsap.timeline();
      tl.to(ball.value, {scale: 1.3, duration: 0.6, ease: 'power1.inOut'})
          .to(ball.value, {scale: 1, duration: 0.6, ease: 'elastic.out(1, 0.4)'})
          .to(ball.value, {backgroundColor: getRandomHarmoniousColor(0), duration: 1});

    }
  });
  return;
};

// 获取和谐颜色
const getRandomHarmoniousColor = (i:number) => {
  const colors = [['#e8cd3c', '#c24a1e', '#e1a941', '#cb533e', '#FF8C00'], ['#1e90ff', '#288cec', '#3289da', '#3c85c7', '#4682b4']];

  return colors[i][Math.floor(Math.random() * 5)];
};

// 为花瓣应用动画
const applyPetalAnimation = (i:number) => {
  if (!ball.value) return; // 确保 ball 已经初始化
  const petals = ball.value.querySelectorAll('.petal');
  petals.forEach((petal, index) => {
    gsap.to(petal, {
      rotation: 360,
      x: 'random(-80, 80)',
      y: 'random(-80, 80)',
      backgroundColor: getRandomHarmoniousColor(i),
      duration: 3,
      repeat: -1,
      yoyo: true,
      ease: 'sine.inOut',
      delay: index * 0.5
    });
  });
};

// 开始综缩的动画
const startScaling = () => {
  if (scalingTween) return; // 如果已经在综缩中，则不重复开始
  scalingTween = gsap.to(ball.value, {
    scale: 1.3,
    repeat: -1,
    yoyo: true,
    duration: 1.,
    ease: 'power1.inOut'
  });
};

// 停止综缩动画
const stopScaling = () => {
  if (scalingTween) {
    scalingTween.kill();
    scalingTween = null;
  }
  gsap.to(ball.value, {
    scale: 1,
    duration: 0.5,
    ease: 'power2.out'
  });
};

// 扩展悬浮球的动画
const expandBall = async () => {
  showPetals.value = false; // 隐藏花瓣
  expandedMessageTip = true; // 显示扩展后的消息
  sendChange(); // 改变样式

  // 等待 DOM 更新，以确保 expandedMessageDiv 可以被访问并渲染
  await nextTick();

  if (expandedMessageDiv.value) {
    // 使用 expandedMessageDiv 获取实际渲染后的高度
    const calculatedHeight = expandedMessageDiv.value.getBoundingClientRect().height;

    // 扩展悬浮球的高度以适应内容
    gsap.to(ball.value, {
      width: '700px',  // 扩展宽度
      height: calculatedHeight +  'px', // 加上一些 padding 以防止内容紧贴边缘
      borderRadius: '20px',
      background: '#FFFFFF',
      duration: 1.5,
      ease: 'power1.inOut',
    });
  }
};

// 监听 expandedMessage 的变化
watch(expandedMessage, () => {
  if (expandedMessageTip) {
    updateBallHeight(); // 当内容更新时，更新悬浮球的高度
  }
});

// 动态更新悬浮球的高度以适应内容
const updateBallHeight = async () => {
  await nextTick(); // 等待 DOM 更新，以确保 expandedMessageDiv 可以被访问

  if (expandedMessageDiv.value) {
    // 创建一个临时的容器用于计算内容的高度
    const tempDiv = document.createElement('div');
    tempDiv.style.position = 'absolute';
    tempDiv.style.width = '200px'; // 使用与悬浮球相同的固定宽度
    tempDiv.style.visibility = 'hidden';
    tempDiv.style.pointerEvents = 'none';
    tempDiv.innerHTML = expandedMessage.value; // 使用 markdown 渲染后的内容

    // 将 tempDiv 添加到 DOM 中以便计算
    document.body.appendChild(tempDiv);

    // 获取临时容器的高度
    let calculatedHeight = tempDiv.getBoundingClientRect().height;

    // 移除临时容器
    document.body.removeChild(tempDiv);

    // 扩展悬浮球的高度以适应内容
    if (calculatedHeight <= 10) calculatedHeight = 10;
    gsap.to(ball.value, {
      width: '500px',
      height: calculatedHeight + 'px', // 加一些 padding 以防止内容紧贴边缘
      borderRadius: '20px',
      backgroundColor: '#FFFFFF',
      duration: 1.5,
      ease: 'power2.inOut'
    });
  }
};

// 恢复悬浮球的动画
const revertBall = async () => {
  showPetals.value = true; // 显示花瓣
  expandedMessageTip = false; // 隐藏扩展的消息
  expandedMessage.value = "";//销毁信息
  await nextTick(); // 等待 DOM 更新

  gsap.to(ball.value, {
    width: '150px',
    height: '150px',
    borderRadius: '50%',
    background: 'radial-gradient(circle at center, rgba(255, 255, 200, 0.8), rgba(255, 140, 0, 0.5)), radial-gradient(circle at center, #FFD700, #FF4500, #FFA500)',
    duration: 1.5,
    ease: 'power1.inOut',
    onComplete: () => {
      applyPetalAnimation(0); // 重新应用花瓣动画
    }
  });
};

// 使用 GSAP 在组件加载时为浮动球和花瓣添加动画
onMounted(() => {
  watch(isBallWobbling, (newValue) => {
    if (newValue) {
      gsap.to(ball.value, {
        y: -30,
        repeat: -1,
        yoyo: true,
        duration: 3,
        ease: 'power1.inOut'
      });
    } else {
      gsap.killTweensOf(ball.value);
      gsap.set(ball.value, {y: 0});
    }
  }, {immediate: true});

  gsap.to(ball.value, {
    boxShadow: '0 0 30px 20px rgba(255, 200, 0, 0.5)',
    repeat: -1,
    yoyo: true,
    duration: 2,
    ease: 'sine.inOut'
  });

  applyPetalAnimation(0); // 初始花瓣动画

});

//获取base url
const stateStore = useStateStore();
let baseURL = ""
onBeforeMount(() => {
  baseURL = stateStore.baseUrl; //先设置成默认url
});

// 临时改变悬浮球颜色
const tempChangeBallColor = () => {
  gsap.to(ball.value, {
    background: 'radial-gradient(circle at center, rgba(173, 216, 230, 0.8), rgba(70, 130, 180, 0.8)), radial-gradient(circle at center, #87CEEB, #4682B4, #1E90FF)', // 设置一个蓝色渐变颜色
    duration: 0.5,
    ease: 'power1.inOut',
    onComplete: () => {
      applyPetalAnimation(1); // 重新应用花瓣动画
    }
  });

};

//删除信息
import {ElMessageBox} from 'element-plus';

const handleDoubleClick = (index: number) => {
  // 弹出确认框
  ElMessageBox.confirm('Are you sure you want to delete this question?', 'Delete Confirmation', {
    confirmButtonText: 'Yes',
    cancelButtonText: 'No',
    type: 'warning'
  }).then(() => {
    // 如果用户点击确认，删除对应的 ask
    asks.value.splice(index, 1);
    // 清空显示的 ai 回复
    showHTML.value = '';
  }).catch(() => {
    // 如果用户点击取消，什么都不做
    console.log('Deletion cancelled');
  });
};

//发送按钮的逻辑
let sendIcon = ref(Promotion);
let sendColor = ref('success')
const sendNormal = () => {
  sendIcon.value = Promotion;
  sendColor.value = 'success'
}

const sendChange = () => {
  sendIcon.value = Close;
  sendColor.value = 'warning'
}


//文件按钮的逻辑
let fileIcon = ref(Picture);
let fileColor = ref('primary')
const fileNormal = () => {
  fileIcon.value = Picture;
  fileColor.value = 'primary'
}

const fileDelete = () => {
  fileIcon.value = Delete;
  fileColor.value = 'danger'
}


// 响应式数据，存储图片的 URL
const imageUrl = ref('');

// 使用 ref 获取文件输入框
const fileInput = ref(null);

// 手动触发文件选择框
const triggerFileInput = () => {
  // 如果有img就删除
  if (imageUrl.value) {
    imageUrl.value = "";
    fileNormal();
    return;
  }
  fileInput.value.click(); // 触发隐藏的文件输入框
};

// 处理文件选择
const onFileChange = (event) => {
  const file = event.target.files[0]; // 获取选中的文件
  if (file) {
    const reader = new FileReader(); // 创建 FileReader 实例
    reader.onload = (e) => {
      imageUrl.value = e.target.result; // 图片读取完成后设置 imageUrl 为文件内容（base64 编码）
      fileDelete();
      console.log(imageUrl.value);
    };
    reader.readAsDataURL(file); // 将文件读取为 Data URL（base64 编码）

    // 重置文件输入框的值，这样即使选择相同的文件也能触发 change 事件
    event.target.value = '';
  }
};

//回车发送
const handleKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Enter') {
    sendToModel();
  }
};

//悬浮窗激活
function openFloating() {

  window.electronAPI.openFloatingWindow();
  console.log("已按下");
}

</script>
<style scoped>
.chat-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start; /* 调整为 flex-start，使内容向上对齐 */
  height: 100vh;
  padding: 180px 20px 20px; /* 减小顶部的 padding，使内容向上移动 */
  background-color: #8fefdd;
}

/* 其他样式保持不变 */


/* 悬浮球样式 */
.float-ball {
  width: 150px; /* 固定宽度 */
  height: 150px;
  border-radius: 50%;
  background: radial-gradient(circle at center, rgba(255, 255, 200, 0.8), rgba(255, 140, 0, 0.5)), radial-gradient(circle at center, #FFD700, #FF4500, #FFA500);
  margin: 50px auto;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.3);
  position: relative;
  overflow-y: scroll;
  scrollbar-width: none;  /* 隐藏滚动条 */
}

.past-info {
  display: flex;
  flex-wrap: wrap;
  max-width: 80%;
  margin-top: 10px;
  gap: 10px;
  overflow-y: hidden;
  max-height: 200px;
}

/* 输入框容器 */
.input-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 600px;
  padding: 10px;
  border-radius: 20px;
  background-color: #f5f5f5;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-top: 10px;
}

.message-input {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 20px;
  font-size: 16px;
  outline: none;
  background-color: transparent;
}

.question-bubble {
  padding: 8px 15px;
  background-color: #e0f7fa;
  border-radius: 10px;
  cursor: pointer;
}

.dropdown-button {
  margin-left: 8px;
}

.petal {
  width: 40px;
  height: 40px;
  background: rgba(255, 200, 0, 0.6);
  border-radius: 50%;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.expanded-message {
  color: #000;
  text-align: left;
  padding: 20px; /* 加入一些内边距 */
  font-size: 1.2em;
}

.markdown-body {
  box-sizing: border-box;
  min-width: 200px;
  max-width: 980px;
  margin: 0 auto;
  padding: 15px;
  width: 700px;
}

@media (max-width: 767px) {
  .markdown-body {
    padding: 15px;
  }
}

img {
  margin-top: 10px;
  width: 80px; /* 固定宽度 */
  height: auto; /* 保持比例 */
  margin-left: 10px;
  border-radius: 20px;
  margin-right: 10px;
}


</style>