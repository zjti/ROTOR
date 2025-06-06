import { downloadFiles } from '@/utils/fileDownloader';
import { usePyodideSync } from './usePyodideSync';
import usePyodide from '@/composables/usePyodide';

export function usePyodideInit() {
  const { pyodide, runPythonS } = usePyodide();

  // runPythonS(`
  //     import os
  //     import sys
  //     import importlib`)
  


  const { triggerSync, initSync } = usePyodideSync(pyodide);

  const initialize = async (fileManifestUrl) => {
    await pyodide.value.runPythonAsync(`
      import os
      import sys
      import importlib
      
      `)

    pyodide.value.loadPackage('micropip')

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