<template>
  <div>

    <evaltable :crops="eval_data" />

     
  <v-container>
     <upload_dialog  />
     <download_dialog />
  </v-container>
 
  </div>
  
</template>

<script setup> 

import { globalStore } from "@/utils/globalstore";

const eval_data = globalStore.get("EVAL_DATA");

 

</script>
  
<style scoped>
</style>
  