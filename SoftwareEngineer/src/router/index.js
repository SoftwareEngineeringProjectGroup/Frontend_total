import { createRouter, createWebHashHistory } from 'vue-router';

// 路由组件
import Home from '@/views/Home.vue';
import Chat from '@/views/Chat.vue';
import Information from '@/views/Information.vue';
import Programming from '@/views/Programming.vue';
import Dietitian from '@/views/Dietitian.vue';
import Setting from '@/views/Setting.vue';
import Floating from "@/views/Floating.vue";

const routes = [
    { path: '/', name: 'Home', component: Home },
    { path: '/chat', name: 'Chat', component: Chat },
    { path: '/information', name: 'Information', component: Information },
    { path: '/programming', name: 'Programming', component: Programming },
    { path: '/dietitian', name: 'Dietitian', component: Dietitian },
    { path: '/setting', name: 'Setting', component: Setting },
    { path: '/floating', name: 'Floating', component: Floating },
];

const router = createRouter({
    history: createWebHashHistory(), // 改为 Hash 模式
    routes,
});

export default router;
