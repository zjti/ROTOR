// Plugins
import Components from 'unplugin-vue-components/vite'
import Vue from '@vitejs/plugin-vue'
import Vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'
import ViteFonts from 'unplugin-fonts/vite'

// Utilities
import { defineConfig } from 'vite'
import { fileURLToPath, URL } from 'node:url'

// https://vitejs.dev/config/
 

export default defineConfig({
  build: {
    target: 'esnext'
  },
  base:'/ROTOR/',
  plugins: [ 
    Vue({
      template: { transformAssetUrls }
    }),
    // https://github.com/vuetifyjs/vuetify-loader/tree/master/packages/vite-plugin#readme
    Vuetify(),
    Components(),
    // ViteFonts({
    //   google: {
    //     families: [{
    //       name: 'Roboto',
    //       styles: 'wght@100;300;400;500;700;900',
    //     }],
    //   },
    // }),
    ViteFonts({
      google: {
        families: [
          {
            name: 'Roboto',
            styles: 'wght@100;300;400;500;700;900',
            defer: false,             // Optional: inject in <head> immediately
            display: 'swap',          // Prevent invisible text during load
            preconnect: false,        // Don't try to preconnect to fonts.googleapis.com
          },
        ],
        // Self-host the fonts!
        download: true,
        injectTo: 'head',            // Inject <style> into <head>
      },
    }),
  ],
  define: { 'process.env': {} },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
    extensions: [
      '.js',
      '.json',
      '.jsx',
      '.mjs',
      '.ts',
      '.tsx',
      '.vue',
    ],
  },
  server: {
    port: 3000,
  },
})