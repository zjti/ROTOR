/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */
import 'leaflet/dist/leaflet.css';
import './assets/fonts/roboto/roboto.css';




// Plugins
import { registerPlugins } from '@/plugins'


// Components
import App from './App.vue'
import { useStorage } from '@vueuse/core'


// Composables
import { createApp,ref } from 'vue'

const app = createApp(App)

import lang_de_def from './assets/lang_de.json'
import lang_en_def from './assets/lang_en.json'

// export const lang_de = useStorage('LANG', lang_de_def) 
// export const lang_en = useStorage('LANG_EN', lang_en_def) 

export const lang_de = useStorage('CUSTOM_LANG_DE',false).value==true ? useStorage('LANG_DE', lang_de_def)  : ref( lang_de_def) 
export const lang_en =ref( lang_en_def) 

app.config.globalProperties.cur_lang = ref("de")

export function langf(x,cur_lang){
    if (!cur_lang){
        cur_lang = app.config.globalProperties.cur_lang.value
    }
    if ( cur_lang == "de" ){ 
        if (x in lang_de.value){
            return    lang_de.value[x];
        }
    }
    if ( cur_lang == "en" ){ 
        if (x in lang_en.value){
            return    lang_en.value[x];
        }
    }
    
    return x + ".";
}

export function langf_set(k,v){
    console.log(lang)
    lang_de.value[k]=v
}

export function get_lang(){
    return app.config.globalProperties.cur_lang.value;
}

app.config.globalProperties.L = langf 

console.log('DONE: setup for langf (language-function) ')

registerPlugins(app)
app.mount('#app')
