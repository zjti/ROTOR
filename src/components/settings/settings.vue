
<script setup> 
</script>

<template>
  <v-container>
    <v-expansion-panels multiple>
      <v-expansion-panel :title="L('MAP_SETTINGS')" class="custom-expansion-panel">
        <v-expansion-panel-text>
          
          <RotorMap></RotorMap>
        </v-expansion-panel-text>
      </v-expansion-panel>
      <v-expansion-panel :title="L('SOIL_SETTINGS')" class="custom-expansion-panel">
        <v-expansion-panel-text> 
          <!-- <formview :block="soil_params" /> -->
          <formview :block="ps" />
        </v-expansion-panel-text>
      </v-expansion-panel>
      <v-expansion-panel :title="L('PHYTO_SETTINGS')" class="custom-expansion-panel">
        <v-expansion-panel-text>  
          <phyto-grid  :cellSize="30" />
        </v-expansion-panel-text>
      </v-expansion-panel>
      <v-expansion-panel :title="L('DUNG_PROPS')"  class="custom-expansion-panel">
        <v-expansion-panel-text>
          <dung_edit />
        </v-expansion-panel-text>
      </v-expansion-panel>
      <v-expansion-panel :title="L('VERKRAUTUNG')"  class="custom-expansion-panel">
        <v-expansion-panel-text>
          <verkraut />
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-container>
</template>

<script setup>
import { koraktor } from "./koraktor/koraktor";
import {watch, ref,reactive } from "vue";
import grid_weather from "../assets/geodata/grid_weather.json";
import usePyodide from '@/composables/usePyodide';
import { useStorage } from '@vueuse/core'
import params_soil from "../assets/params_soil.json";
const ps =  useStorage('PARAMS_SOIL',params_soil)


const { runPythonS } = usePyodide();
 
runPythonS('config.SOIL = json.loads("""'+ JSON.stringify( ps.value ) +'""")' )
watch(ps, async (newValue, oldValue) => {
  console.log('Soil changed:', newValue)
  console.log(JSON.stringify( params_soil.value ))
  runPythonS('config.SOIL = json.loads("""'+ JSON.stringify( ps.value ) +'""")' )
 
}, { deep: true })
 

koraktor.set( 'WEATHER_MONTHLY' ,grid_weather.features[10] )

// export default {
//   data() {
//     return {
//       soil_params: {},
//     };
//   },
//   async created() {
//     // Load the soil params from the JSON file
//     // const response = await fetch("./src/assets/params_soil.json");

//     // this.soil_params = koraktor.registerDict(await response.json());
//     this.soil_params = koraktor.registerDict(params_soil);
//   }, 
// };
</script>