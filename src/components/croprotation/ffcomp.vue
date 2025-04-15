<template>
  <v-card
    style="width: 43vw"
    class="ma-2 pa-2"
    
  >
    <v-card-title class="cursor-pointer"> </v-card-title>

    
    <v-select
      style="height: 80px"
      :label="L('FF_Kultur') + ', ' + L('ANBAU_JAHR') + ': ' + jahr"
      :items="
      JSON.parse(get_avail_crops_for_jahr(FF, jahr)).map((key) => ({
                          value: key,
                          title: L(key),
                        }))
      "
      class="custom-label-color"
      v-model="FF[jahr].crop"
    ></v-select>
  </v-card>
</template>

  <script  setup>
import { ref, reactive, computed, defineEmits } from "vue";
// import { koraktor } from "../koraktor/koraktor";
import usePyodide from "@/composables/usePyodide";
import { globalStore } from '@/utils/globalstore'

const { runPythonS } = usePyodide();

const get_avail_crops_for_jahr = runPythonS("jswrapper.get_avail_crops_for_jahr"); // get Python func

const props = defineProps({
  jahr: {
    type: Number,
    required: true,
  },
});

const emit = defineEmits(["crop_select", "jahr_select"]);

const FF = globalStore.get("FF")

  
</script>