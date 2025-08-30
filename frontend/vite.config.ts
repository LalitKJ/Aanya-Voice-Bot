import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vite.dev/config/
export default defineConfig(
  ({ mode }) => {
    const env = loadEnv(mode, process.cwd(), 'VITE_SERVER_URL');
    const serverUrl = env.VITE_SERVER_URL;
    return {
      plugins: [react()],
      server: {
        proxy: {
          '/api': {
            target: serverUrl,
            changeOrigin: true,
            ws: true,
            rewrite: (path) => path.replace(/^\/api/, ''),
          }
        },
      }
    }
  }
)
