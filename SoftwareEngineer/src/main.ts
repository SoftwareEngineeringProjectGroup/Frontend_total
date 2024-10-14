// import './style.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import axios from 'axios'
// import VueAxios from 'vue-axios'
import router from './router/index.js'


axios.defaults.baseURL = 'http://127.0.0.1:5000/api';

const app = createApp(App)
app.use(ElementPlus, { size: 'small', zIndex: 3000 })
app.use(router)
app.use(createPinia())
// app.use(VueAxios, axios)
app.config.globalProperties.$axios = axios
app.mount('#app')