
<template>
  <v-select
    v-model="restrctions_select"
    :items="all_restrictions"
    label="Resrictions"
  ></v-select>

  <div style="overflow-x: auto">
    <div class="grid-container">
      <!-- Horizontal Axis Label (Above Top Labels) -->
      <div class="horizontal-axis-label">
        {{ horizontalAxisLabel }}
      </div>

      <!-- Top Labels (Vertical) -->
      <div class="top-labels">
        <div class="label-spacer"></div>
        <!-- Spacer for the left labels -->
        <div
          v-for="(label, index) in labels"
          :key="index"
          class="top-label"
          :style="{ width: cellSize + 'px' }"
        >
          <l>{{ label }}</l>
        </div>
      </div>

      <!-- Main Grid Area -->
      <div class="grid-area">
        <!-- Vertical Axis Label (Left of Left Labels) -->
        <div class="vertical-axis-label">
          {{ verticalAxisLabel }}
        </div>

        <!-- Left Labels (Horizontal) -->
        <div class="left-labels">
          <div
            v-for="(label, index) in labels"
            :key="index"
            class="left-label"
            :style="{ height: cellSize + 'px' }"
          >
            <l>{{ label }}</l>
          </div>
        </div>

        <!-- Grid Cells -->
        <div class="grid">
          <div
            v-for="(rowLabel, rowIndex) in labels"
            :key="rowIndex"
            class="grid-row"
          >
            <div
              v-for="(colLabel, colIndex) in labels"
              :key="colIndex + '_' + rowIndex"
              class="grid-cell"
              :style="{ width: cellSize + 'px', height: cellSize + 'px' }"
              @click="handleCellClick(rowLabel, colLabel)"
            >
              <!-- Display the delay if it exists -->
              {{ getDelay(rowLabel, colLabel) }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script setup>
import { ref } from "vue";
import { globalStore } from '@/utils/globalstore'

import crops from "@/assets/crops.json";
 
</script>

<script>
export default {
  data() {
    return {
      data_delayData: globalStore['PHYTO_DELAY'],
      data_delayData_time: globalStore['PHYTO_DELAY_TIME'],
      restrctions_select: ref("Phyto"),
      all_restrictions: ["Phyto", "Zeit"],
    };
  },
  computed: {
    delayData() {
      return { Phyto: this.data_delayData, Zeit: this.data_delayData_time }[
        this.restrctions_select
      ];
    },

    labels() {
      return Object.keys(crops);
    },
  },
  props: {
    //   labels: {
    //     type: Array,
    //     required: true,
    //   },
    cellSize: {
      type: Number,
      default: 30, // Default cell size in pixels
    },
    horizontalAxisLabel: {
      type: String,
      default: "Nachfrucht", // Default horizontal axis label
    },
    verticalAxisLabel: {
      type: String,
      default: "Vorfrucht", // Default vertical axis label
    },
    //   delayData: {
    //     type: Object,
    //     required: true, // The dictionary containing delay values
    //   },
  },
  methods: {
    handleCellClick(rowLabel, colLabel) {
      // Get the current delay value
      const currentDelay = this.getDelay(rowLabel, colLabel);

      // Open a prompt to allow the user to input a new delay value
      const newDelay = prompt(
        `Enter new delay for ${rowLabel} -> ${colLabel}:`,
        currentDelay
      );

      // If the user provides a valid input, update the delayData
      if (newDelay !== null && !isNaN(newDelay)) {
        this.updateDelay(rowLabel, colLabel, parseFloat(newDelay));
      }
    },
    getDelay(rowLabel, colLabel) {
      // Retrieve the delay for the given row and column labels
      if (this.delayData[rowLabel] && this.delayData[rowLabel][colLabel]) {
        return this.delayData[rowLabel][colLabel].delay;
      }
      return ""; // Return empty string if no delay is found
    },
    updateDelay(rowLabel, colLabel, newDelay) {
      // Update the delayData object with the new delay value
      if (!this.delayData[rowLabel]) {
        this.delayData[rowLabel] = {};
      }
      this.delayData[rowLabel][colLabel] = { delay: newDelay };
    },
  },
};
</script>
  
  <style scoped>
.grid-container {
  display: inline-block; /* Center the grid container */
  text-align: center; /* Center the content inside the container */
}

.horizontal-axis-label {
  margin-inline: auto; /* Center the horizontal axis label */
  margin-bottom: 10px; /* Space between axis label and top labels */
  font-weight: bold;
}

.top-labels {
  display: flex;
  margin-left: 100px; /* Adjust based on your left labels width */
}

.top-label {
  writing-mode: vertical-lr;
  transform: rotate(220deg);
  text-align: left; /* Align text to the left */
  display: flex;
  align-items: flex-start; /* Align text to the top */
  justify-content: flex-start; /* Align text to the left */
  width: 50px; /* Fixed width for top labels */
  white-space: nowrap; /* Prevent text from wrapping */
}

.label-spacer {
  width: 120px; /* Same as left-labels width */
}

.grid-area {
  display: flex;
}

.vertical-axis-label {
  writing-mode: vertical-lr;
  transform: rotate(180deg);
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px; /* Adjust based on your design */
  margin-right: 10px; /* Space between axis label and left labels */
  font-weight: bold;
}

.left-labels {
  display: flex;
  flex-direction: column;
  width: 150px; /* Adjust based on your design */
}

.left-label {
  text-align: right;
  padding-right: 10px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  height: 30px; /* Fixed height for left labels */
}

.grid {
  display: flex;
  flex-direction: column;
}

.grid-row {
  display: flex;
}

.grid-cell {
  border: 1px solid #000;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px; /* Fixed width for grid cells */
  height: 30px; /* Fixed height for grid cells */
}

.grid-cell:hover {
  background-color: #f0f0f0;
}
</style>