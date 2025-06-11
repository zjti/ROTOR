<script setup>
import { ref, watchEffect, getCurrentInstance, watch } from "vue";
import usePyodide from "@/composables/usePyodide";
import { useStorage, watchPausable } from "@vueuse/core";
import { globalStore } from '@/utils/globalstore'


const model = defineModel();

</script>

<template>
    <v-expansion-panels variant="accordion">
    <v-expansion-panel title="Arbeitsschritte">
        <v-expansion-panel-text>
         
        <worksteplist v-model="model.worksteplist"/>


        </v-expansion-panel-text>
    </v-expansion-panel>
    
    </v-expansion-panels>
</template>
