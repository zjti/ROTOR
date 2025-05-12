<script setup>
import { ref, watchEffect, getCurrentInstance, watch } from "vue";
import usePyodide from "@/composables/usePyodide";
import { useStorage, watchPausable } from "@vueuse/core";
import { globalStore } from '@/utils/globalstore'



const { pyodide, runPythonS, runPython } = usePyodide();

const updateFFlength = runPythonS("jswrapper.updateFFlength"); // get Python func

const FF = globalStore.get("FF")

const NJahre = ref(5);

FF.value = JSON.parse(updateFFlength(FF.value, NJahre.value));
const jahr = ref(1);
const tab = ref("auswahl");
const panel = ref(0);


watch(NJahre, (newValue, oldValue) => {
  const v = JSON.parse(updateFFlength(FF.value, newValue))
  console.log('aa', v)

  if (v) {
    FF.value = v;
  }
});





</script>


<template>
  <div>
    <v-expansion-panels variant="accordion" v-model="panel">
      <v-expansion-panel :title="L('FF_CREATE')" class="custom-expansion-panel">
        <v-expansion-panel-text>
          <NumberInput v-model="NJahre" class="custom-label-color" :label="L('FF_LENGTH')" style="width: 100%"
            hide-details="auto"></NumberInput>
        </v-expansion-panel-text>
      </v-expansion-panel>
      <v-expansion-panel class="custom-expansion-panel">
        <template v-slot:title v-if="panel !== 1">
          <span>
            <l>OPTIONS</l>
          </span>
        </template>
        <v-expansion-panel-text>
          <v-row>
            <v-col cols="3">
              <NumberInput v-model="jahr" class="custom-label-color" :label="L('ANBAU_JAHR') +
                (Object.hasOwn(FF[jahr], 'crop') && FF[jahr].crop ? '  (' + L(FF[jahr].crop) + ')' : '')
                " style="width: 100%" hide-details="auto" @update:model-value="tab = 'auswahl'"></NumberInput>

              <v-tabs v-model="tab" direction="vertical">
                <v-tab value="auswahl">
                  <l>Auswahl</l>
                </v-tab>
                <v-tab value="anbau" v-if="FF[jahr].vis.anbau_tab">
                  <l>Anbau</l>
                </v-tab>
                <v-tab value="dung" v-if="FF[jahr].vis.dung_tab">
                  <l>Dünger</l>
                </v-tab>
                <v-tab value="schnitt" v-if="FF[jahr].vis.schnitt_tab">
                  <l>Schnittnutzung</l>
                </v-tab>
                <v-tab value="ertrag" v-if="FF[jahr].vis.ertrag_tab">
                  <l>Ertrag</l>
                </v-tab>
              </v-tabs>
            </v-col>
            <v-col>
              <v-tabs-window v-model="tab" style="height: 300px" class="w-100">
                <v-tabs-window-item value="schnitt">
                  <schnitt_select v-model:schnitte="FF[jahr].schnitt_menge"></schnitt_select>
                </v-tabs-window-item>

                <v-tabs-window-item value="ertrag" v-if="FF[jahr].vis.ertrag_tab">
                  <ertrag_select :jahr="jahr" />
                </v-tabs-window-item>

                <v-tabs-window-item value="anbau" style="overflow-y: scroll" v-if="FF[jahr].vis.anbau_tab">
                  <v-card elevation="0">
                    <v-card-item>
                      <v-card-title>
                        <l>ANBAU_OPTS</l>
                      </v-card-title>

                      <v-card-subtitle class="multi-line-subtitle">
                        <l>ANBAU_OPTS_SUB</l>
                      </v-card-subtitle>
                    </v-card-item>
                    <v-card-text>
                      <v-select v-if="FF[jahr].vis.leg_ansaat" style="height: 80px" class="custom-label-color"
                        :label="L('Ansaat')" :items="FF[jahr].leg_ansaat_opts.map((key) => ({
                          value: key,
                          title: L(key),
                        }))" v-model="FF[jahr].leg_ansaat" />
                      <v-checkbox :label="L('UNDERSAWN')" v-if="FF[jahr].vis.us_opt" v-model="FF[jahr].us"></v-checkbox>


                      <NumberInput class="custom-label-color pa-0 ma-0" label="Saatgutmenge" suffix="kg/ha"
                        v-model="FF[jahr].seeds_kg_per_ha_corrected" :hint="FF[jahr].seeds_kg_per_ha_corrected != FF[jahr].seeds_kg_per_ha
                          ? 'Saatgutbedarf vom benutzer Modifiziert'
                          : ''
                          " persistent-hint />

                      <v-checkbox :label="L('Nebenprodukternte')" v-if="FF[jahr].vis.stroh_opt"
                        v-model="FF[jahr].stroh"></v-checkbox>
                      <v-checkbox :label="L('Zwischenfrucht_select')" v-if="FF[jahr].vis.zw_opt"
                        v-model="FF[jahr].zw"></v-checkbox>

                      <NumberInput class="custom-label-color pa-0 ma-0" label="Ertrag Zwischenfrucht" suffix="FM dt/ha"
                        v-model="FF[jahr].covercrop_yield_dt_corrected" :hint="FF[jahr].covercrop_yield_dt_corrected != FF[jahr].covercrop_yield_dt
                          ? 'Zwischenfruchtertrag vom benutzer Modifiziert'
                          : ''
                          " persistent-hint v-if="FF[jahr].zw" />

                      <v-select style="height: 80px" :label="L('Zwischefruchtanbau')" :items="FF[jahr].zw_plant_opts.map((key) => ({
                        value: key,
                        title: L(key),
                      }))
                        " class="custom-label-color" v-model="FF[jahr].zw_plant" v-if="FF[jahr].zw">
                      </v-select>

                      <NumberInput v-if="FF[jahr].zw" class="custom-label-color" :label="L('LEG_SELECT_IN_ZW')"
                        suffix="% TS" v-model="FF[jahr].zwischenfrucht_legant"></NumberInput>

                      <v-select v-if="FF[jahr].zw" class="custom-label-color" :label="L('SEL_WINTER_HARD')" :items="['abfrierend', 'frosthart'].map((key) => ({
                        value: key,
                        title: L(key),
                      }))
                        " v-model="FF[jahr].zwischenfrucht_winterhard"></v-select>

                      <v-select v-if="
                        FF[jahr].zw &&
                        FF[jahr].zwischenfrucht_winterhard == 'frosthart'
                      " class="custom-label-color" :label="L('SEL_ZW_NUTZ')" :items="['Abfuhr', 'Einarbeitung'].map((key) => ({
                      value: key,
                      title: L(key),
                    }))
                      " v-model="FF[jahr].zwischenfrucht_schnittnutz"></v-select>
                    </v-card-text>
                  </v-card>
                </v-tabs-window-item>
                <v-tabs-window-item value="dung" v-if="FF[jahr].vis.dung_tab"
                  style="overflow-y: scroll;overflow-x: clip;height: 100%;">
                  <dung_select v-model:amounts="FF[jahr].dung_menge" :has_herbst_gabe="FF[jahr].vis.has_herbst_gabe" />
                </v-tabs-window-item>

                <v-tabs-window-item value="auswahl">
                  <v-card elevation="0">
                    <v-card-item>
                      <v-card-title>
                        <l>LIMIT_CROP_SELECT</l>
                      </v-card-title>
                      <v-card-subtitle class="multi-line-subtitle">
                        <l>LIMIT_CROP_SELECT_SUB</l>
                      </v-card-subtitle>
                    </v-card-item>
                    <v-card-text>
                      <v-checkbox :label="L('RESTRICT_PHYTO')" v-model="FF[jahr].restr_select_phyto"></v-checkbox>
                      <v-checkbox :label="L('RESTRICT_TIME')" v-model="FF[jahr].restr_select_time"></v-checkbox>
                    </v-card-text>
                  </v-card>
                </v-tabs-window-item>
              </v-tabs-window>
            </v-col>
          </v-row>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>

    <v-row no-gutters class="ma-0 pa-0" style="width: 100%">
      <v-col v-for="n in NJahre" :key="n" class="ma-0 pa-0">
        <ffcomp @click="jahr = n; tab = 'auswahl'" :jahr="n"></FFComp>
      </v-col>
    </v-row>
  </div>
</template>
<style>
.multi-line-subtitle {
  white-space: normal !important;
}
</style>