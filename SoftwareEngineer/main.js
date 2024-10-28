// electron用的
import { createRequire } from 'module';
const require = createRequire(import.meta.url);

const { app, BrowserWindow } = require('electron')
const path = require('path');

process.env['ELECTRON_DISABLE_SECURITY_WARNINGS'] = 'true';

let mainWindow;
let miniWindow;

const createWindow = () => {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,

        webPreferences: {
            contextIsolation: false,
            sandbox:false,
            nodeIntegration: true,
            additionalArguments: ['--enable-speech-dispatcher'],
        }
    });

    // 监听窗口的最小化事件
    mainWindow.on('minimize', (event) => {
        event.preventDefault(); // 阻止窗口真正最小化
        mainWindow.hide(); // 隐藏主窗口
        createMiniWindow(); // 创建悬浮窗口
    });

    // 下面的url为自己启动vite项目的url
    mainWindow.loadURL('http://localhost:5173/');
    // 打开electron的开发者工具
    mainWindow.webContents.openDevTools({ mode: 'detach' });
}

const createMiniWindow = () => {
    miniWindow = new BrowserWindow({
        width: 200,
        height: 100,
        frame: false, // 无边框窗口
        alwaysOnTop: true, // 保持窗口在最上层
        skipTaskbar: true, // 从任务栏隐藏
        transparent: true, // 窗口透明
        webPreferences: {
            contextIsolation: true,
            nodeIntegration: false,
            additionalArguments: ['--enable-speech-dispatcher'],
        }
    });

    // 加载 Vue 开发服务器的悬浮窗口页面
    miniWindow.loadURL('http://localhost:5173/information');

    miniWindow.on('closed', () => {
        miniWindow = null;
    });
};


// Electron app 事件处理
app.whenReady().then(() => {
    app.commandLine.appendSwitch('ignore-certificate-errors');
    app.commandLine.appendSwitch('enable-speech-dispatcher'); // 启用语音识别支持
    createWindow();

    // 响应主窗口恢复事件
    const { ipcMain } = require('electron');
    ipcMain.on('restore-window', () => {
        if (mainWindow) {
            mainWindow.show(); // 恢复主窗口
            if (miniWindow) miniWindow.close(); // 关闭悬浮窗口
        }
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

