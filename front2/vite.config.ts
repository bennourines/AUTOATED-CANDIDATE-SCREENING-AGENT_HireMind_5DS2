import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      'figma:asset/546a4a954d15091706c425f397a221b3336468dd.png': path.resolve(__dirname, './src/assets/546a4a954d15091706c425f397a221b3336468dd.png')
    }
  },
  server: {
    port: 3000
  }
})
