<script  >
import vuetify from "../../plugins/vuetify";
import bkr_select from "./bkr_select.vue"; // Import your custom component
import NumberInput from "./NumberInput.vue";
import StringInput from "./StringInput.vue";
 
export default {
  components: {
    NumberInput,StringInput,
    bkr_select,
     
    
  },
  props: {
    block: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      typemap: {
        int: "NumberInput",
        float: "NumberInput", //"v-number-input",
        string: "StringInput",
        boolean: "v-switch",
        bkr_int: "bkr_select",
      },
    };
  },

  computed: {
    filteredBlock() {
      // Filter out keys that start with "___" or have vis property set to false
      return Object.fromEntries(
        Object.entries(this.block).filter(([key, value]) => {
          // Exclude keys starting with "___"
          const excludeKey = key.startsWith("___");
          // Exclude if the value is an object and has vis: false
          const excludeVis =
            typeof value === "object" && value !== null && value.vis === false;
          // Keep the entry if neither condition is met
          return !excludeKey && !excludeVis;
        })
      );
    },
  },
};
</script>

<template>
  <div class="flex-container">
    <div :key="prop" v-for="(opts, prop) in filteredBlock" class="flex-item">
      <component
        class="custom-label-color w-100"
        v-if="opts['type'] in typemap"
        :label="L(prop)"
        :is="typemap[opts['type']]"
        v-model="opts['default']"
        :suffix="opts['unit']"
        :helpText="'help' in opts ? L(opts['help']) : null"
      />
      <v-select
        v-if="opts['type'] == 'select'"
        class="custom-label-color w-100"
        :label="L(prop)"
        :items="
          opts['items'].map((key) => ({
            value: key,
            title: L(key),
          }))
        "
        v-model="opts['default']"
      ></v-select>
      <component
        v-if="opts['type'] != 'select' && !(opts['type'] in typemap)"
        :is="opts['type']"
        :label="L(prop)"
        :data="{ '123': 'aa' }"
      />
    </div>
  </div>
</template>


<style scoped>
.flex-container {
  display: flex;
  flex-wrap: wrap;
  gap: 2px; /* Space between items */
}

/* For wider screens: 2 items per row with equal width */
@media (min-width: 768px) {
  .flex-item {
    flex: 1 1 calc(50% - 1px); /* Equal width, accounting for gap */
  }
}

/* For smaller screens: 1 item per row */
@media (max-width: 767px) {
  .flex-item {
    flex: 1 1 100%;
  }
}

.flex-item {
  padding: 2px;
  /* border: 1px solid #ccc; Optional: Add borders for visual clarity */
  text-align: center;
}
</style>
