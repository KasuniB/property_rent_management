import { defineConfig } from 'vite';
import path from 'path';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  build: {
    outDir: 'public/dist',
    emptyOutDir: true,
    lib: {
      entry: {
        'property_rent_management': path.resolve(__dirname, 'public/js/property_rent_management.js'),
      },
      formats: ['iife'],
      name: 'PropertyRentManagement'
    },
    rollupOptions: {
      output: {
        entryFileNames: '[name].bundle.js',
        assetFileNames: '[name].bundle.[ext]'
      }
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'public/js')
    }
  }
});