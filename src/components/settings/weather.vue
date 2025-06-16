
   
<template>
        <div class="pa-4 grey lighten-4">
            
  <!-- <v-select

    :items="['ET0','PRECIPITATION','TEMPERATURE_AVG']"
    label="Parameter auswahl"
    
  ></v-select> -->
  <v-select
    v-model="WEATHER_KEY"

        class="custom-label-color w-100"
        label="Parameter auswahl"
        :items="
          ['ET0','PRECIPITATION','TEMPERATURE_AVG'].map((key) => ({
            value: key,
            title: L(key),
          }))
        "
      />

            <WeatherChart :labels="months" :data="scaledData" :title="L(WEATHER_KEY)" />
    
        <v-expansion-panels >
      <v-expansion-panel title="Anpassung">
        <v-expansion-panel-text>
          <modelvalue v-model="FF['FF_META'][WEATHER_KEY].get_1" title="Januar" />
          <modelvalue v-model="FF['FF_META'][WEATHER_KEY].get_2" title="Februar" />
          <modelvalue v-model="FF['FF_META'][WEATHER_KEY].get_3" title="März" />
          <modelvalue v-model="FF['FF_META'][WEATHER_KEY].get_4" title="April" />
          <modelvalue v-model="FF['FF_META'][WEATHER_KEY].get_5" title="Mai" />
          <modelvalue v-model="FF['FF_META'][WEATHER_KEY].get_6" title="Juni" />
          <modelvalue v-model="FF['FF_META'][WEATHER_KEY].get_7" title="Juli" />
          <modelvalue v-model="FF['FF_META'][WEATHER_KEY].get_8" title="August" />
          <modelvalue v-model="FF['FF_META'][WEATHER_KEY].get_9" title="September" />
          <modelvalue v-model="FF['FF_META'][WEATHER_KEY].get_10" title="Oktober" />
          <modelvalue v-model="FF['FF_META'][WEATHER_KEY].get_11" title="November" />
          <modelvalue v-model="FF['FF_META'][WEATHER_KEY].get_12" title="Dezember" />
        </v-expansion-panel-text>
      </v-expansion-panel>
      </v-expansion-panels>
          
          

        </div>
  </template> 
  
  <script setup>
  import { ref ,computed} from 'vue'
//   import WeatherChart from './WeatherChart.vue'
  import { globalStore } from '@/utils/globalstore'
  import { langf } from "@/main.js";
  
  const FF = globalStore.get('FF')

  const WEATHER_KEY = ref('ET0')

  const scaledData = computed(() =>{
        if ( WEATHER_KEY.value == 'PRECIPITATION'){
            return JSON.parse(FF.value['FF_META'][WEATHER_KEY.value].monthly.monthly).map(v => v * 30)
        }else{
            return JSON.parse(FF.value['FF_META'][WEATHER_KEY.value].monthly.monthly)
        }
    }
    )
   
  
  const months = [
  'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
]

  // Mock data: 365 days with random temperatures
  const daysOfYear = Array.from({ length: 365 }, (_, i) => `Day ${i + 1}`)
  const temperatureData = Array.from({ length: 365 }, () =>
    Math.round(Math.random() * 30)
  )
  </script>
  
  