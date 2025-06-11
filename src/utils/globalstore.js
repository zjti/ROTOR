import { reactive, } from 'vue'
import { useStorage, watchTriggerable } from '@vueuse/core'
import usePyodide from '@/composables/usePyodide';
const { runPython, runPythonS, isLoading, initializePyodide } = usePyodide();

import params_soil from "../assets/params/params_soil.json";
import CdelayData from "../assets/cross_breaks.json";
import CdelayData_time from "../assets/cross_breaks_time.json";
import verkrautung from "../assets/params/verkraut.json";
import params_dung from "../assets/params/params_dung.json";
import weather_data from "../assets/params/wd.json";

const userlocation = useStorage("USERINFO",{
  "FARMNAME": {
      "default": '',
      "type": "string", 
      "help":"Bitte Betriebsnamen für die Auswertung angeben"
  },"USERNAME": {
      "default": '',
      "type": "string", 
      "help":"Bitte Namen des Bearbeiters für die Auswertung angeben"
  },"FARMSIZE": {
      "default":"FARM_SMALL",
      "type": "select",
      "items":["FARM_SMALL","FARM_MEDIUM","FARM_BIG"]
  },
})

await initializePyodide();
await runPython('config.WEATHER_DATA = json.loads("""' + JSON.stringify(weather_data) + '""")');

const verkraut = useStorage('VERKRAUTUNG', verkrautung)
const psoil = useStorage('PARAMS_SOIL', params_soil)
const pdt = useStorage('PHYTO_DELAY_TIME', CdelayData_time)
const pd = useStorage('PHYTO_DELAY', CdelayData)
const pdung = useStorage('PARAMS_DUNG', params_dung)
const ff = useStorage('FF', {})
const puser = useStorage('PARAMS_USER', userlocation)

const eval_data = useStorage('EVAL_DATA', {})


export const globalStore = new Map();
globalStore.set('PARAMS_USER', puser)
globalStore.set('SOIL', psoil)
globalStore.set('PHYTO_DELAY_TIME', pdt)
globalStore.set('PHYTO_DELAY', pd)
globalStore.set('VERKRAUTUNG', verkraut)
globalStore.set('DUNG_DATA', pdung)
globalStore.set('FF', ff)
globalStore.set('EVAL_DATA', eval_data)



function writetojupyter(filename, content) {
  const storageKey = `JupyterLite Storage/files/${filename}`;



  // Create file entry
  const fileEntry = {
    name: filename.split('/').pop(),
    path: filename,
    type: "file",
    format: "text",
    mimetype: "text/plain",
    content,
    size: content.length,
    writable: true,
    created: new Date().toISOString(),
    last_modified: new Date().toISOString()
  };
  localStorage.setItem(storageKey, JSON.stringify(fileEntry));
}


const { trigger, ignoreUpdates } = watchTriggerable(
  globalStore.get('FF'),
  (newVal) => {
    ignoreUpdates(() => {
      if (isLoading.value == false) {

        try {
          const updateFF = runPythonS("jswrapper.JSupdateFF"); // get Python func
          const get_eval_data = runPythonS("jswrapper.JSget_eval_data"); // get Python func
          console.log('update ff ')

          const ff_json = updateFF(ff.value)
          const v = JSON.parse(ff_json);
          if (v) {
            console.log('write ff')
            ff.value = v;
            writetojupyter('config_data/FFolge.json', ff_json)
            eval_data.value = JSON.parse(get_eval_data())
          }
        } catch (error) {
          console.error('Error updating FF:', error);
        }



      }
    })
  }, { deep: true }
)
var FF_initialized_trigger = () => { }
const FF_trigger = trigger


{
  const { trigger, ignoreUpdates } = watchTriggerable(
    globalStore.get('SOIL'),
    (newVal) => {
      ignoreUpdates(() => {
        runPythonS('config.SOIL = json.loads("""' + JSON.stringify(newVal) + '""")')
        writetojupyter('config_data/SOIL.json', JSON.stringify(newVal))

        FF_initialized_trigger()

      })
    }, { deep: true }
  )
  trigger()
}

{
  const { trigger, ignoreUpdates } = watchTriggerable(
    globalStore.get('PHYTO_DELAY'),
    (newVal) => {
      ignoreUpdates(() => {
        runPythonS('config.PHYTO_DELAY = json.loads("""' + JSON.stringify(newVal) + '""")')
        writetojupyter('config_data/PHYTO_DELAY.json', JSON.stringify(newVal))
        FF_initialized_trigger()

      })
    }, { deep: true }
  )
  trigger()
}
{
  const { trigger, ignoreUpdates } = watchTriggerable(
    globalStore.get('PARAMS_USER'),
    (newVal) => {
      ignoreUpdates(() => {
        runPythonS('config.PARAMS_USER = json.loads("""' + JSON.stringify(newVal) + '""")')
        writetojupyter('config_data/PARAMS_USER.json', JSON.stringify(newVal))
        FF_initialized_trigger()

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
        writetojupyter('config_data/PHYTO_DELAY_TIME.json', JSON.stringify(newVal))
        FF_initialized_trigger()

      })
    }, { deep: true }
  )
  trigger()
}


{
  const { trigger, ignoreUpdates } = watchTriggerable(
    globalStore.get('VERKRAUTUNG'),
    (newVal) => {
      ignoreUpdates(() => {

        runPythonS('config.VERKRAUTUNG = json.loads("""' + JSON.stringify(newVal) + '""")')
        writetojupyter('config_data/VERKRATUNG.json', JSON.stringify(newVal))
        FF_initialized_trigger()

      })
    }, { deep: true }
  )
  trigger()
}
{
  const { trigger, ignoreUpdates } = watchTriggerable(
    globalStore.get('DUNG_DATA'),
    (newVal) => {
      ignoreUpdates(() => {

        runPythonS('config.DUNG_DATA = json.loads("""' + JSON.stringify(newVal) + '""")')
        writetojupyter('config_data/DUNG_DATA.json', JSON.stringify(newVal))
        FF_initialized_trigger()

      })
    }, { deep: true }
  )
  trigger()
}

FF_trigger()
FF_initialized_trigger = FF_trigger

window.ff_initialized_trigger = FF_trigger