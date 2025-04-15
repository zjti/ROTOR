import { reactive,  } from 'vue'
import { useStorage,watchTriggerable } from '@vueuse/core'
import usePyodide from '@/composables/usePyodide';
const { runPythonS } = usePyodide();

import params_soil from "../assets/params/params_soil.json";
import CdelayData from "../assets/cross_breaks.json";
import CdelayData_time from "../assets/cross_breaks_time.json";
import verkrautung from "../assets/params/verkraut.json";
import params_dung from "../assets/params/params_dung.json";

import Verkraut from '../components/settings/verkraut.vue';

const verkraut = useStorage('VERKRAUTUNG',verkrautung)
const psoil = useStorage('PARAMS_SOIL',params_soil)
const pdt =  useStorage('PHYTO_DELAY_TIME',CdelayData_time)
const pd =  useStorage('PHYTO_DELAY',CdelayData)
const pdung =  useStorage('PARAMS_DUNG',params_dung)


export const globalStore = reactive({
  SOIL : psoil,
  PHYTO_DELAY_TIME:pdt,
  PHYTO_DELAY:pd,
  VERKRAUTUNG:verkraut,
  DUNG_DATA:pdung
})

const { trigger, ignoreUpdates } = watchTriggerable(
  psoil,
  (newVal) => {
     ignoreUpdates(() => {
    
    console.log('update soil')
    runPythonS('config.SOIL = json.loads("""'+ JSON.stringify( newVal) +'""")' )
 
    })
  },{ deep: true }
)

{
const { trigger, ignoreUpdates } = watchTriggerable(
  pdt,
  (newVal) => {
     ignoreUpdates(() => {
    
    console.log('update pdt ')
    runPythonS('config.PHYTO_DELAY_TIME = json.loads("""'+ JSON.stringify( newVal) +'""")' )
 
    })
  },{ deep: true }
)
}
