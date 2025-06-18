<template>
    <v-dialog v-model="dialog" max-width="600">
      <template v-slot:activator="{ props }">
        <v-btn color="primary" v-bind="props" style="width:100%" >
          Fruchtfolge Speichern
        </v-btn>
      </template>
  
      <v-card>
        <v-card-title>Fruchtfolge Speichern</v-card-title>
        
        <v-card-text>
           
  
          <v-text-field
            v-model="downloadFileName"
            label="Dateiname"
            variant="outlined"
            class="mt-4"
            hint="Dateiendung (.json) wird automatisch hinzugefügt"
            persistent-hint
          ></v-text-field>
  
          <v-alert
            v-if="error"
            type="error"
            class="mt-4"
          >
            {{ error }}
          </v-alert>
        </v-card-text>
  
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue-darken-1"
            variant="text"
            @click="dialog = false"
          >
            Zurück
          </v-btn>
          <v-btn
            color="blue-darken-1"
            variant="text"
            @click="downloadCombinedJson"
            :disabled="selectedKeys.length === 0"
          >
            Download
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>
  
  <script setup>
  import { ref, watch } from 'vue';

  const keys = ['FFOLGE_NJAHRE', 'KRAUT_KEY','CLIMATE_DATA_MONTLY','LOCATION_LAT_LONG','EVAL_DATA','FF','DUNG_DATA',
    'VERKRAUTUNG','KRAUT_KEY','PHYTO_DELAY','PHYTO_DELAY_TIME','SOIL','PARAMS_USER'
  ]
  const props = defineProps({
    // Array of keys that should be available for download
     
    // If true, users can't modify the key selection (only select from provided keys)
    fixedKeys: {
      type: Boolean,
      default: false
    }
  });
  
  const dialog = ref(false);
  const selectedKeys = ref([...keys]); // Initialize with provided keys
  const availableKeys = ref([...keys]);
  const downloadFileName = ref('fruchtfolge_export');
  const error = ref('');
  
  function downloadCombinedJson() {
    try {
      const combinedData = {};
      let hasData = false;
      
      selectedKeys.value.forEach(key => {
        const item = localStorage.getItem(key);
        if (item) {
          hasData = true;
          try {
            combinedData[key] = JSON.parse(item);
          } catch {
            combinedData[key] = item; // Fallback to raw string if not JSON
          }
        }
      });
  
      if (!hasData) {
        error.value = 'missing storage key';
        return;
      }
  
      // Create download
      const jsonStr = JSON.stringify(combinedData, null, 2);
      const blob = new Blob([jsonStr], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      
      // Determine filename
      let filename = downloadFileName.value.trim();
      if (!filename.endsWith('.json')) {
        filename += '.json';
      }
      
      // Trigger download
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
      
      dialog.value = false;
    } catch (err) {
      error.value = 'Download failed: ' + err.message;
    }
  }
  </script>