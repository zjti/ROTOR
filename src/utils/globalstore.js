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
const krautkey = useStorage('KRAUT_KEY', 'Region Nord-Ost')
const psoil = useStorage('PARAMS_SOIL', params_soil)
const pdt = useStorage('PHYTO_DELAY_TIME', CdelayData_time)
const pd = useStorage('PHYTO_DELAY', CdelayData)
const pdung = useStorage('PARAMS_DUNG', params_dung)
const ff = useStorage('FF', {})
const puser = useStorage('PARAMS_USER', userlocation)

const eval_data = useStorage('EVAL_DATA', {})

const location = useStorage('LOCATION_LAT_LONG',{'lat':52,'lon':14})
const climate_data = useStorage('CLIMATE_DATA_MONTLY',{})
const NJahre = useStorage('FFOLGE_NJAHRE', 5)

export const globalStore = new Map();
globalStore.set('FFOLGE_NJAHRE', NJahre)
globalStore.set('PARAMS_USER', puser)
globalStore.set('SOIL', psoil)
globalStore.set('PHYTO_DELAY_TIME', pdt)
globalStore.set('PHYTO_DELAY', pd)
globalStore.set('KRAUT_KEY', krautkey)
globalStore.set('VERKRAUTUNG', verkraut)
globalStore.set('DUNG_DATA', pdung)
globalStore.set('FF', ff)
globalStore.set('EVAL_DATA', eval_data)
globalStore.set('LOCATION_LAT_LONG', location)
globalStore.set('CLIMATE_DATA_MONTLY', climate_data)




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
          
          runPythonS('config.KRAUT_KEY = json.loads(""" ' + JSON.stringify(krautkey.value) + ' """)')
          runPythonS('config.VERKRAUTUNG = json.loads(""" ' + JSON.stringify(verkraut.value) + ' """)')


          // const ff_json = updateFF(ff.value)
          // const v = JSON.parse(ff_json);
          // if (v) {
          //   console.log('write ff')
          //   ff.value = v;
          //   writetojupyter('config_data/FFolge.json', ff_json)
          //   const eval_data_json = get_eval_data()
          //   eval_data.value = JSON.parse(eval_data_json)
          //   globalStore.get('EVAL_DATA', eval_data).value =  JSON.parse(eval_data_json)

          //   writetojupyter('config_data/eval_data.json', eval_data_json)
          // }
          for (var i = 0; i < 1; i++){
            var ff_json = updateFF(ff.value)
            var v = JSON.parse(ff_json);
            ff.value = v;
            
          }
          
          writetojupyter('config_data/FFolge.json', ff_json)
          const eval_data_json = get_eval_data()
          eval_data.value = JSON.parse(eval_data_json)
          globalStore.get('EVAL_DATA', eval_data).value =  JSON.parse(eval_data_json)

          writetojupyter('config_data/eval_data.json', eval_data_json)

        } catch (error) {
          console.error('Error updating FF:', error);
        }



      }
    })
  }, { deep: true }
)
var FF_initialized_trigger = () => { }
const FF_trigger = trigger



const { trigger:trigger_CLIMATE_DATA_MONTLY   } = watchTriggerable(
  globalStore.get('CLIMATE_DATA_MONTLY'),
  (newVal) => {
    ignoreUpdates(() => {
      const updateWeather = runPythonS("jswrapper.JSupdateWeather"); 
      updateWeather(JSON.stringify(globalStore.get('LOCATION_LAT_LONG').value))
      
      runPythonS('config.CLIMATE_DATA_MONTLY = json.loads("""' + JSON.stringify(newVal) + '""")')
      writetojupyter('config_data/CLIMATE_DATA_MONTLY.json', JSON.stringify(newVal))

      FF_initialized_trigger()

    })
  }, { deep: true }
)
trigger_CLIMATE_DATA_MONTLY()


{
  const { trigger, ignoreUpdates } = watchTriggerable(
    globalStore.get('LOCATION_LAT_LONG'),
    (newVal) => {
      ignoreUpdates(() => {
        const updateWeather = runPythonS("jswrapper.JSupdateWeather"); 
        // updateWeather(JSON.stringify(globalStore.get('LOCATION_LAT_LONG').value))
        updateWeather(JSON.stringify(newVal))
  
        runPythonS('config.LOCATION_LAT_LONG = json.loads("""' + JSON.stringify(newVal) + '""")')
        writetojupyter('config_data/LOCATION_LAT_LONG.json', JSON.stringify(newVal))

        trigger_CLIMATE_DATA_MONTLY()
        // FF_initialized_trigger()

      })
    }, { deep: true }
  )
  trigger()
}

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