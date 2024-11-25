const { app, Menu, ipcMain } = require('electron');
const path = require('path');
const { createMainWindow } = require('./mainWindow');
const { createFloatingWindow, handleFloatingWindowEvents } = require('./floatingWindow');

process.env['ELECTRON_DISABLE_SECURITY_WARNINGS'] = 'true';

// 禁用菜单栏
Menu.setApplicationMenu(null);

app.whenReady().then(() => {
    app.commandLine.appendSwitch('ignore-certificate-errors');
    app.commandLine.appendSwitch('enable-speech-dispatcher'); // 启用语音识别支持
    app.setPath('userData', path.join(__dirname, 'userData')); // 自定义缓存目录，避免权限问题

    // 创建主窗口
    const mainWindow = createMainWindow();

    // 监听悬浮窗口相关的事件
    handleFloatingWindowEvents();

    app.on('activate', () => {
        if (mainWindow === null) createMainWindow();
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});
