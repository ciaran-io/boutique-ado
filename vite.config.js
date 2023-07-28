import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  root: resolve('./static/assets'),
  base: '/static/',

  build: {
    manifest: true,
    outDir: resolve('./static/dist'),
    assetsDir: '',
    rollupOptions: {
      input: {
        main: resolve('./static/assets/js/main.js'),
        stripe: resolve('./static/assets/js/stripe.js'),
        cssImport: resolve('./static/assets/js/css-import.js'),
      },
    },
    css: {
      postcss: './postcss.config.js',
    },
  },
})