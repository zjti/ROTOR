<template>
    <v-dialog v-model="dialog" max-width="600">
      <template v-slot:activator="{ props }">
        <v-btn color="primary" v-bind="props">
          Fruchfolge laden
        </v-btn>
      </template>
  
      <v-card>
        <v-card-title>Fruchtfolge öffnen</v-card-title>
        
        <v-card-text>
          <v-file-input
            v-model="file"
            label="Datei auswählen"
            prepend-icon="mdi-code-json"
            accept=".json,application/json"
            @change="onFileChange"
            :error-messages="error"
            clearable
          ></v-file-input>
  
           
  
          <v-alert
            v-if="uploadSuccess"
            type="success"
            class="mt-4"
          >
            Allesgut, Sie können den Dialog schließen
          </v-alert>
  
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
            @click="uploadAndOverwrite"
            :disabled="!file"
            :loading="uploading"
          >
            Laden
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { globalStore } from '@/utils/globalstore'

  
  const dialog = ref(false);
  const file = ref(null);
  const error = ref('');
  const uploadSuccess = ref(false);
  const uploading = ref(false);
  const foundKeys = ref([]);
  const updatedKeys = ref([]);
  
  const onFileChange = () => {
    error.value = '';
    uploadSuccess.value = false;
    foundKeys.value = [];
  };
  
  const uploadAndOverwrite = async () => {
    if (!file.value) return;
  
    uploading.value = true;
    error.value = '';
    updatedKeys.value = [];
  
    try {
      const fileContent = await readFileAsText(file.value);
      const jsonData = JSON.parse(fileContent);
  
      if (typeof jsonData !== 'object' || jsonData === null) {
        throw new Error('File must contain a JSON object (dictionary)');
      }
  
      foundKeys.value = Object.keys(jsonData);
      
      if (foundKeys.value.length === 0) {
        throw new Error('No keys found in the JSON dictionary');
      }
  
      // Process each key in the uploaded JSON
      for (const key of foundKeys.value) {
        if (jsonData[key] !== undefined) {
          
          localStorage.setItem(key, JSON.stringify(jsonData[key]));
          globalStore.get(key).value = jsonData[key]

          updatedKeys.value.push(key);
        }

      }
  
      uploadSuccess.value = true;
      file.value = null;
      
    } catch (err) {
      error.value = `Upload failed: ${err.message}`;
      console.error('Upload error:', err);
    } finally {
      uploading.value = false;
    }
  };
  
  function readFileAsText(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => resolve(e.target.result);
      reader.onerror = (e) => reject(new Error('Failed to read file'));
      reader.readAsText(file);
    });
  }
  </script>