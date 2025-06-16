<template>
    <div>
      <v-select
    v-model="KRAUT_KEY"

        class="custom-label-color w-100"
        label="Parameter auswahl"
        :items="['Region Nord-Ost','Region Süd', 'Region Nord-West']"
      />
    
    <grid
      :delayData="verkrautung[KRAUT_KEY]"
      :cellSize="30"
      :fixedColumnOrder="colnames"
      dataType="number"
      horizontalAxisLabel="Verunkrautungsindex"
      verticalAxisLabel="Fruchtart/Methode"
    />
  </div>
  </template>

<script setup>
import { ref } from "vue";
import { globalStore } from '@/utils/globalstore'


const KRAUT_KEY =  globalStore.get('KRAUT_KEY') //ref('Region Nord-Ost')
</script>
<script>
import { globalStore } from '@/utils/globalstore'




export default {
  data() {
    return {
      colnames: ['PEREN_VK','SOMMER_VK','WINTER_VK'],
 
      verkrautung: globalStore.get('VERKRAUTUNG'),
    };
  },
  async created() {
    // Load the crop options from the JSON file

    // this.cropOptions = await this.loadCropOptions();
 
   
    
  },
};
</script>
