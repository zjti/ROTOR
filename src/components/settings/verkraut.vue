<template>
    nok
    <grid
      :delayData="verkrautung"
      :cellSize="30"
      :fixedColumnOrder="colnames"
      dataType="number"
      horizontalAxisLabel="Kraut"
      verticalAxisLabel="Kultur/Methode"
    />
   
  </template>

<script>
import { globalStore } from '@/utils/globalstore'




export default {
  data() {
    return {
      colnames: ['PEREN_VK','WINTER_VK','SOMMER_VK'],
 
      verkrautung: globalStore.get('VERKRAUTUNG'),
    };
  },
  async created() {
    // Load the crop options from the JSON file

    // this.cropOptions = await this.loadCropOptions();
 
   
    
  },
};
</script>
