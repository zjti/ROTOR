<template>
    <div>
      <!-- Download button that triggers the dialog -->
      <v-btn color="primary" @click="dialog = true">Report als PDF speichern</v-btn>
  
      <!-- Filename input dialog -->
      <v-dialog v-model="dialog" max-width="500">
        <v-card>
          <v-card-title>Dateiname festlegen</v-card-title>
          
          <v-card-text>
            <v-text-field
              v-model="filename"
              label="Dateiname" 
              persistent-hint
              :rules="[v => !!v || 'Dateiname benötigt']"
              @keyup.enter="startDownload"
            ></v-text-field>
          </v-card-text>
  
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="dialog = false">Zurück</v-btn>
            <v-btn 
              color="primary" 
              @click="startDownload"
              :disabled="!filename"
              :loading="downloading"
            >
              Download
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import usePyodide from "@/composables/usePyodide";

  const { pyodide, runPythonS, runPython } = usePyodide();
  const dialog = ref(false);
  const filename = ref('eco_report');
  const downloading = ref(false);
  
  const startDownload = async () => {
    if (!filename.value) return;
    
    downloading.value = true;
    try {
      await downloadPdf();
      dialog.value = false;
    } catch (error) {
      console.error('Download failed:', error);
    } finally {
      downloading.value = false;
    }
  };
  
  const downloadPdf = async () => {
    const file_bytes = await runPythonS(`jswrapper.JSdownload_eco_report()`);
    console.log(file_bytes);
    
    const uint8Array = new Uint8Array(file_bytes);
    const blob = new Blob([uint8Array], { type: "application/pdf" });
    
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    
    // Use the entered filename, adding .pdf if not already present
    const downloadName = filename.value.endsWith('.pdf') 
      ? filename.value 
      : `${filename.value}.pdf`;
    
    link.download = downloadName;
    link.click();
    
    // Clean up
    URL.revokeObjectURL(link.href);
  };
  </script>