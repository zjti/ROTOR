<style>
.custom-label-color .v-label {
  font-size: 17px;
  color: #002200;
}

.custom-expansion-panel .v-expansion-panel-title {
  font-size: 1.5rem; /* Adjust size as needed */
  /* font-weight: bold; */
  min-height: 48px; /* Optional: increase height */
}
</style>


<script setup>
import { getCurrentInstance ,onMounted ,ref,watch} from "vue";
import { useStorage } from '@vueuse/core'

import usePyodide from '@/composables/usePyodide';
 
  
const { isLoading,pyodide, initializePyodide,runPython } = usePyodide();
  
const authenticated = useStorage('authenticated', false)  


const is_mounted = ref(false)
onMounted(async () => {
  
  while (isLoading.value ){
    await new Promise(r => setTimeout(r, 200));
    console.log('isloading')
  }
  console.log('done loading')


  await runPython('import json \n')
  // await runPython('import config \n')
//   await runPython('from ff.calc_opts import calc_opts \n')
//   await runPython('CROP_OPTS = json.loads("""'+ JSON.stringify(koraktor.get('CROP_OPTS').value) + '""")')
//   await runPython ('config.PHYTO_DELAY =      json.loads("""' + JSON.stringify(koraktor.get('PHYTO_DELAY').value) + '""") ')
//   await runPython ('config.PHYTO_DELAY_TIME = json.loads("""' + JSON.stringify(koraktor.get('PHYTO_DELAY_TIME').value) + '""") ')
//   await runPython ('config.DUNG_DATA = json.loads("""' + JSON.stringify(koraktor.get('DUNG_DATA').value) + '""") ')
  
//   await runPython('config.SOIL = json.loads("""'+ JSON.stringify( ps.value) +'""")' )
//   await runPython('config.WEATHER_DATA = json.loads("""'+ JSON.stringify( weather_data) +'""")' )
  
  is_mounted.value=true;
});
 


const instance = getCurrentInstance();
const app = instance.appContext.app; 


const tab =  useStorage('tab', "3")
const cur_lang = useStorage('cur_lang', 'de')
app.config.globalProperties.cur_lang = cur_lang

const next_lang = (lang)=>{
  if (lang.value=='de'){
    return 'en' 
  }
  if (lang.value=='en'){
    return 'xx'
  } 
  if (lang.value=='xx'){
    return 'de';
  }
}
</script>


<template>
  <v-app>
    <Password
      v-if="!authenticated "
      @password-correct="authenticated = true"
    />
      <loading  v-if='authenticated'/> 
    
    
      <v-app-bar v-if="authenticated && !isLoading && is_mounted"
 >
        <v-img
          class="mx-2"
          src="./assets/imgs/zalf.jpg"
          max-height="40"
          max-width="40"
          contain
        ></v-img>
        <v-img
          class="mx-2"
          src="./assets/imgs/bol.jpg"
          height="51"
          max-width="40"
          contain
        ></v-img>
        <v-img
          class="mx-2"
          src="./assets/imgs/wm_logo.png"
          max-height="40"
          max-width="40"
          contain
        ></v-img>
        <v-toolbar-title class="ml-2">
        <img
          
          src="./assets/imgs/rotor.png"
          height="100px"
          
        />
      </v-toolbar-title>
        <!-- <v-toolbar-title class="ml-2"> ROTOR </v-toolbar-title> -->
   
        <v-tabs v-model="tab">
          <v-tab value="1">
            <l>WELCOME_TAB</l>
          </v-tab>
          <v-tab value="2">
            <l>SETTINGS_TAB</l>
          </v-tab>
          <v-tab value="3">
            <l>FRUCHTFOLGE_TAB</l>
          </v-tab>

          <v-tab value="4">
            <l>ECO_TAB</l>
          </v-tab>
          <v-tab value="5">
            <l>EVAL_TAB</l>
          </v-tab>
        </v-tabs>

        <v-spacer></v-spacer>

        <v-btn
          flat
          @click="(app.config.globalProperties.cur_lang.value = next_lang(app.config.globalProperties.cur_lang)),
            console.log(app.config.globalProperties.cur_lang)"     

        >
          <span class="mr-2">{{ app.config.globalProperties.cur_lang}}</span>
        </v-btn>
      </v-app-bar>

       
      <v-main
        class="d-flex justify-center"
        style="min-height: 300px"
        v-if="authenticated && !isLoading && is_mounted"
      >
        <!-- Main Content -->
        <drop_down_console/>  

        <v-tabs-window v-model="tab" style="width: 90%">
          <v-tabs-window-item value="1"> <welcome/> </v-tabs-window-item>

          <v-tabs-window-item value="2">
            <settings></settings>
          </v-tabs-window-item>

          <v-tabs-window-item value="3">
            <ff />
          </v-tabs-window-item>
          <v-tabs-window-item value="4"> 4 
              <!-- <ecoedit /> -->
               <ff_eco></ff_eco>

          </v-tabs-window-item>

          <v-tabs-window-item value="5">
            <v-container>
              <v-expansion-panels multiple v-if="app.config.globalProperties.cur_lang.value=='dx'">
                <v-expansion-panel title="CropOpts">
                  <v-expansion-panel-text>
                    <crop_opts />
                  </v-expansion-panel-text>
                </v-expansion-panel>

                <v-expansion-panel title="CropCodeOpts">
                  <v-expansion-panel-text>
                    <kbase />
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>
            </v-container>
            <eva/>
          </v-tabs-window-item>
        </v-tabs-window>
      </v-main>
        
  </v-app>
</template>

 
 
 
