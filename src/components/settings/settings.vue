<template>
  <v-container>
    <v-expansion-panels multiple>
      <v-expansion-panel :title="L('MAP_SETTINGS')" class="custom-expansion-panel">
        <v-expansion-panel-text>
          <formview :block="userlocation" />
          <RotorMap></RotorMap>
        </v-expansion-panel-text>
      </v-expansion-panel>
      <v-expansion-panel :title="L('SOIL_SETTINGS')" class="custom-expansion-panel">
        <v-expansion-panel-text>
          <!-- <formview :block="soil_params" /> -->
          <formview :block="ps" />
        </v-expansion-panel-text>
      </v-expansion-panel>
      <v-expansion-panel :title="L('PHYTO_SETTINGS')" class="custom-expansion-panel">
        <v-expansion-panel-text>
          <phyto-grid :cellSize="30" />
        </v-expansion-panel-text>
      </v-expansion-panel>
      <v-expansion-panel :title="L('DUNG_PROPS')" class="custom-expansion-panel">
        <v-expansion-panel-text>
          <dung_edit />
        </v-expansion-panel-text>
      </v-expansion-panel>
      <v-expansion-panel :title="L('VERKRAUTUNG')" class="custom-expansion-panel">
        <v-expansion-panel-text>
          <verkraut />
        </v-expansion-panel-text>
      </v-expansion-panel>

      <v-expansion-panel :title="L('WETTER')" class="custom-expansion-panel">
        <v-expansion-panel-text>
          <weather />
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-container>
</template>

<script setup>
import { globalStore } from '@/utils/globalstore'
import { useStorage, watchTriggerable } from '@vueuse/core'

const ps = globalStore.get('SOIL')
const userlocation = useStorage("USERINFO",{
    "FARMNAME": {
        "default": '',
        "type": "string", 
        "help":"Bitte Betriebsnamen für die Auswertung angeben"
    },"USERNAME": {
        "default": '',
        "type": "string", 
        "help":"Bitte Namen des Bearbeiters für die Auswertung angeben"
    },"FARMSIZE": {
        "default":"FARM_SMALL",
        "type": "select",
        "items":["FARM_SMALL","FARM_MEDIUM","FARM_BIG"]
    },
})
</script>