// src/stores/stateStore.ts
import {defineStore} from 'pinia';

export const useStateStore = defineStore('state', {
    state: () => ({
        isOpenValue: 0, //状态栏是否收缩
        userImagePath: "./static/userDefault.jpg", // 存储用户图片路径sta
        aiImagePath: "./static/aiDefault.jpg", // 存储ai图片路径
        audioType: 'D', // 音频类型
        baseUrl: "http://10.252.130.135:8000",//IPv4地址
        chatHistory:[],
        infoHistory:[],
        isPlayed: false, //检测是否已经播放过介绍页面
        gender: "male",//性别
        personalPrompt: "",//个人prompt
        isShow: true//演示模式
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
        setisPlayed(newValue: boolean) {
            this.isPlayed = newValue;
        },
        setGender(newValue: string) {
            this.gender = newValue;
        },
        setPersonalPrompt(newValue: string) {
            this.personalPrompt = newValue
        },
        setIsShow(newValue: boolean) {
            this.isShow = newValue
        },
        setChatHistory(newValue: []) {
            this.chatHistory = newValue
        },
        setInfoHistory(newValue: []) {
            this.infoHistory = newValue
        },

    },
});

