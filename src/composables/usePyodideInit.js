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

    // 1. Download missing files
    await downloadFiles(fileManifestUrl);

    await initSync();
    // 2. Trigger sync with Pyodide
    await triggerSync();

    // 3. Verify initialization
    const rootFiles = await pyodide.value.runPythonAsync(`
      import json
      
      try:
          from autoreload import autoreload
      except:
          autoreload = lambda x: None
     
      try:
          import config 
          from pyodide.ffi import to_js
          import ff.restrictions

          from ff.calc_opts import calc_opts 
          os.listdir('/')

          import ff
      except:
          pass
          
      def updateFF(f):
        return json.dumps(ff.updateFF(f.to_py()))

    
      def updateFFlength(f,jahre):
        return json.dumps(ff.updateFFlength(f.to_py(),jahre))

      def get_avail_crops_for_jahr(ffolge, jahr):
        x = ff.restrictions.get_avail_crops_for_jahr(ffolge.to_py(), jahr)
        return x

      
    `);
    console.log('Pyodide initialized with files:', rootFiles);
  };

  return { initialize };
}