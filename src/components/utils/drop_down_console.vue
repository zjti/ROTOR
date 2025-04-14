<template>
  <div class="quake-console" :class="{ 'console-open': isOpen }">
    <div class="console-header" @click="toggleConsole">
      <span>Pyodide REPL Console</span>
      <span class="toggle-icon">{{ isOpen ? "▼" : "▲" }}</span>
    </div>
    <div class="console-content" v-show="isOpen">
      <div class="console-output" ref="outputEl">
        <div
          v-for="(line, index) in outputLines"
          :key="index"
          v-html="line"
        ></div>
      </div>
      <div class="console-input">
        <span class="prompt" v-html="getPrompt()"></span>
        <textarea
          v-model="input"
          @keydown="handleKeyDown"
          @keyup.up="historyUp"
          @keyup.down="historyDown"
          ref="inputEl"
          placeholder="Enter Python code (Shift+Enter for new line)"
          rows="1"
          @input="adjustTextareaHeight"
        ></textarea>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, watch } from "vue";
import usePyodide from "@/composables/usePyodide";
import { useStorage } from '@vueuse/core'


const { pyodide, runPython } = usePyodide(); // Make sure your composable exposes the pyodide instance

const isOpen = ref(false);
const input = ref("");
const outputLines = ref([]);
const history = useStorage('console_history',[]);
const historyIndex = ref(-1);
const outputEl = ref(null);
const inputEl = ref(null);
const isMultiline = ref(false);


const pyodideOutputWriter = (text) => {
  // Split multiline output and add each line
  text.split("\n").forEach((line) => {
    if (line.trim()) {
      outputLines.value.push(line);
    }
  });
  scrollToBottom();
};

// Initialize Pyodide output redirection
const esc= (text)=>{
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
const initializeOutputRedirection =async () => {

  if (!pyodide.value) {
    outputLines.value.push("Waiting for Pyodide initialization...");
    return;
  }
  await pyodide.value.loaded;


  try {
    pyodide.value.setStdout({
      batched: (text) => pyodideOutputWriter(esc(text))
    });
    pyodide.value.setStderr({
      batched: (text) => pyodideOutputWriter(`<span class="error">${esc(text)}</span>`)
    });
    outputLines.value.push("Pyodide stdout/stderr redirected to console");
  } catch (error) {
    outputLines.value.push(`<span class="error">Failed to redirect output: ${error.message}</span>`);
  }
};

const initializationWatcher = watch(() => pyodide?.value, async (newVal) => {
  if (newVal) {
    const success = await initializeOutputRedirection();
    if (success) {
      initializationWatcher(); // Stop watching after successful setup
    }
  }
}, { immediate: true });

const toggleConsole = () => {
  isOpen.value = !isOpen.value;
};

watch(isOpen, (newVal) => {
  if (newVal) {
    nextTick(() => {
      if (inputEl.value) {
        inputEl.value.focus();
      }
      scrollToBottom();
    });
  }
});

const getPrompt = () => {
  return isMultiline.value ? "... " : "&gt;&gt;&gt; ";
};

const handleKeyDown = (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    execute();
  } else if (e.key === "Enter" && e.shiftKey) {
    // Allow default behavior (new line)
    isMultiline.value = true;
    nextTick(() => adjustTextareaHeight());
  }
};

const adjustTextareaHeight = () => {
  if (inputEl.value) {
    inputEl.value.style.height = "auto";
    inputEl.value.style.height = `${Math.min(
      inputEl.value.scrollHeight,
      200
    )}px`;
  }
};

const execute = async () => {
  if (!input.value.trim()) return;

  const command = input.value;
  history.value.push(command);
  historyIndex.value = history.value.length;

  // Display input with prompts
  outputLines.value.push(`<span class="input-line">${command.split('\n').map((line, i) => `${i === 0 ? '>>>' : '...'} ${esc(line)}`).join('\n')}</span>`);

  try {
    // Execute the command - output will be captured via stdout/stderr
    const result = await runPython(command);
    
    // Also capture the return value if not None
    if (result !== undefined && result !== null) {
      const displayValue = await runPython(`repr(${command})`)
        .catch(() => null);
      if (displayValue && displayValue !== 'None') {
        outputLines.value.push(esc(displayValue));
      }
    }
  } catch (error) {
    outputLines.value.push(`<span class="error">${esc(error.message)}</span>`);
  }

  input.value = "";
  scrollToBottom();
  nextTick(() => inputEl.value?.focus());
};



const historyUp = () => {
  if (history.value.length === 0) return;
  if (historyIndex.value > 0) {
    historyIndex.value--;
    input.value = history.value[historyIndex.value];
  }
  nextTick(() => {
    if (inputEl.value) {
      inputEl.value.focus();
    }
  });
};

const historyDown = () => {
  if (history.value.length === 0) return;
  if (historyIndex.value < history.value.length - 1) {
    historyIndex.value++;
    input.value = history.value[historyIndex.value];
  } else {
    historyIndex.value = history.value.length;
    input.value = "";
  }
  nextTick(() => {
    if (inputEl.value) {
      inputEl.value.focus();
    }
  });
};

const scrollToBottom = () => {
  nextTick(() => {
    if (outputEl.value) {
      outputEl.value.scrollTop = outputEl.value.scrollHeight;
    }
  });
};

onMounted(async() => {
  if (pyodide?.value) {
    await initializeOutputRedirection();
  }

  outputLines.value.push("Pyodide console ready. Enter Python commands below.");
  

  const handleGlobalKeyDown = (event) => {
    if (event.key === "`" || event.key === "~") {
      event.preventDefault(); 
      toggleConsole();
    }
  };

  window.addEventListener("keydown", handleGlobalKeyDown);
});
</script>

<style scoped>
.quake-console {
  position: fixed;
  top: -400px;
  left: 0;
  right: 0;
  height: 400px;
  background-color: #1e1e1e;
  color: #f0f0f0;
  font-family: monospace;
  font-size: 14px;
  border-bottom: 2px solid #444;
  z-index: 1000;
  transition: top 0.3s ease;
}

.quake-console.console-open {
  top: 0;
}

.console-header {
  padding: 8px 15px;
  background-color: #333;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  user-select: none;
}

.console-content {
  height: calc(100% - 36px);
  display: flex;
  flex-direction: column;
}

.console-output {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  white-space: pre-wrap;
}

.console-input {
  display: flex;
  padding: 8px 10px;
  background-color: #252525;
  border-top: 1px solid #444;
  align-items: flex-start;
}

.prompt {
  margin-right: 8px;
  color: #4caf50;
  white-space: nowrap;
  padding-top: 4px;
}

textarea {
  flex: 1;
  background: transparent;
  border: none;
  color: inherit;
  font-family: monospace;
  font-size: inherit;
  outline: none;
  resize: none;
  overflow-y: hidden;
  min-height: 20px;
  max-height: 200px;
  padding: 0;
  line-height: 1.4;
}

.input-line {
  color: #569cd6;
}

.error {
  color: #f44747;
}
</style>