// const axios = require('axios');
// const fs = require('fs');
// const path = require('path');
//
// async downloadAndSaveFile() {
//     try {
//         // 向 Django 后端请求生成的 Python 文件
//         const response = await axios({
//             url: 'http://<后端IP>:<端口>/generate-bubble-sort/', // 替换为后端 API 地址
//             method: 'GET',
//             responseType: 'blob' // 让响应以二进制数据（Blob）形式返回
//         });
//
//         // 使用 preload.js 中暴露的 pathJoin 来构建保存路径
//         const savePath = window.electron.pathJoin('D:', 'SPSS', 'bubble_sort.py');
//
//         // 将响应中的数据保存到本地文件
//         window.electron.saveFile(savePath, response.data);
//     } catch (error) {
//         console.error('下载文件失败:', error);
//     }
// }
//
// // 调用该方法来下载并保存文件
// downloadAndSaveFile();
