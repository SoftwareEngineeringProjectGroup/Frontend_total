import { createRouter, createWebHistory } from 'vue-router'

// 路由组件
import Home from '@/views/Home.vue'
import Chat from '@/views/Chat.vue'
import Information from '@/views/Information.vue'
import Programming from '@/views/Programming.vue'
import Dietitian from '@/views/Dietitian.vue'
import Setting from '@/views/Setting.vue'

const routes = [
    { path: '/', name: 'Home', component: Home },
    { path: '/chat', name: 'Chat', component: Chat },
    { path: '/information', name: 'Information', component: Information },
    { path: '/programming', name: 'Programming', component: Programming },
    { path: '/dietitian', name: 'Dietitian', component: Dietitian },
    { path: '/setting', name: 'Setting', component: Setting },
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
})

export default router
