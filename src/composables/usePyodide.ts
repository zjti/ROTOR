import { ref } from 'vue';
import { loadPyodide } from 'pyodide';
import { usePyodideSync } from './usePyodideSync';
import { usePyodideInit } from './usePyodideInit';


const pyodideInstance = ref<any>(null);
const isLoading = ref(false);
const error = ref<Error | null>(null);

export default function usePyodide() {
  const initializePyodide = async () => {
    if (pyodideInstance.value) return pyodideInstance.value;
    
    isLoading.value = true;
    try {
      // Add artificial delay (3 seconds)
      // await new Promise(resolve => setTimeout(resolve, 9000));
      
      pyodideInstance.value = await loadPyodide({
        indexURL: "https://cdn.jsdelivr.net/pyodide/v0.27.4/full/"
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