// src/stores/stateStore.ts
import { defineStore } from 'pinia';

export const useStateStore = defineStore('state', {
    state: () => ({
        isOpenValue: 0, //状态栏是否收缩
        userImagePath: "/static/userDefault.jpg", // 存储用户图片路径
        aiImagePath: "/static/aiDefault.jpg", // 存储ai图片路径
    }),
    actions: {
        setisOpenValue(newValue: number) {
            this.isOpenValue = newValue;
        },
        setuserImagePath(newValue: string) {
            this.userImagePath = newValue;
        },
        setaiImagePath(newValue: string) {
            this.aiImagePath = newValue;
        },
    },
});

