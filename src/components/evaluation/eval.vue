<template>
  <div>

    <evaltable :crops="eval_data" />

  </div>
  
</template>

<script setup>
import { globalStore } from "@/utils/globalstore";

const eval_data = globalStore.get("EVAL_DATA");
</script>
  
<style scoped>
</style>
  