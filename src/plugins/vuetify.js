/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'


import 'leaflet/dist/leaflet.css';

// Composables
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

 


const myCustomLightTheme = {
  dark: false,
  
  colors: {
    foreground: '#0FF',

    'on-background': '#000000',
    'on-surface': '#000000',
    'on-surface-light-1': '#000000',
    'on-surface-variant': '#00FF00',



    background: '#aaFFaa',
    surface: '#EFE',//'#669966',
    'surface-bright': '669966',//'#FFFFFF',
    'surface-light': '#00F',//'#EEEEEE',
    'surface-variant': '#c2c2c2',
    'on-surface-variant': '#111',
    primary: '#338833',//'#18cc0A',
    'primary-light-1': '#000000',//'#18cc0A',
    'primary-darken-1': '#FF0000',//'#1F5592',
    secondary: '#00FFFF',// '#48A9A6',
    'secondary-darken-1': '#00FFFF',
    error: '#B00020',
    info: '#400',//'#2196F3',
    success: '#400',// '#4CAF50',
    warning: '#A80',
  },
  variables: {
    // 'primary--text': '#FF00FF',
    'border-color': '#000000',
    'border-opacity': 0.12,
    'high-emphasis-opacity': 0.87,
    'medium-emphasis-opacity': 1.0,
    'disabled-opacity': 0.38,
    'idle-opacity': 0.04,
    'hover-opacity': 0.04,
    'focus-opacity': 0.12,
    'selected-opacity': 0.08,
    'activated-opacity': 0.12,
    'pressed-opacity': 0.12,
    'dragged-opacity': 0.08,
    'theme-kbd': '#212529',
    'theme-on-kbd': '#FFFFFF',
    'theme-code': '#FF00F5',
    'theme-on-code': '#000000',
  }
}

import { de } from 'vuetify/locale'


export default createVuetify({
  theme: {
    defaultTheme: 'myCustomLightTheme',
    themes: {
      myCustomLightTheme,
    },
  },
  lang: {
    locales: { de },
    current: 'de'
  }, 
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
  defaults: {
    global: {
      style: {
        fontFamily: 'Roboto, sans-serif',
      },
    },
  },
})

