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
      <NumberInput
        class="custom-label-color pa-0 ma-0"
        label="Gesamtertrag Hauptprodukt"
        suffix="FM dt/ha"
        v-model="FF[props.jahr].yield_dt_corrected"
        :hint="
          FF[props.jahr].yield_dt_corrected != FF[props.jahr].yield_dt_calc 
            ? 'Ertrag vom benutzer Modifiziert'
            : ''
        "
        persistent-hint
      />
      <v-text-field
        v-if="
          'dung_menge' in  FF[props.jahr] && Object.keys(FF[props.jahr].dung_menge).length > 0
        "
        class="custom-label-color pa-0 ma-0"
        label="davon Mehrertrag aus Düngung"
        suffix="FM dt/ha"
        :readonly='true'
        v-model="FF[props.jahr].yield_from_fert_dt"
      />

      <NumberInput
        class="custom-label-color pa-0 ma-0"
        label="Rohproteingehalt im Hauptprodukt "
        suffix="%"
        v-model="FF[props.jahr].crude_protein_content_corrected"
        :hint="
        FF[props.jahr].crude_protein_content_corrected != FF[props.jahr].crude_protein_content 
            ? 'Rohproteingehalt vom benutzer Modifiziert'
            : ''
        "
        persistent-hint
      />

      <NumberInput
        class="custom-label-color pa-0 ma-0"
        label="Ertrag Nebenprdukt"
        suffix="FM dt/ha"
        v-model="FF[props.jahr].nebenprodukt_yield_dt_corrected"
        :hint="
          FF[props.jahr].nebenprodukt_yield_dt_corrected != FF[props.jahr].nebenprodukt_yield_dt_calc
            ? 'Nebenproduktertrag vom benutzer Modifiziert'
            : ''
        "
        persistent-hint
      /> </v-container
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