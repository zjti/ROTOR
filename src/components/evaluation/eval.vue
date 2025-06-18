<template>
  <div>
    <v-expansion-panels variant="accordion" v-model="panel">
            <v-expansion-panel title=" &nbsp">
                <v-expansion-panel-text>

  


  <std_eval_table/>

  
  <v-container style="width:400px">
      <modelvalue v-model="FF['FF_META'].ff_eval.humus_method"/>
      <upload_dialog  />
      <div style="height:15px" ></div>
      <download_dialog  />
  </v-container>
   </v-expansion-panel-text>
   </v-expansion-panel>
   </v-expansion-panels>
  </div>

</template>

<script setup> 

import { globalStore } from "@/utils/globalstore";
import { ref } from "vue";

const eval_data = globalStore.get("EVAL_DATA");
const FF = globalStore.get("FF");
const panel = ref(0)
 

</script>
  
<style scoped>
</style>
  