
<template>
    <div v-if="isLoading" class="pyodide-loader">
      <div class="loader-content">
        <div class="spinner"></div>
        <p>Loading Cropcode...</p>
        <p v-if="progress">{{ progress }}</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import usePyodide from '@/composables/usePyodide';
  
  const { isLoading } = usePyodide();
  const progress = ref('Initializing...');
  
  onMounted(async () => {
    // You can add progress updates if needed
    setTimeout(() => progress.value = 'Downloading Cropdata...', 1500);
  });
  </script>
  
  <style scoped>
  .pyodide-loader {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
    color: white;
  }
  
  .loader-content {
    text-align: center;
  }
  
  .spinner {
    border: 4px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top: 4px solid #42b983;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 0 auto 20px;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  </style>