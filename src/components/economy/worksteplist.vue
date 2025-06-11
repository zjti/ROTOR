<script setup>

const model = defineModel();

</script>

<template>
    <v-expansion-panels variant="accordion">
        <v-expansion-panel title="Arbeitsgänge">
            <v-expansion-panel-text>
                <modelvalue v-model="model.sum_machine_cost_eur_per_ha" />
                <modelvalue v-model="model.sum_diesel_cost_eur_per_ha" />
                <modelvalue v-model="model.sum_man_hours_per_ha" />

                <v-expansion-panels variant="accordion" multiple>
                    <v-expansion-panel v-for="(value, key, index) in model.worksteplist" :key="index" :title="  key  ">
                        <v-expansion-panel-text>
                                <workstep v-model = model.worksteplist[key] />

                        </v-expansion-panel-text>
                    </v-expansion-panel>

                </v-expansion-panels>

                
                
            </v-expansion-panel-text>
        </v-expansion-panel>

    </v-expansion-panels>
</template>
