import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        index: 'index.html',
        app: 'logic-ui.html'
      }
    }
  }
});