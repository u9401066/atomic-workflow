import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: resolve(__dirname, '..', 'dist', 'webview'),
    emptyOutDir: true,
    rollupOptions: {
      input: resolve(__dirname, 'src', 'main.tsx'),
      output: {
        entryFileNames: 'index.js',
        assetFileNames: 'index.[ext]',
        // Single chunk for webview simplicity
        manualChunks: undefined,
      },
    },
    // Webview needs a single self-contained bundle
    cssCodeSplit: false,
    sourcemap: true,
  },
  define: {
    'process.env.NODE_ENV': JSON.stringify('production'),
  },
});
