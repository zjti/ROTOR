<script setup>

const model = defineModel();

</script>

<template>
    <div>
        <modelvalue v-model="model.get_name"/>

        <modelvalue v-model="model.get_date"/>
        <modelvalue v-model="model.get_man_hours_h_per_ha"/>
        <modelvalue v-model="model.get_machine_cost_eur_per_ha"/>
        <modelvalue v-model="model.get_diesel_l_per_ha"/>
        <modelvalue v-model="model.get_diesel_eur_per_ha"/>
        <modelvalue v-model="model.get_session_labour_h_per_ha"/>
        
    </div>
</template>
