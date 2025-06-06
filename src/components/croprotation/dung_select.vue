<template>
  <v-row 
    ><v-col>
      <v-card elevation="0" >
        <v-card-item>
          <v-card-title> Düngerauswahl: </v-card-title>
          <v-card-subtitle> Bitte  </v-card-subtitle>
        </v-card-item>
        <v-card-text>
          <v-select
            v-model="selectedItems"
            :items="Object.keys(itemsDict)"
            label="Dünger auwählen"
            multiple
            outlined
            class="always-placeholder"
            :menu-props="{ closeOnContentClick: false }"
            ref="mySelect"
            @update:modelValue="closeDropdown"
            ><template v-slot:selection="{}"
              >.
              <!-- Empty template to hide selected items -->
            </template></v-select
          >
        </v-card-text></v-card
      ></v-col
    ><v-col>
      <v-table v-if="selectedItems.length > 0">
        <tbody>
          <tr v-for="item in selectedItems" :key="item">
            <td>
              <NumberInput
                v-model="amounts[item].menge"
                class="custom-label-color"
                :label="item"
                style="width: 100%"
                hide-details="auto"
                suffix="t/ha"
              />
              <v-checkbox label="Standardgabe im Frühjahr sonst Herbstgabe auswählen" v-if="has_herbst_gabe" v-model='amounts[item].is_herbst' style="width: 100%"
              />
            </td>
          </tr>
        </tbody>
      </v-table> </v-col
  ></v-row>
</template>
  
  <script setup>
import { computed, useTemplateRef } from "vue";
import NumberInput from "@/components/utils/NumberInput.vue";
import { globalStore } from '@/utils/globalstore'

const mySelect = useTemplateRef("mySelect");


const props = defineProps({
  amounts: {
    type: Object,
    required: true,
  },
  has_herbst_gabe: {
    type: Boolean,
    required: true,
  },
});

const itemsDict = globalStore.get("DUNG_DATA");

const selectedItems = computed({
  get: () => {
    console.log(Object.keys(props.amounts));
    return Object.keys(props.amounts);
  },
  set: (newVal) => {
    console.log('DM',newVal)
    newVal.forEach((item) => {
      if (!props.amounts[item]) {
        console.log('i',item,props.amounts)
        props.amounts[item] = {menge:0, is_herbst:false}; // Directly assign the value
      }
    });
    Object.keys(props.amounts).forEach((item) => {
      if (!newVal.includes(item)) {
        delete props.amounts[item]; // Directly delete the property
      }
    });
  },
});

const closeDropdown = () => {
  // Close the dropdown menu
  console.log("cd", mySelect);
  if (mySelect.value.menu) {
    mySelect.value.menu = false;
  }
};
</script>
  
  <style scoped>
</style>