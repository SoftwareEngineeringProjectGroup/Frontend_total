import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import ElementPlus from 'element-plus' // 引入模块
import 'element-plus/dist/index.css' // 引入css

const app = createApp(App)
app.use(ElementPlus) // 添加到中间件



app.mount('#app')
