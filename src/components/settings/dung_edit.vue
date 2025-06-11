<template>
  
  <v-select
    v-model="selectedKey"
    :items="Object.keys(dung_data).concat('Dünger hinzufügen')"
    :label="langf('SELECT_ENTRY')"
    @change="loadData"
  ></v-select>

  <Formview :block="cur_dung" ref="my_form"> </Formview>
</template>
  
<script setup>
import { globalStore } from '@/utils/globalstore'
import { langf } from "@/main.js";

 

</script>
  <script>
import { ref, reactive ,computed} from "vue";
 export default {
  data() {
    return {
      dung_data: globalStore.get("DUNG_DATA"),
      format: {
        TM: { type: "float", unit: "%" },
        "N/FM": { type: "float", unit: "kg/t FM" },
        Navil_spring: { type: "float", unit: "%" },
        Navil_autumn: { type: "float", unit: "%" },
        Nloss: { type: "float", unit: "%" },
        "P/FM": { type: "float", unit: "kg/t FM" },
        "K/FM": { type: "float", unit: "kg/t FM" },
        "HUMUS_HE": { type: "float", unit: "HE" },
        "PREIS_EUR_PER_T": { type: "float", unit: "€/t" },
      },

      selectedKey: null,
      newKey: "",
    };
  },
  computed: {
    cur_dung() {
      
      const original = this.dung_data[this.selectedKey];
      const transformed = reactive({});

      for (const key in original) {
        console.log(key)
        // Create a computed property for top-level values
        transformed[key] = reactive({
          default: computed({
            get: () => original[key],
            set: (newValue) => {
              original[key] = newValue;
            },
          }),
          // default:0,
          unit: this.format[key].unit,
          type: this.format[key].type
        });
      }
      return transformed;
    },
  },
  methods: {
    // Load data for the selected key
    loadData() {
      if (this.selectedKey !== "new") {
        this.currentData = JSON.parse(
          JSON.stringify(this.jsonData[this.selectedKey])
        );
      } else {
        this.currentData = {};
      }
    },
    // Save changes to the JSON data
    saveChanges() {
      this.$set(this.jsonData, this.selectedKey, this.currentData);
      this.$root.$toast.success("Changes saved successfully!", {
        timeout: 2000,
      });
    },
    // Duplicate the current entry
    duplicateEntry() {
      const newKey = `${this.selectedKey}_copy`;
      this.jsonData[newKey] = JSON.parse(JSON.stringify(this.currentData));
      this.selectedKey = newKey;
      this.loadData();
      this.$root.$toast.info("Entry duplicated successfully!", {
        timeout: 2000,
      });
    },
    // Create a new entry
    createNewEntry() {
      if (this.newKey) {
        this.jsonData[this.newKey] = {
          TM: [0, "%"],
          "N/FM": [0, "kg/t"],
          Navil_spring: [0, "%"],
          Navil_autumn: [0, "%"],
          Nloss: [0, "%"],
          "P/FM": [0, "kg/t"],
          "K/FM": [0, "kg/t"],
        };
        this.selectedKey = this.newKey;
        this.loadData();
        this.newKey = "";
        this.$root.$toast.success("New entry created successfully!", {
          timeout: 2000,
        });
      } else {
        this.$root.$toast.error("Please enter a valid key.", { timeout: 2000 });
      }
    },
  },
};
</script>
  
  <style scoped>
.v-table {
  width: 100%;
}
</style>