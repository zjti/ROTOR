<script setup>
import { ref, watchEffect, getCurrentInstance, watch, computed } from "vue";
import usePyodide from "@/composables/usePyodide";
import { useStorage, watchPausable } from "@vueuse/core";
import { globalStore } from '@/utils/globalstore'
import { keyValues } from "vuetify/lib/util/helpers.mjs";



const { pyodide, runPythonS, runPython } = usePyodide();

// const updateFFlength = ); 

const FF = globalStore.get("FF")
// const NJahre= Object.keys(FF.value).length - 1
// console.log('AWE',NJahre,Object.keys(FF.value))


const panel = ref(0)
const panel2 = ref(0)


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


 
const generateStackedDatasets = (values) => {
    const numSegments = values[0]?.length || 0

    const baseColors = [
        '#1abc9c', '#3498db', '#e67e22', '#e74c3c',
        '#9b59b6', '#f1c40f', '#2ecc71', '#34495e'
    ]

    const segmentNames = ['Irrigation', 'Rain', 'Snow', 'Evaporation', 'Runoff', 'Drainage']

    return Array.from({ length: numSegments }, (_, i) => ({
        label: segmentNames[i] || `Segment ${i + 1}`,
        data: values.map(v => v[i]),
        backgroundColor: baseColors[i % baseColors.length],
        stack: 'stack-0'
    }))
}
// const datasets =ref( generateStackedDatasets(values))


 
// const datasets = ref(buildDatasetsFromDicts(wokrload_dicts.value))



</script>

<template>
    <div>
        <v-expansion-panels variant="accordion" v-model="panel">
            <v-expansion-panel title="Ökonomie">
                <v-expansion-panel-text>

                    <v-expansion-panels variant="accordion" multiple v-model="panel2">
                        <v-expansion-panel title="Deckungsbeitrag für Fruchtfolge">
                            <v-expansion-panel-text>
                                <modelvalue v-model="FF['FF_META'].economy.ff_gross_margin_eur_per_ha" />

                            </v-expansion-panel-text>
                        </v-expansion-panel>
                        <v-expansion-panel title="Arbeitsspitzen">
                            <v-expansion-panel-text>
                                <work_load_chart :labels="FF['FF_META'].economy.half_months.half_months" :datasets="FF['FF_META'].economy.arbeits_spitzen_plot.arbeits_spitzen_plot" />
                            </v-expansion-panel-text>
                        </v-expansion-panel>
                        <v-expansion-panel title="Sonstiges">
                            <v-expansion-panel-text>

                                <modelvalue v-model="FF['FF_META'].economy.diesel_eur_per_l" />
                                <modelvalue v-model="FF['FF_META'].economy.extra_cost_eur_per_ha"
                                    helpText="Dieser wert kann in jedem Anbaujahr angepasst werden. Kann Kosten für Versicherungen etc. beinhalten. " />
                                <modelvalue v-model="FF['FF_META'].economy.session_labour_eur_per_h" />


                            </v-expansion-panel-text>
                        </v-expansion-panel>
                    </v-expansion-panels>
                    <download_eco_report />
                   


                </v-expansion-panel-text>
            </v-expansion-panel>
        </v-expansion-panels>


        <v-expansion-panels variant="accordion" multiple>
            <!-- <v-expansion-panel v-for="(value, key, index) in FF" :key="index"
                :title="'Fruchtfolgefeld ' + key + ' ' + L(value.crop)"> -->
            <v-expansion-panel v-for="n in (Object.keys(FF).length - 1)" :key="n"
                :title="'Fruchtfolgefeld ' + n + ' ' + L(FF[n].crop)">
                <v-expansion-panel-text>

                    <v-expansion-panels variant="accordion">
                        <v-expansion-panel title="Leistungen">
                            <v-expansion-panel-text>
                                <modelvalue v-model="FF[n].MODELVALUES.yield_dt_fm_per_ha" />
                                <modelvalue v-model="FF[n].MODELVALUES.cropeconomy.price_yield_eur_per_dt_fm" />
                                <modelvalue v-model="FF[n].MODELVALUES.cropeconomy.yield_leistung_eur_per_ha" />

                                <modelvalue
                                    v-model="FF[n].MODELVALUES.cropeconomy.price_yield_grünfutter_eur_per_dt_fm" />
                                <modelvalue
                                    v-model="FF[n].MODELVALUES.cropeconomy.yield_grünfutter_leistung_eur_per_ha" />


                                <modelvalue v-model="FF[n].MODELVALUES.cropeconomy.price_yield_heu_eur_per_dt_fm" />
                                <modelvalue v-model="FF[n].MODELVALUES.cropeconomy.yield_heu_leistung_eur_per_ha" />

                                <modelvalue v-model="FF[n].MODELVALUES.cropeconomy.price_yield_silage_eur_per_dt_fm" />
                                <modelvalue v-model="FF[n].MODELVALUES.cropeconomy.yield_silage_leistung_eur_per_ha" />

                                <modelvalue v-model="FF[n].MODELVALUES.cropeconomy.other_leistung_eur_per_ha" />

                            </v-expansion-panel-text>
                        </v-expansion-panel>

                        <v-expansion-panel title="Saatgut">
                            <v-expansion-panel-text>

                                <div v-if="!('seed_u_per_ha' in FF[n].MODELVALUES)">
                                    <modelvalue v-model="FF[n].MODELVALUES.seed_kg_per_ha" />
                                    <modelvalue v-model="FF[n].MODELVALUES.cropeconomy.seed_cost_eur_per_kg" />
                                </div>
                                <div v-else>
                                    <modelvalue v-model="FF[n].MODELVALUES.seed_u_per_ha" />
                                    <modelvalue v-model="FF[n].MODELVALUES.cropeconomy.seed_cost_eur_per_u" />
                                </div>
                                <modelvalue v-model="FF[n].MODELVALUES.cropeconomy.seed_cost_eur_per_ha" />


                            </v-expansion-panel-text>
                        </v-expansion-panel>

                        <v-expansion-panel title="Sonstige Kosten">
                            <v-expansion-panel-text>
                                <modelvalue v-model="FF[n].MODELVALUES.cropeconomy.extra_cost_eur_per_ha" />


                            </v-expansion-panel-text>
                        </v-expansion-panel>


                    </v-expansion-panels>



                    <cover_crop_economy v-model="FF[n].MODELVALUES.cropeconomy.covercropeconomy"
                        v-if="FF[n].MODELVALUES && FF[n].MODELVALUES.cropeconomy && 'covercropeconomy' in FF[n].MODELVALUES.cropeconomy" />


                    <worksteplist v-model="FF[n].MODELVALUES.cropeconomy" v-if="FF[n].MODELVALUES && FF[n].MODELVALUES.cropeconomy"/>


                    <modelvalue v-model="FF[n].MODELVALUES.cropeconomy.gross_margin_eur_per_ha" v-if="FF[n].MODELVALUES && FF[n].MODELVALUES.cropeconomy"/>
                    <modelvalue v-model="FF[n].MODELVALUES.cropeconomy.gross_margin_per_man_hour_eur_per_h" v-if="FF[n].MODELVALUES && FF[n].MODELVALUES.cropeconomy"/>


                </v-expansion-panel-text>
            </v-expansion-panel>
        </v-expansion-panels>
    </div>
</template>
