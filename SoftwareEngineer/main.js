import { createRequire } from 'module';
const require = createRequire(import.meta.url);


const { app, BrowserWindow } = require('electron')

process.env['ELECTRON_DISABLE_SECURITY_WARNINGS'] = 'true';


const createWindow = () => {
    const win = new BrowserWindow({
        width: 800,
        height: 600
    })

    // win.loadFile('index.html')

    // 下面的url为自己启动vite项目的url。
    win.loadURL('http://localhost:5173/')
    // 打开electron的开发者工具
    win.webContents.openDevTools({ mode: 'detach' })
}

app.whenReady().then(() => {
    app.commandLine.appendSwitch('ignore-certificate-errors')
    createWindow()
    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow()
    })
})

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})
