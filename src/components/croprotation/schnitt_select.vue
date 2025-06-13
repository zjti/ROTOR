<template>
  <v-row>
    <v-col>
      <v-card elevation="0">
        <v-card-item>
          <v-card-title> <l>SCHNITT_NUTZUNG</l>: </v-card-title>

          <v-card-subtitle> <l>SCHNITT_NUTZUNG_SUB</l> </v-card-subtitle>
        </v-card-item>
        <v-card-text>
          <NumberInput
            v-model="anzahl"
            class="custom-label-color"
            label="Anzahl der Schnitte"
            style="width: 100%"
            hide-details="auto"
            :step ='1'
            :min="0"
          ></NumberInput></v-card-text
      ></v-card>
    </v-col>
    <v-col><v-container style="height: 300px; overflow-y: scroll">
      <v-table v-if="anzahl > 0">
        <tbody>
          <tr v-for="n in anzahl" :key="n">
            <td>
              <NumberInput
                v-model="schnitte[n].yield"
                class="custom-label-color"
                :label="'Ertrag Schnitt ' + n"
                style="width: 100%"
                hide-details="auto"
                suffix="FM dt/ha"
              ></NumberInput>
              <v-select
                class="custom-label-color"
                :label="getlabel(n)"
                :items="['heu', 'silage', 'grünfutter', 'mulch']"
                v-model="schnitte[n].nutz"
              ></v-select>
              
              <!-- v-model="model.schnitt_nutz[n]" -->
            </td>
          </tr>
        </tbody>
      </v-table></v-container>
    </v-col>
  </v-row>
</template>
  
  <script setup>
import { computed, useTemplateRef } from "vue";

const props = defineProps({
  schnitte: {
    type: Object,
    required: true,
  },
});

const anzahl = computed({
  set: (ANZ) => {
    // Add amounts for newly selected items
    const defaultValue = { yield: 30, nutz: "grünfutter" };
    for (let key in props.schnitte) {
      if (Number(key) > ANZ) {
        delete props.schnitte[key];
      }
    }
    const highestKey = Math.max(...Object.keys(props.schnitte).map(Number), 0);
    if (ANZ > highestKey) {
      // Add new default entries up to ANZ
      for (let key = highestKey + 1; key <= ANZ; key++) {
        props.schnitte[key] = { ...defaultValue }; // Use a copy of the default value
      }
    }
  },
  get: () => {
    return Object.keys(props.schnitte).length;
  },
});

const getlabel = function (n) {
  var val = {
    1: "erste",
    2: "zweite",
    3: "dritte",
    4: "vierte",
    5: "fünfte",
  };
  if (n <= Object.keys(val).length) {
    return val[n] + " Nutzung";
  }
  return n + "te Nutzung";
};
</script>
  
  <style scoped>
</style>