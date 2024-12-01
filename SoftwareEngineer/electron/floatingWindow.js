const { BrowserWindow, ipcMain } = require('electron');
const path = require('path');

let floatingWindow = null;  // 用变量存储窗口实例

function createFloatingWindow() {
    // 检查是否已经存在悬浮窗口，如果存在，直接返回该窗口
    if (floatingWindow) {
        floatingWindow.show(); // 如果窗口已经存在，直接显示窗口
        return floatingWindow;
    }

    // 如果窗口不存在，创建新的窗口
    floatingWindow = new BrowserWindow({
        width: 390,
        height: 85,
        frame: false, // 无边框
        alwaysOnTop: true, // 总是在最上层
        transparent: true, // 透明背景
        webPreferences: {
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js'), // 使用 preload.js
        },
    });

    // 加载 Vue 打包后的页面
    floatingWindow.loadFile('./dist/index.html').then(() => {
        floatingWindow.webContents.executeJavaScript(`
            window.location.hash = '#/floating';
        `);
    });

    // 监听窗口关闭事件，防止窗口关闭时被销毁
    floatingWindow.on('closed', () => {
        floatingWindow = null;  // 窗口关闭时，释放窗口引用
    });

    return floatingWindow;
}

// 监听渲染进程发来的消息，创建或显示悬浮窗口
function handleFloatingWindowEvents() {
    ipcMain.on('open-floating-window', () => {
        console.log('Main process received request to open floating window.');
        createFloatingWindow(); // 调用创建悬浮窗口的函数
    });

    ipcMain.on('close-floating-window', () => {
        if (floatingWindow) {
            floatingWindow.hide(); // 隐藏窗口
        }
    });

    ipcMain.on('resize-floating-window', (event, width, height) => {
        if (floatingWindow) {
            floatingWindow.setSize(width, height); // 调整悬浮窗口大小
        }
    });
}

module.exports = { createFloatingWindow, handleFloatingWindowEvents };
