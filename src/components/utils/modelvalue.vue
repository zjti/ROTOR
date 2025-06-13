<script setup>

const props = defineProps({
helpText: {
    type: String,
    default: '',
  },
  step: {
    type: Number,
    default: 0.2,
  },
  max: {
    type: Number,
    default: Infinity,
  },
  min: {
    type: Number,
    default: 0,
  }
});

import { computed, ref } from "vue";
const model = defineModel();
const half_months = [
    'JAN1','JAN2','FEB1','FEB2','MRZ1','MRZ2',
    'APR1','APR2','MAI1','MAI2','JUN1','JUN2',
    'JUL1','JUL2','AUG1','AUG2','SEP1','SEP2',
    'OKT1','OKT2','NOV1','NOV2','DEZ1','DEZ2',
]

</script>

<template>
    <div v-if="model && (!('visible' in model) ||  (model.visible == true))">
    <div v-if="'name_corrected' in model">
        
    
    <v-checkbox :label="model.name" v-model="model[model.name_corrected]" v-if="model.type == 'bool'" />


    <v-select v-else-if="model.type == 'select'" class="custom-label-color w-100" :label="model.name" :items="model.select_opts.map((key) => ({
        value: key,
        title: L(key),
    }))" v-model="model[model.name_corrected]"></v-select>

    <v-select v-else-if="model.type == 'date'" class="custom-label-color w-100" :label="model.name" :items="half_months.map((key) => ({
        value: key,
        title: L(key),
    }))" v-model="model[model.name_corrected]"></v-select>

    
    <NumberInput class="custom-label-color pa-0 ma-0" resetbtn :label="model.name" :suffix="model.unit"
        v-model="model[model.name_corrected]" :hint="Math.abs(model[model.name_corrected] - model[model.name])>0.1
            ? 'Wert vom Nutzer verändert '
            : ''"
            :helpText="helpText"
            :step="step"
            :min="min"
            :max="max"
            persistent-hint @send-reset="model[model.name_corrected] = model[model.name]" v-else />

    
    </div>
    <div v-else>
        <NumberInput class="custom-label-color pa-0 ma-0" :label="model.name" :suffix="model.unit"
        v-model="model[model.name]"  :readonly="true" nobtns/>
        
    </div>
</div>
        
    


</template>