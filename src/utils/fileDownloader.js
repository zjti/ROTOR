// utils/fileDownloader.js
export async function downloadFiles(fileListUrl) {
    try {
      const response = await fetch(fileListUrl);
      const files = await response.json();
      
      // First pass: Create all directories
      const dirs = new Set();
      files.forEach(file => {
        const segments = file.path.split('/');
        segments.slice(0, -1).reduce((acc, dir) => {
          const path = acc ? `${acc}/${dir}` : dir;
          dirs.add(path);
          return path;
        }, '');
      });
      console.log(dirs)
  
      // Create directory entries first
      for (const dirPath of dirs) {
        const dirKey = `JupyterLite Storage/files/${dirPath}`;
        if (!localStorage.getItem(dirKey)) {
          console.log('mkdir ',dirKey)
          const dirName = dirPath.split('/').pop();
          localStorage.setItem(dirKey, JSON.stringify({
            name: dirName,
            path: dirPath,
            type: "directory",
            format: "json",
            mimetype: "application/json",
            content: [], // Will be populated with children
            size: 0,
            writable: true,
            created: new Date().toISOString(),
            last_modified: new Date().toISOString()
          }));
        }
      }
  
      // Second pass: Create files and update directory contents
      for (const file of files) {
        const storageKey = `JupyterLite Storage/files/${file.path}`;
        
        // NOT OVERWRITE EXISTING 
        // if (localStorage.getItem(storageKey)) continue;
  
        // Download file content
        const fileResponse = await fetch(file.url);
        const content = await fileResponse.text();
  
        // Create file entry
        const fileEntry = {
          name: file.path.split('/').pop(),
          path: file.path,
          type: "file",
          format: "text",
          mimetype: "text/plain",
          content,
          size: content.length,
          writable: true,
          created: new Date().toISOString(),
          last_modified: new Date().toISOString()
        };
        localStorage.setItem(storageKey, JSON.stringify(fileEntry));
        const event = new Event("storage")
        event.key = storageKey
        event.newValue = JSON.stringify(fileEntry)
        window.dispatchEvent( event )

  
        // Update parent directory content array
        const parentDirPath = file.path.split('/').slice(0, -1).join('/');
        // console.log('update parent',parentDirPath)
        if (parentDirPath) {
          const parentKey = `JupyterLite Storage/files/${parentDirPath}`;
          const parentDir = JSON.parse(localStorage.getItem(parentKey));
          parentDir.content = parentDir.content || [];
          parentDir.content.push({
            name: fileEntry.name,
            path: fileEntry.path,
            type: fileEntry.type,
            format: fileEntry.format,
            mimetype: fileEntry.mimetype,
            last_modified: fileEntry.last_modified,
            created: fileEntry.created,
            size: fileEntry.size,
            writable: fileEntry.writable
          });
          parentDir.last_modified = new Date().toISOString();
          localStorage.setItem(parentKey, JSON.stringify(parentDir));
          

        }
      }
    } catch (error) {
      console.error('Download failed:', error);
      throw error;
    }
  }

  