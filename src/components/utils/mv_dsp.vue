<script setup>
import { computed } from 'vue';

const props = defineProps({
  akey: {
    type: String,
    default: '',
  },
  obj: {
    type: Object,
    required: true
  }
});

const v = computed(() => {
  if (!props.akey || !props.obj?.MODELVALUES) return '';
  
  try {
    // Split the key by dots and safely navigate the object
    const keys = props.akey.split('.');
    let subobj = props.obj.MODELVALUES;
    
    // Traverse each level of the nested structure
    for (const key of keys) {
      if (!subobj || typeof subobj !== 'object') {
        return '';
      }
      subobj = subobj[key];
    }
    
    // Handle the final value extraction
    if (!subobj || typeof subobj !== 'object') {
      return '';
    }
    
    const keyToUse = 'name_corrected' in subobj 
      ? subobj.name_corrected 
      : subobj.name;
    
    return subobj[keyToUse];
  } catch {
    return '';
  }
});
</script>

<template>
  <div>{{ v }}</div>
</template>