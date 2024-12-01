import { createRouter, createWebHashHistory } from 'vue-router';

// 路由组件
import Home from '@/views/Home.vue';
import Chat from '@/views/Chat.vue';
import Information from '@/views/Information.vue';
import Programming from '@/views/Programming.vue';
import Dietitian from '@/views/Dietitian.vue';
import Setting from '@/views/Setting.vue';
import Floating from "@/views/Floating.vue";
import Intro from "@/views/Intro.vue";
import Feedback from "@/views/Feedback.vue";

const routes = [
    { path: '/', name: 'Home', component: Home, meta: { title: 'Lambda' } },
    { path: '/chat', name: 'Chat', component: Chat, meta: { title: 'Chat' } },
    { path: '/information', name: 'Information', component: Information, meta: { title: 'Info' } },
    { path: '/programming', name: 'Programming', component: Programming, meta: { title: 'Programming Assistant' } },
    { path: '/dietitian', name: 'DietitianIntro', component: Intro, meta: { title: 'Dietitian Intro' } },
    { path: '/dietitian/main', name: 'DietitianMain', component: Dietitian, meta: { title: 'Nutritionist' } },
    { path: '/setting', name: 'Setting', component: Setting, meta: { title: 'Settings' } },
    { path: '/floating', name: 'Floating', component: Floating, meta: { title: 'Floating Window' } },
    { path: '/feedback', name: 'Feedback', component: Feedback, meta: { title: 'Feedback' } },
];

const router = createRouter({
    history: createWebHashHistory(), // Using Hash mode
    routes,
});

// 动态设置页面标题
router.beforeEach((to, from, next) => {
    if (to.meta.title) {
        document.title = to.meta.title; // 设置页面标题
    }
    next();
});

export default router;
