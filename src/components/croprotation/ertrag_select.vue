<template>
    <v-row>
  <v-col>
    <v-card elevation="0">
      <v-card-item>
        <v-card-title> Ertrag: </v-card-title>
        <v-card-subtitle class="multi-line-subtitle">
          Standort-, Vorfrucht- und Düngungsabhängiger Ertrag. Ertrag und
          Rohproteingehalt sind veränderbar
        </v-card-subtitle>
      </v-card-item>
    </v-card></v-col
  ><v-col>
    <v-container style="height:300px;  overflow-y: scroll">

      

 
      </v-container
  ></v-col></v-row>
</template>
    
<script  setup>
import { globalStore } from '@/utils/globalstore'
import { watch, ref, reactive, computed } from "vue";
import NumberInput from "@/components/utils/NumberInput.vue";

const props = defineProps({
  jahr: {
    type: Number,
    required: true,
  },
});

const FF = globalStore.get("FF")

</script>
 
<style scoped>
  /* 
  .multi-line-subtitle {
    white-space: normal !important;
  } */

</style>