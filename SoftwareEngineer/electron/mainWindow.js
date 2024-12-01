const { BrowserWindow, globalShortcut } = require('electron');
const path = require('path');

let mainWindow;
let zoomFactor = 1; // 初始化缩放比例

function createMainWindow() {
    mainWindow = new BrowserWindow({
        width: 1000,
        height: 800,
        webPreferences: {
            contextIsolation: true,
            sandbox: false,
            nodeIntegration: true,
            additionalArguments: ['--enable-speech-dispatcher'],
            preload: path.join(__dirname, 'preload.js'), // 添加 preload.js
        },
    });

    // 加载 Vue 打包后的 HTML 文件
    mainWindow.loadFile('./dist/index.html');

    // 清除缓存以避免相关错误
    mainWindow.webContents.session.clearCache();

    // 注册刷新页面快捷键
    globalShortcut.register('CommandOrControl+R', () => {
        mainWindow.webContents.reload(); // 刷新当前页面
    });

    // 注册全局快捷键实现页面内容缩放
    globalShortcut.register('CommandOrControl+1', () => {
        zoomFactor += 0.1;
        if (zoomFactor > 3) zoomFactor = 3; // 最大缩放限制
        mainWindow.webContents.setZoomFactor(zoomFactor);
    });

    globalShortcut.register('CommandOrControl+2', () => {
        zoomFactor -= 0.1;
        if (zoomFactor < 0.5) zoomFactor = 0.5; // 最小缩放限制
        mainWindow.webContents.setZoomFactor(zoomFactor);
    });

    globalShortcut.register('CommandOrControl+0', () => {
        zoomFactor = 1;
        mainWindow.webContents.setZoomFactor(zoomFactor);
    });

    // 如果需要，可以打开开发者工具
    // mainWindow.webContents.openDevTools({ mode: 'detach' });

    return mainWindow;
}

module.exports = { createMainWindow };
