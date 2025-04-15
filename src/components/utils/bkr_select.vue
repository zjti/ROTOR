<template>
  <v-select
    v-model="model"
    :items="selectItems"
    item-title="label"
    item-value="key"
    :label="label"
  ></v-select>
</template>
  
  <script setup>

defineProps({
  
  label: {
    required: false,
  },
  suffix: {
    required: false,
  },
});

import { ref, computed } from "vue";

const model = defineModel();

// Dictionary containing keys and descriptions
const optionsDict = {
  101: "mittlere diluviale Böden MV und Uckermark",
  102: "sandige diluviale Böden des nordostdeutschen Binnentieflandes",
  104: "trocken-warme diluviale Böden des ostdeutschen Tieflandes",
  105: "vorpommersche Sandböden im Uecker-Randow-Gebiet",
  106: "Oderbruch",
  107: "Lößböden in der Ackerebene (Ost)",
  108: "Lößböden in den Übergangslagen (Ost)",
  109: "diluviale Böden der Altmark und Überlappung nördliches Niedersachsen",
  111: "Verwitterungsböden in den Übergangslagen (Ost)",
  112: "Verwitterungsböden in den Höhenlagen (östliches Bayern)",
  113: "Nordwestbayern-Franken",
  114: "Albflächen und Ostbayerisches Hügelland",
  115: "Tertiär-Hügelland Donau-Süd",
  120: "Hochrhein-Bodensee",
  121: "Rheinebene und Nebentäler",
  122: "Schwäbische Alb, Baar",
  123: "Oberes Gäu und körnermaisfähige Übergangslagen",
  127: "Mittellagen Rheinland-Pfalz und Saarland",
  128: "Hunsrück, Westerwald",
  129: "Hocheifel / Höhenlagen",
  130: "Odenwald, Spessart",
  132: "Osthessische Mittelgebirgslagen",
  133: "Zentralhessische Ackerbaugebiete, Warburger Börde",
  134: "Sauerland, Briloner Höhen",
  141: "Jülicher Börde, Zülpicher Börde / Niederungslagen, feucht",
  142: "oberer Mittelrhein, Niederrhein, südliches Münsterland",
  145: "Südhannover / Lehmböden",
  146: "Lüneburger Heide / Sandige Böden",
  147: "mittleres Niedersachsen / leichte Lehmböden",
  148: "südwestliches Weser-Ems-Gebiet / sandige Böden",
  151: "Elbe-Weser-Dreieck / sandige Böden",
  152: "Niedersächsische Küsten- und Elbmarsch",
  153: "Geest - Süd",
  154: "südliches schleswig-holsteinisches Hügelland",
  155: "Marsch - Nord",
  156: "Geest - Nord",
  157: "nördliches schleswig-holsteinisches Hügelland",
  158: "NW-Mecklenburg und Küstengebiet / bessere diluviale Böden",
  191: "Teutoburger Wald",
  192: "Harz",
  193: "Rhön",
  194: "Thüringer Wald",
  195: "Erzgebirge",
  196: "Bayrischer Wald",
  198: "Schwarzwald",
  199: "Alpen",
  143: "Ost-Westfalen, Lippe, Haarstrang, Bergisches Land / Übergangslagen mäßig feucht",
  150: "nordwestliches Weser-Ems-Gebiet / sandige Böden",
  117: "Moränen-Hügelland und Voralpenland",
  116: "Gäu, Donau- und Inntal",
};

// Reactive ref for the selected key
const selectedKey = ref(null);

// Compute the items for the v-select
const selectItems = computed(() => {
  return Object.entries(optionsDict).map(([key, description]) => ({
    key: Number(key), // Ensure the key is a number
    label: `${key} - ${description}`, // Combine key and description for the label
  }));
});
</script>