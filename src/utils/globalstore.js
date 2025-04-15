import { reactive, } from 'vue'
import { useStorage, watchTriggerable } from '@vueuse/core'
import usePyodide from '@/composables/usePyodide';
const { runPython, runPythonS, isLoading,initializePyodide } = usePyodide();

import params_soil from "../assets/params/params_soil.json";
import CdelayData from "../assets/cross_breaks.json";
import CdelayData_time from "../assets/cross_breaks_time.json";
import verkrautung from "../assets/params/verkraut.json";
import params_dung from "../assets/params/params_dung.json";
import weather_data from "../assets/params/wd.json";


const verkraut = useStorage('VERKRAUTUNG', verkrautung)
const psoil = useStorage('PARAMS_SOIL', params_soil)
const pdt = useStorage('PHYTO_DELAY_TIME', CdelayData_time)
const pd = useStorage('PHYTO_DELAY', CdelayData)
const pdung = useStorage('PARAMS_DUNG', params_dung)
const ff = useStorage('FF', {})



export const globalStore = new Map();
globalStore.set('SOIL', psoil)
globalStore.set('PHYTO_DELAY_TIME', pdt)
globalStore.set('PHYTO_DELAY', pd)
globalStore.set('VERKRAUTUNG', verkraut)
globalStore.set('DUNG_DATA', pdung)
globalStore.set('FF', ff)

await initializePyodide();
  

await runPython('config.WEATHER_DATA = json.loads("""'+ JSON.stringify( weather_data) +'""")' )


{
  const { trigger, ignoreUpdates } = watchTriggerable(
    globalStore.get('SOIL'),
    (newVal) => {
      ignoreUpdates(  () => {
          runPythonS('config.SOIL = json.loads("""' + JSON.stringify(newVal) + '""")')
      })
    }, { deep: true }
  )
  trigger()
}

{
  const { trigger, ignoreUpdates } = watchTriggerable(
    globalStore.get('PHYTO_DELAY'),
    (newVal) => {
      ignoreUpdates(  () => {
          runPythonS('config.PHYTO_DELAY = json.loads("""' + JSON.stringify(newVal) + '""")')

      })
    }, { deep: true }
  )
  trigger()
}
{
  const { trigger, ignoreUpdates } = watchTriggerable(
    globalStore.get('PHYTO_DELAY_TIME'),
    (newVal) => {
      ignoreUpdates(() => {
         runPythonS('config.PHYTO_DELAY_TIME = json.loads("""' + JSON.stringify(newVal) + '""")')

      })
    }, { deep: true }
  )
  trigger()
}


{
  const { trigger, ignoreUpdates } = watchTriggerable(
    globalStore.get('VERKRAUTUNG'),
    (newVal) => {
      ignoreUpdates(  () => {

         runPythonS('config.VERKRAUTUNG = json.loads("""' + JSON.stringify(newVal) + '""")')

      })
    }, { deep: true }
  )
  trigger()
}
{
  const { trigger, ignoreUpdates } = watchTriggerable(
    globalStore.get('DUNG_DATA'),
    (newVal) => {
      ignoreUpdates(  () => {

         runPythonS('config.DUNG_DATA = json.loads("""' + JSON.stringify(newVal) + '""")')

      })
    }, { deep: true }
  )
  trigger()
}



{

  const { trigger, ignoreUpdates } = watchTriggerable(
    globalStore.get('FF'),
   (newVal) => {
      console.log('ffu', isLoading.value)
      ignoreUpdates(() => {
        if (isLoading.value == false) {

          const updateFF = runPythonS("jswrapper.updateFF"); // get Python func
          console.log('update ff ')

          const v = JSON.parse(updateFF(ff.value));
          if (v) {
            console.log('write ff')
            ff.value = v;
          }


        }
      })
    }, { deep: true }
  )
  trigger()
}
