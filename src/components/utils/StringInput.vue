<template>
  <div>
    <v-text-field
      :model-value="displayValue"
      :label="label"
      :rules="rules"
      :readonly="readonly"

      :hint="hint"
      persistent-hint
      type="text"
      @update:model-value="handleInput"
      @blur="handleBlur"
      @keydown.up.prevent="increment"
      @keydown.down.prevent="decrement"
      class="comma-numeric-input"
      :suffix="suffix"
    >
      <!-- Use append-inner slot for the buttons -->
      <template v-slot:append-inner>
        <div v-if="!nobtns" class="button-group">
          <v-btn v-if='resetbtn' icon @click="reset" class="arrow-button">
            <v-icon>mdi-reload</v-icon>
          </v-btn>
          <v-btn
            v-if="helpText"
            icon
            @click="showHelpDialog = true"
            class="help-button"
          >
            <v-icon>mdi-help</v-icon>
          </v-btn>
        </div>
      </template>
    </v-text-field>

    <!-- Help Dialog -->
    <v-dialog v-model="showHelpDialog" max-width="500">
      <v-card>
        <v-card-title>{{label}}</v-card-title>
        <v-card-text>
          <!-- Use v-html to render the helpText as HTML -->
          <div v-html="helpText"></div>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="showHelpDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
const emit = defineEmits(['send-reset']);


// Define the model for v-model binding
const modelValue = defineModel({
  type: String,
  default: '',
});

const props = defineProps({
  nobtns: {
    type: Boolean,
    default: false,
  },
  label: {
    type: String,
    default: 'String Input',
  },
  resetbtn: {
    type: Boolean,
    default: false,
  },
  readonly: {
    type: Boolean,
    default: false,
  },
  min: {
    type: Number,
    default: -Infinity,
  },
  max: {
    type: Number,
    default: Infinity,
  },
  
  suffix: {
    type: String,
    default: '',
  },
  step: {
    type: Number,
    default: 1,
  },
  rules: {
    type: Array,
    default: () => [],
  },
  helpText: {
    type: String,
    default: '',
  },
  hint: {
    type: String,
    default: '',
  },
});

const showHelpDialog = ref(false);

// Format the value for display (comma as decimal separator)
const formatValue = (value) => {
 
  return value
};

// Parse the value from display (comma to dot)
const parseValue = (value) => {
  
  return value;
};

// Clamp the value within min and max range
const clampValue = (value) => {
  return value
};

// Handle input events
const handleInput = (value) => {
  const parsedValue = parseValue(value);
  modelValue.value = clampValue(parsedValue);
};

// Handle blur events
const handleBlur = () => {
  if (displayValue.value === '') {
    modelValue.value = null; // Set modelValue to null if input is empty
  } else {
    const parsedValue = parseValue(displayValue.value);
    modelValue.value = clampValue(parsedValue);
  }
};

// Increment the value
const increment = () => {
  const currentValue = modelValue.value || 0; // Default to 0 if modelValue is null
  const newValue = clampValue(parseFloat((currentValue + props.step).toFixed(6)));
  modelValue.value = newValue;
};

// Decrement the value
const decrement = () => {
  const currentValue = modelValue.value || 0; // Default to 0 if modelValue is null
  const newValue = clampValue(parseFloat((currentValue - props.step).toFixed(6)));
  modelValue.value = newValue;
};

const reset = () => {
  emit('send-reset');

};

// Watch for changes to modelValue and format it for display
const displayValue = ref(formatValue(modelValue.value));
watch(modelValue, (newValue) => {
  displayValue.value = formatValue(newValue);
});
</script>

<style scoped>
.comma-numeric-input {
  position: relative;
}

.button-group {
  display: flex;
  align-items: center;
  gap: 4px; /* Space between the buttons */
}
 

.arrow-button {
  margin: 0;
  padding: 0;
  background-color: transparent !important; /* Make buttons transparent */
  box-shadow: none !important; /* Remove shadow */
}
 

.help-button {
  margin: 0;
  padding: 0;
  background-color: transparent !important; /* Make buttons transparent */
  box-shadow: none !important; /* Remove shadow */
}
</style>