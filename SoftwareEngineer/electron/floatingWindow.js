const { BrowserWindow, ipcMain } = require('electron');
const path = require('path');

let floatingWindow;

function createFloatingWindow() {
    floatingWindow = new BrowserWindow({
        width: 400,
        height: 1000,
        frame: false,
        alwaysOnTop: true,
        transparent:true,

        webPreferences: {
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js'), // 使用 preload.js
        },
    });

    floatingWindow.loadFile('./dist/index.html').then(() => {
        floatingWindow.webContents.executeJavaScript(`
            window.location.hash = '#/floating';
        `);
    });
    // floatingWindow.webContents.openDevTools({ mode: 'detach' });

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
