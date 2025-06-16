import { downloadFiles } from '@/utils/fileDownloader';
import { usePyodideSync } from './usePyodideSync';
import usePyodide from '@/composables/usePyodide';

export function usePyodideInit() {
  const { pyodide, runPythonS } = usePyodide();

  

  const { triggerSync, initSync } = usePyodideSync(pyodide);

  const initialize = async (fileManifestUrl) => {
    await pyodide.value.runPythonAsync(`
      import os
      import sys
      import importlib
      
      `)

    await pyodide.value.loadPackage('micropip')
    await pyodide.value.runPythonAsync("import micropip")
    // // await pyodide.value.runPythonAsync("micropip.install('reportlab')")
    await pyodide.value.runPythonAsync("micropip.install('./chardet-5.2.0-py3-none-any.whl')")

    await pyodide.value.runPythonAsync("micropip.install('./numpy-2.0.2-cp312-cp312-pyodide_2024_0_wasm32.whl')")

    await pyodide.value.runPythonAsync("micropip.install('./pillow-10.2.0-cp312-cp312-pyodide_2024_0_wasm32.whl')")
    await pyodide.value.runPythonAsync("micropip.install('./reportlab-4.4.1-py3-none-any.whl')")
    // https://files.pythonhosted.org/packages/38/6f/f5fbc992a329ee4e0f288c1fe0e2ad9485ed064cac731ed2fe47dcc38cbf/chardet-5.2.0-py3-none-any.whl
    // await pyodide.value.runPythonAsync("micropip.install('./scipy-1.14.1-cp312-cp312-pyodide_2024_0_wasm32.whl')")
    
    
    // ROTOR/public/
    // await pyodide.value.runPythonAsync("micropip.install('./reportlab-4.4.1-py3-none-any.whl')")

    // await pyodide.value.runPythonAsync("micropip.install('numpy')")
    await pyodide.value.runPythonAsync("micropip.install('scipy')")
    

  
    

    // 1. Download missing files
    window.updateFiles = async () => {await downloadFiles(fileManifestUrl)}
    await downloadFiles(fileManifestUrl);

    await initSync();
    // 2. Trigger sync with Pyodide
    await triggerSync();

    // 3. post initialization
    await pyodide.value.runPythonAsync(`
      import json
      
      try:
          from ROTOR.utils.autoreload import autoreload
      except:
          print("could not load 'autoreload'")
          autoreload = lambda : None
      
      from ROTOR.utils.js import jswrapper 
      from ROTOR.utils import config  
      
      
    `);
    console.log('Pyodide initialized ');
  };

  return { initialize };
}