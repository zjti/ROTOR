<script setup>
import { ref, watchEffect, getCurrentInstance, watch } from "vue";
import usePyodide from "@/composables/usePyodide";
import { useStorage, watchPausable } from "@vueuse/core";
import { globalStore } from '@/utils/globalstore'


const model = defineModel();

</script>

<template>
    <v-expansion-panels variant="accordion">
    <v-expansion-panel title="Zwischenfrucht Ökonomie">
        <v-expansion-panel-text>
        <modelvalue v-model="model.cover_crop_seed_kg_per_ha" />
        <modelvalue v-model="model.cover_crop_seed_cost_eur_per_kg" />
        <modelvalue v-model="model.cover_crop_seed_cost_eur_per_ha" />

        <!-- <worksteplist v-model="model.worksteplist"/> -->


        </v-expansion-panel-text>
    </v-expansion-panel>
    
    </v-expansion-panels>
</template>
