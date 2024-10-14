import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
// 按需导入element-plus的更多组件
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import {fileURLToPath, URL} from "node:url";


export default defineConfig({
  plugins: [
    vue(),
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver()],
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'static',
    assetsInlineLimit: 4096, // 配置资源内联的大小限制
    rollupOptions: {
      output: {
        assetFileNames: 'static/[name].[hash][extname]', // 资源文件的输出路径和命名规则
      },
    },
    sourcemap: false, // 生产环境是否生成 source map 文件
  }
})