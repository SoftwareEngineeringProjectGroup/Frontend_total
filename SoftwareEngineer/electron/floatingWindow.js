const { BrowserWindow, ipcMain } = require('electron');
const path = require('path');

let floatingWindow;

function createFloatingWindow() {
    floatingWindow = new BrowserWindow({
        width: 200,
        height: 200,
        frame: false,
        alwaysOnTop: true,
        transparent: true,
        webPreferences: {
            contextIsolation: true,
            nodeIntegration: false,
        },
    });

    // 加载 Vue 打包后的 HTML 文件，并导航到悬浮窗口的特定路由
    floatingWindow.loadFile('./dist/index.html').then(() => {
        floatingWindow.webContents.executeJavaScript(`
            window.location.hash = '#/floating';
        `);
    });

    return floatingWindow;
}

// 监听渲染进程发来的消息，创建悬浮窗口
function handleFloatingWindowEvents() {
    ipcMain.on('open-floating-window', () => {
        console.log('Main process received request to open floating window.');
        if (!floatingWindow) {
            createFloatingWindow();
        }
    });
}

module.exports = { createFloatingWindow, handleFloatingWindowEvents };
