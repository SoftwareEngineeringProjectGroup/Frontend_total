const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    openFloatingWindow: () => {
        console.log("已收到");
        ipcRenderer.send('open-floating-window')}
});

