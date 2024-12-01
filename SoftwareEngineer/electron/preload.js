const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    openFloatingWindow: () => {
        console.log("已收到");
        ipcRenderer.send('open-floating-window')},
    closeFloatingWindow: () => ipcRenderer.send('close-floating-window'),
    resizeFloatingWindow: (width, height) => ipcRenderer.send('resize-floating-window', width, height)
});

