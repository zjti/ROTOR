import { ref } from 'vue';
import { loadPyodide } from 'pyodide';
import { usePyodideSync } from './usePyodideSync';
import { usePyodideInit } from './usePyodideInit';



const pyodideInstance = ref<any>(null);
const isLoading = ref(false);
const error = ref<Error | null>(null);

export async function loadLocalPyodide() {
  // Check if already loaded
  if (window.loadPyodide) return window.loadPyodide;

  // Dynamically load pyodide.js from public/pyodide/
  await new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = "./pyodide/pyodide.js";
    script.onload = () => resolve();
    script.onerror = reject;
    document.head.appendChild(script);
  });

  // Return global loadPyodide now that it's loaded
  return window.loadPyodide;
}


export default function usePyodide() {

   

  const initializePyodide = async () => {
    if (pyodideInstance.value) return pyodideInstance.value;
    
    isLoading.value = true;
    try {
      
      // const loadPyodide = await loadLocalPyodide();

      pyodideInstance.value = await loadPyodide({
        indexURL: "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/"
        // indexURL: "./pyodide/"
      });
 
        
      const { initialize } = usePyodideInit();
      await initialize('/ROTOR/files-manifest.json');  

      return pyodideInstance.value;
      
      
    } catch (err) {
      error.value = err as Error;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  return {
    pyodide: pyodideInstance,
    isLoading,
    error,
    initializePyodide,
    runPython: async (code: string) => {
      if (!pyodideInstance.value) {
        // await initializePyodide();
      }
      return await pyodideInstance.value.runPythonAsync(code);
    },
    runPythonS: (code: string) => {
      return pyodideInstance.value.runPython(code);
    }
  };
}