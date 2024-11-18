// src/stores/stateStore.ts
import {defineStore} from 'pinia';

export const useStateStore = defineStore('state', {
    state: () => ({
        isOpenValue: 0, //状态栏是否收缩
        userImagePath: "./static/userDefault.jpg", // 存储用户图片路径sta
        aiImagePath: "./static/aiDefault.jpg", // 存储ai图片路径
        audioType: 'D', // 音频类型
        baseUrl: "http://127.0.0.1:8000",//IPv4地址
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
        setaudioType(newValue: string) {
            this.audioType = newValue;
        },
        setbaseUrl(newValue: string) {
            this.baseUrl = newValue;
        },
    },
});

