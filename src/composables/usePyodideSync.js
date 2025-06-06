import { watch, onUnmounted } from 'vue';
import usePyodide from "@/composables/usePyodide";


export function usePyodideSync(pyodideRef) {
  let isProcessing = false;
  const changeQueue = new Set();
  const {pyodide, runPythonS, runPython } = usePyodide();


  // ================= CORE FUNCTIONS =================
  const ensureParentDirs = async (pyodide, fullPath) => {
    const dirs = fullPath.split('/').slice(0, -1);
    let currentPath = '';
    
    for (const dir of dirs) {
      currentPath = currentPath ? `${currentPath}/${dir}` : dir;
      try {
        await pyodide.FS.mkdir(currentPath);
      } catch (error) {
        if (error.errno !== 20) throw error; // Ignore EEXIST
      }
    }
  };

  const processFileUpdate = async (pyodide, item) => {
    if (item.path.includes('/')) {
      await ensureParentDirs(pyodide, item.path);
    }
    if (item.format == 'json'){
      item.content = JSON.stringify(item.content)
    }
    console.log('upload:',item.path)
    await pyodide.FS.writeFile(item.path, item.content || '');
    try{
    await runPython('autoreload()')
    console.log('reload ok')
    if (typeof window.ff_initialized_trigger === 'function') {
      window.ff_initialized_trigger();
    }
    }catch{
      console.log('reload error')
    }
    
  };

  const processDeletion = async (pyodide, key) => {
    const path = key.replace('JupyterLite Storage/files/', '');
    try {
      const stats = pyodide.FS.stat(path);
      if (pyodide.FS.isDir(stats.mode)) {
        await deleteRecursive(pyodide, path);
      } else {
        await pyodide.FS.unlink(path);
      }
    } catch (error) {
      if (error.errno !== 44) console.error('Deletion failed:', path, error);
    }
  };

  // ================= QUEUE PROCESSING =================
  const processQueue = async () => {
    if (!pyodideRef.value?.FS || changeQueue.size === 0) return;
    
    isProcessing = true;
    const pyodide = pyodideRef.value;
    const queue = Array.from(changeQueue);
    changeQueue.clear();

    for (const { type, key, value } of queue) {
      console.log('pQ', type,key)
      try {
        if (type === 'delete') {
          await processDeletion(pyodide, key);
        } else {
          const item = JSON.parse(value);
          if (item.type === 'notebook') {
              //pass
          }else if (item.type === 'directory') {
            await ensureParentDirs(pyodide, item.path);
            try{
            await pyodide.FS.mkdir(item.path);
            }catch(e){
              console.log('mkdir error;',item.path,' (already exists?)',e)
            }
          } else {
            await processFileUpdate(pyodide, item);
            
          }
        }
      } catch (error) {
        console.error('Sync error:', { key, error , type, value});
      }
    }
    isProcessing = false;
  };

  // ================= EVENT HANDLING =================
  const handleStorageChange = (event) => {
    console.log('handleStorageChange',event.key)

    if (!event.key?.startsWith('JupyterLite Storage/files/')) return;
    console.log('handleStorageChange')

    changeQueue.add({
      type: event.newValue === null ? 'delete' : 'update',
      key: event.key,
      value: event.newValue
    });

    if (!isProcessing) {
      requestAnimationFrame(() => processQueue());
    }
  };

  // ================= LIFECYCLE =================
  const init = async () => {
    window.addEventListener('storage', handleStorageChange);
    // Initial full sync
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key.startsWith('JupyterLite Storage/files/')) {
        handleStorageChange({
          key,
          newValue: localStorage.getItem(key)
        });
        await processQueue();
      }
    }
  };

  // watch(pyodideRef, (pyodide) => {
  //   if (pyodide) init();
  // }, { immediate: true });

  onUnmounted(() => {
    window.removeEventListener('storage', handleStorageChange);
  });

  // ================= UTILITIES =================
  const deleteRecursive = async (pyodide, path) => {
    const contents = pyodide.FS.readdir(path);
    for (const item of contents.filter(i => !['.', '..'].includes(i))) {
      const fullPath = `${path}/${item}`;
      const stats = pyodide.FS.stat(fullPath);
      if (pyodide.FS.isDir(stats.mode)) {
        await deleteRecursive(pyodide, fullPath);
      } else {
        await pyodide.FS.unlink(fullPath);
      }
    }
    await pyodide.FS.rmdir(path);
  };

  return { triggerSync: processQueue , initSync:init};
}