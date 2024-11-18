const { app, BrowserWindow, ipcMain, Menu, globalShortcut } = require('electron');
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

    // 清除缓存以避免相关错误
    mainWindow.webContents.session.clearCache();

    // 禁用 GPU 加速以解决 GPU 缓存问题
    app.commandLine.appendSwitch('disable-gpu');
    app.commandLine.appendSwitch('disable-software-rasterizer');

    // 注册快捷键：Ctrl + 加号进行放大
    globalShortcut.register('Control+=', () => {
        let currentZoom = mainWindow.webContents.getZoomFactor();
        mainWindow.webContents.setZoomFactor(currentZoom + 0.1);  // 每次放大 0.1
    });

    // 注册快捷键：Ctrl + 减号进行缩小
    globalShortcut.register('Control+-', () => {
        let currentZoom = mainWindow.webContents.getZoomFactor();
        mainWindow.webContents.setZoomFactor(currentZoom - 0.1);  // 每次缩小 0.1
    });

    // 如果需要，可以打开开发者工具
    mainWindow.webContents.openDevTools({ mode: 'detach' });
};

// 创建悬浮窗的函数
let floatingWindow;
const createFloatingWindow = () => {
    floatingWindow = new BrowserWindow({
        width: 200,
        height: 200,
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
    app.setPath('userData', path.join(__dirname, 'userData')); // 自定义缓存目录，避免权限问题
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
