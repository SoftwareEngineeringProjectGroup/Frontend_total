import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
// 按需导入element-plus的更多组件
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'



export default defineConfig({
  plugins: [vue(),
    // 打补丁
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver()],
    })
  ]
})


