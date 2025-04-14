<script setup>
import { computed, ref } from "vue";
import { useSlots, getCurrentInstance } from "vue";
import { lang_de, langf, langf_set } from "../../main.js";
const instance = getCurrentInstance();
const app = instance.appContext.app;
import { useStorage } from "@vueuse/core";

const cur_lang = useStorage("cur_lang", "de");

const slots = useSlots();

const msg = computed(() => {
  return langf(
    slots.default()[0].children,
    app.config.globalProperties.cur_lang.value
  );
});
const key = computed(() => {
  return slots.default()[0].children;
});

const cur_key = ref(null)

const show_dialog = ref(false);

function set_lang_val(key) {
  cur_key.value = key;

  show_dialog.value = true;
    
  const t = useStorage('CUSTOM_LANG_DE',true)
  t.value = true
  
}
</script>

<template>
  <!-- <span > {{ L(msg) }}</span> -->
  <span v-if="cur_lang == 'xx'" @click="set_lang_val(key)"> {{ msg }}</span>
  <span v-if="cur_lang != 'xx'"> {{ msg }}</span>
  <!-- <span > {{ L(children) }}</span> -->

  <v-dialog v-model="show_dialog" width="auto">
    <v-card prepend-icon="mdi-update" title="LANG_SETUP" style="min-width:400px">
    
    <v-select  class="custom-label-color" label="key" :items="Object.keys(lang_de)" v-model="cur_key"/>
    
    <v-text-field class="custom-label-color" label='value' v-model="lang_de[cur_key]" />

      <template v-slot:actions>
        <v-btn class="ms-auto" text="Ok"  @click="show_dialog = false"
        ></v-btn>
      </template>
    </v-card>
      
  </v-dialog>
</template>
 