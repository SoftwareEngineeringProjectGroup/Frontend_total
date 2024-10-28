const { contextBridge, ipcRenderer } = require('electron');
const fs = require('fs');
const path = require('path');

contextBridge.exposeInMainWorld('electron', {
    saveFile: (filePath, data) => {
        fs.writeFile(filePath, data, (err) => {
            if (err) {
                console.error('保存文件失败:', err);
            } else {
                console.log('文件保存成功:', filePath);
            }
        });
    },
    pathJoin: (...args) => path.join(...args)
});
