const { app, BrowserWindow, ipcMain, Menu } = require('electron');
const path = require('path');

process.env['ELECTRON_DISABLE_SECURITY_WARNINGS'] = 'true';

let mainWindow;
// 禁用默认菜单栏
Menu.setApplicationMenu(null);

const createWindow = () => {
    mainWindow = new BrowserWindow({
        width: 1000,
        height: 800,
        webPreferences: {
            contextIsolation: true,
            sandbox: false,
            nodeIntegration: true,
            additionalArguments: ['--enable-speech-dispatcher'],
            preload: path.join(__dirname, 'preload.js') // 添加 preload.js
        }
    });

    // 加载本地 HTML 文件
    mainWindow.loadFile('./dist/index.html');

    // 如果需要，可以打开开发者工具
    mainWindow.webContents.openDevTools({ mode: 'detach' });
};

// 创建悬浮窗的函数
let floatingWindow;
const createFloatingWindow = () => {
    floatingWindow = new BrowserWindow({
        width: 400,
        height: 300,
        frame: false,
        alwaysOnTop: true,
        transparent: true,
        webPreferences: {
            contextIsolation: true,
            nodeIntegration: false
        }
    });
    floatingWindow.loadFile('./dist/index.html').then(() => {
        floatingWindow.webContents.executeJavaScript(`
    window.location.hash = '#/floating';
  `);
    });
};

// Electron app 事件处理
app.whenReady().then(() => {
    app.commandLine.appendSwitch('ignore-certificate-errors');
    app.commandLine.appendSwitch('enable-speech-dispatcher'); // 启用语音识别支持
    createWindow();

    // 响应 Vue 渲染进程的请求，创建悬浮窗
    ipcMain.on('open-floating-window', () => {
        console.log("main也收到");
        createFloatingWindow();
    });

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
