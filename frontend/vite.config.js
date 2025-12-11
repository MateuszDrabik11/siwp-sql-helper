import { fileURLToPath, URL } from 'node:url'
import { defineConfig, loadEnv} from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import path from 'node:path'
const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
export default defineConfig(({ mode }) => {
    const env = loadEnv(mode, process.cwd(), '')
    return {
  plugins: [
    vue(),
    vueDevTools(),
  ],
  server: {
    proxy: {
        '/api': {
            target: env.VITE_API_TARGET, // Your backend URL
            changeOrigin: true,
            rewrite: (p) => p.replace(/^\/api/, ''), // Optional: remove /api prefix
        }
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    },
  },
}}
)
