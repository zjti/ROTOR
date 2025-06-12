<script setup>
import { ref, watchEffect, getCurrentInstance, watch } from "vue";
import usePyodide from "@/composables/usePyodide";
import { useStorage, watchPausable } from "@vueuse/core";
import { globalStore } from '@/utils/globalstore'
import { keyValues } from "vuetify/lib/util/helpers.mjs";



const { pyodide, runPythonS, runPython } = usePyodide();

// const updateFFlength = ); 

const FF = globalStore.get("FF")
const  panel = ref(0)


const fu = () => {
    const file_bytes = runPythonS(`jswrapper.JSdownload_eco_report()`)
    console.log(file_bytes)
    const uint8Array = new Uint8Array(file_bytes);

    const blob = new Blob([uint8Array], { type: "application/pdf" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "downloaded_from_pyodide.pdf";
    link.click();
}

</script>

<template>
    <div>
        <v-expansion-panels variant="accordion" v-model="panel">
            <v-expansion-panel title="Ökonomie">
                <v-expansion-panel-text >

                    <modelvalue v-model="FF['1'].MODELVALUES.economy.diesel_eur_per_l" />
                    <modelvalue v-model="FF['1'].MODELVALUES.economy.extra_cost_eur_per_ha" helpText="Dieser wert kann in jedem Anbaujahr angepasst werden. Kann Kosten für Versicherungen etc. beinhalten. "/>
                    <modelvalue v-model="FF['1'].MODELVALUES.economy.sesssion_labour_eur_per_h" />
                    <v-btn @click="fu()">Download</v-btn>  
                    

                </v-expansion-panel-text>
            </v-expansion-panel>
        </v-expansion-panels>


        <v-expansion-panels variant="accordion" multiple>
            <v-expansion-panel v-for="(value, key, index) in FF" :key="index"
                :title="'Anbaujahr ' + key + ' ' + L(value.crop)">
                <v-expansion-panel-text>

                    <v-expansion-panels variant="accordion">
                        <v-expansion-panel title="Leistungen">
                            <v-expansion-panel-text>
                                <modelvalue v-model="value.MODELVALUES.yield_dt_fm_per_ha" />
                                <modelvalue v-model="value.MODELVALUES.cropeconomy.price_yield_eur_per_dt_fm" />
                                <modelvalue v-model="value.MODELVALUES.cropeconomy.yield_leistung_eur_per_ha" />

                                <modelvalue v-model="value.MODELVALUES.cropeconomy.other_leistung_eur_per_ha" />

                            </v-expansion-panel-text>
                        </v-expansion-panel>
                        
                         <v-expansion-panel title="Saatgut">
                            <v-expansion-panel-text>
                                
                                <div v-if="!('seed_u_per_ha' in value.MODELVALUES)" >
                                <modelvalue v-model="value.MODELVALUES.seed_kg_per_ha"  />
                                <modelvalue v-model="value.MODELVALUES.cropeconomy.seed_cost_eur_per_kg"  />
                                </div><div v-else>
                                <modelvalue v-model="value.MODELVALUES.seed_u_per_ha"  />
                                <modelvalue v-model="value.MODELVALUES.cropeconomy.seed_cost_eur_per_u"/>
                                </div>
                                <modelvalue v-model="value.MODELVALUES.cropeconomy.seed_cost_eur_per_ha" />


                            </v-expansion-panel-text>
                        </v-expansion-panel>

                        <v-expansion-panel title="Sonstige Kosten">
                            <v-expansion-panel-text>
                                <modelvalue v-model="value.MODELVALUES.cropeconomy.extra_cost_eur_per_ha" />


                            </v-expansion-panel-text>
                        </v-expansion-panel>
                        

                    </v-expansion-panels>



                    <cover_crop_economy v-model="value.MODELVALUES.cropeconomy.covercropeconomy"
                        v-if="'covercropeconomy' in value.MODELVALUES.cropeconomy" />


                    <worksteplist v-model="value.MODELVALUES.cropeconomy" />

                  
                <modelvalue v-model="value.MODELVALUES.cropeconomy.gross_margin_eur_per_ha" />
                <modelvalue v-model="value.MODELVALUES.cropeconomy.gross_margin_per_man_hour_eur_per_h" />
                

                </v-expansion-panel-text>
            </v-expansion-panel>
        </v-expansion-panels>
    </div>
</template>
