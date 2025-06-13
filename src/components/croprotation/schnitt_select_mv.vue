<template>
  <v-row>
    <v-col>
      <v-card elevation="0">
        <v-card-item>
          <v-card-title> <l>SCHNITT_NUTZUNG</l>: </v-card-title>

          <v-card-subtitle> <l>SCHNITT_NUTZUNG_SUB</l> </v-card-subtitle>
        </v-card-item>
        <v-card-text>
          <!-- <NumberInput
            v-model="anzahl"
            class="custom-label-color"
            label="Anzahl der Schnitte"
            style="width: 100%"
            hide-details="auto"
            :step ='1'
            :min="0"
          ></NumberInput> -->
          <modelvalue v-model="model.num_cuts" :step="1" :min="0" :max="5"/>
          </v-card-text
      ></v-card>
    </v-col>
    <v-col><v-container style="height: 300px; overflow-y: scroll">
      <v-table >
        <tbody>
          <!-- <tr v-for="n in anzahl" :key="n">
            <td> -->
              <!-- <NumberInput
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
              ></v-select> -->
            <tr><td>
              <modelvalue v-model="model.cut1"/>
              <modelvalue v-model="model.nutz1"/>
            
              <modelvalue v-model="model.cut2"/>
              <modelvalue v-model="model.nutz2"/>
            
              <modelvalue v-model="model.cut3"/>
              <modelvalue v-model="model.nutz3"/>
            
              <modelvalue v-model="model.cut4"/>
              <modelvalue v-model="model.nutz4"/>
            
              <modelvalue v-model="model.cut5"/>
              <modelvalue v-model="model.nutz5"/>
            </td></tr>
        </tbody>
      </v-table></v-container>
    </v-col>
  </v-row>
</template>
  
  <script setup>
import { computed, useTemplateRef } from "vue";

const model = defineModel();


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