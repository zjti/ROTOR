
<template>
  <div class="grid-container">
    <!-- Horizontal Axis Label (Above Top Labels) -->
    <div class="horizontal-axis-label">
      {{ horizontalAxisLabel }}
    </div>

    <!-- Top Labels (Vertical) -->
    <div class="top-labels">
      <div class="label-spacer"></div> <!-- Spacer for the left labels -->
      <div
        v-for="(label, index) in fixedColumnOrder || topLabels"
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
          v-for="(label, index) in leftLabels"
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
          v-for="(rowLabel, rowIndex) in leftLabels"
          :key="rowIndex"
          class="grid-row"
        >
          <div
            v-for="(colLabel, colIndex) in fixedColumnOrder || topLabels"
            :key="colIndex"
            class="grid-cell"
            :style="{ width: cellSize + 'px', height: cellSize + 'px' }"
            @click="handleCellClick(rowLabel, colLabel)"
          >
            <!-- Display the delay or checkmark based on dataType -->
            <template v-if="dataType === 'number'">
              {{ getDelay(rowLabel, colLabel) }}
            </template>
            <template v-else-if="dataType === 'boolean'">
              <span v-if="getDelay(rowLabel, colLabel) === true">✔</span>
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script>
export default {
  props: {
    cellSize: {
      type: Number,
      default: 30, // Default cell size in pixels
    },
    horizontalAxisLabel: {
      type: String,
      default: "Horizontal Axis Label", // Default horizontal axis label
    },
    verticalAxisLabel: {
      type: String,
      default: "Vertical Axis Label", // Default vertical axis label
    },
    delayData: {
      type: Object,
      required: true, // The dictionary containing delay values
    },
    fixedColumnOrder: {
      type: Array, // Array of strings to fix the column order
      default: null, // If not provided, use dynamic order
    },
    dataType: {
      type: String, // 'number' or 'boolean'
      default: "number", // Default to number
      validator: (value) => ["number", "boolean"].includes(value), // Validate prop
    },
  },
  computed: {
    // Left labels (y-axis) are the top-level keys of delayData
    leftLabels() {
      return Object.keys(this.delayData);
    },
    // Top labels (x-axis) are the nested keys of delayData or fixedColumnOrder
    topLabels() {
      if (this.fixedColumnOrder) {
        return this.fixedColumnOrder;
      }
      const nestedKeys = new Set();
      for (const row of Object.values(this.delayData)) {
        for (const key of Object.keys(row)) {
          nestedKeys.add(key);
        }
      }
      return Array.from(nestedKeys);
    },
  },
  methods: {
    handleCellClick(rowLabel, colLabel) {
      if (this.dataType === "number") {
        // Get the current delay value
        const currentDelay = this.getDelay(rowLabel, colLabel);

        // Open a prompt to allow the user to input a new delay value
        const newDelay = prompt(
          `Enter new value ${rowLabel} -> ${colLabel}:`,
          currentDelay
        );

        // If the user provides a valid input, update the delayData
        if (newDelay !== null && !isNaN(newDelay)) {
          this.updateDelay(rowLabel, colLabel, parseFloat(newDelay));
        }
      } else if (this.dataType === "boolean") {
        // Toggle the boolean value
        const currentValue = this.getDelay(rowLabel, colLabel);
        console.log(currentValue)
        this.updateDelay(rowLabel, colLabel, !currentValue);
      }
    },
    getDelay(rowLabel, colLabel) {
      // Retrieve the delay for the given row and column labels
      if (
        this.delayData[rowLabel] &&
        this.delayData[rowLabel][colLabel]
      ) {
        if (this.dataType === "number" && this.delayData[rowLabel][colLabel].value === 0) {
          return "0";
        }
        return this.delayData[rowLabel][colLabel].value;
      }
      return this.dataType === "number" ? "-" : false; // Return default value based on dataType
    },
    updateDelay(rowLabel, colLabel, newDelay) {
      // Ensure reactivity by using Vue.set or this.$set
      if (!this.delayData[rowLabel]) {
        this.delayData[rowLabel] = {};
      }
      this.delayData[rowLabel][colLabel] = { value: newDelay };
      console.log(rowLabel, colLabel, newDelay);
      console.log(this.delayData);
      // Emit an event to notify the parent component of the change
      this.$emit("delay-updated", this.delayData);
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