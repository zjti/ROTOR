 
<template>
  <v-card class="mx-auto">
    <!-- Card title -->
    <!-- <v-card-title class="text-h6"> <l>MAP_SELECT</l> </v-card-title> -->

    <!-- Map container -->
    <v-card-text style="padding: 0">
      <Map
        :wmsLayers="wmsLayers"
        @marker-placed="handleMarkerPlaced"
        @load="handle_load"
        @loading="handle_loading"
        ref="my_map"
      ></Map>
      <BusyIndicator :isBusy="isBusy > 0" />
    </v-card-text>
  </v-card>
</template>

<script setup>
import { getFeatureInfoUrl, fetchWithTimeout } from "@/utils/maphelpers.js";
import { ref } from "vue";
import { langf } from "@/main.js";
import { globalStore } from '@/utils/globalstore'



const wmsLayers = {
  N_DEPO: {
    name: langf("N_DEPO"),
    type: "wms",
    url: "https://datahub.uba.de/server/services/Lu/Hintergrund%C2%ADbelastungs%C2%ADdaten_Stickstoff/MapServer/WMSServer",
    layer: 0,
    version: "1.1.1",
    legend:
      '<div style="background-color:#fff;"><span>(Einheit: kg N ha⁻¹ a⁻¹)</span><br> <img src="./map/n_depo.png">',
  },
  FELD_KAPA: {
    name: langf("FELD_KAPA"),
    type: "wms",
    url: "https://services.bgr.de/wms/boden/fk10dm1000/?",
    layer: 0,
    version: "1.1.1",
    maxZoom: 110,
    legend: '<div style="background-color:#fff;">   <img src="./map/fkw.png">',
  },
  NUTZ_FELD_KAPA: {
    name: langf("NUTZ_FELD_KAPA"),
    type: "wms",
    url: "https://services.bgr.de/wms/boden/nfkwe1000/?",
    layer: 0,
    version: "1.1.1",
    legend:
    '<div style="background-color:#fff;">   <img src="./map/nfkw.png">',
  },
  BKR: {
    name: langf("BKR"),
    type: "wms",
    url: "https://geoservices.julius-kuehn.de/geoserver/bkr/wms?",
    layer: "Bodenklimaraum",
    version: "1.3.0",
  },
  HUMUSOB: {
    name: langf("HUMUSOB"),
    type: "wms",
    url: "https://services.bgr.de/wms/inspire_so/buek1000humusob/?",
    layer: 0, 
    legend:
    '<div style="background-color:#fff;"><span>(Einheit: % COrg )</span><br>    <img src="./map/humusob.png">',
  },

};

const markerPosition = ref(null);
const my_map = ref(null);
const isBusy = ref(0);

const handle_load = () => {
  isBusy.value--;
  console.log("load", isBusy.value);
};
const handle_loading = () => {
  isBusy.value++, console.log("loading", isBusy.value);
};

const handleMarkerPlaced = (position) => {
  markerPosition.value = position;

  console.log(position);
  const lat = position.lat;
  const lon = position.lng;

  console.log(
    getFeatureInfoUrl(
      "https://services.bgr.de/wms/boden/nfkwe1000/",
      "0",
      lat,
      lon,
      64,
      64,
      "1.1.1"
    )
  );

  fetchWithTimeout(
    getFeatureInfoUrl(
      "https://services.bgr.de/wms/boden/nfkwe1000/",
      0,
      lat,
      lon,
      64,
      64,
      "1.1.1"
    ),
    isBusy,
    4000
  ).then((data) => {
    if (data) {
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(data, "application/xml");

      // Extract the PixelValue attribute
      const fieldsElement = xmlDoc.getElementsByTagName("FIELDS")[0];
      const pixelValue = fieldsElement.getAttribute("Classify.PixelValue");

      if (pixelValue != "NoData" && pixelValue != "noData") {
        globalStore.get("SOIL").value["NFK"].default =  parseFloat(parseFloat(pixelValue).toFixed(2));
      }
    } else {
      // Handle the failure case
    }
  });

  console.log(
    getFeatureInfoUrl(
      "https://services.bgr.de/wms/boden/fk10dm1000/",
      "0",
      lat,
      lon,
      64,
      64,
      "1.1.1"
    )
  );

  fetchWithTimeout(
    getFeatureInfoUrl(
      "https://services.bgr.de/wms/boden/fk10dm1000/",
      0,
      lat,
      lon,
      64,
      64,
      "1.1.1"
    ),
    isBusy,
    4000
  ).then((data) => {
    if (data) {
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(data, "application/xml");

      // Extract the PixelValue attribute
      const fieldsElement = xmlDoc.getElementsByTagName("FIELDS")[0];
      const pixelValue = fieldsElement.getAttribute("Classify.PixelValue");

      if (pixelValue != "NoData" && pixelValue != "noData") {
        globalStore.get("SOIL").value["FELD_KAPA"].default =   parseFloat(parseFloat(pixelValue).toFixed(2));
      }
    } else {
      // Handle the failure case
    }
  });


  console.log(
    getFeatureInfoUrl(
      "https://datahub.uba.de/server/services/Lu/Hintergrund%C2%ADbelastungs%C2%ADdaten_Stickstoff/MapServer/WMSServer",
      "0",
      lat,
      lon,
      64,
      64,
      "1.1.1"
    )
  );

  fetchWithTimeout(
    getFeatureInfoUrl(
      "https://datahub.uba.de/server/services/Lu/Hintergrund%C2%ADbelastungs%C2%ADdaten_Stickstoff/MapServer/WMSServer",
      0,
      lat,
      lon,
      64,
      64,
      "1.1.1"
    ),
    isBusy,
    4000
  ).then((data) => {
    if (data) {
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(data, "application/xml");
      console.log(xmlDoc);
      // Extract the PixelValue attribute
      const fieldsElement = xmlDoc.getElementsByTagName("FIELDS")[0];
      const Value = fieldsElement.getAttribute("Classify.Pixelwert");

      if (Value != "noData") {
        globalStore.get("SOIL").value["N_DEPO"].default = parseFloat((parseFloat(Value) /71.428).toFixed(2));
      }
    } else {
      // Handle the failure case
    }
  });

  const featureInfoUrl = getFeatureInfoUrl(
    "https://services.bgr.de/wms/inspire_so/buek1000humusob/",
    0,
    lat,
    lon,
    64,
    64,
    "1.1.1"
  );
  console.log(featureInfoUrl);
  fetchWithTimeout(featureInfoUrl, isBusy, 4000).then((data) => {
    if (data) {
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(data, "application/xml");
      console.log(xmlDoc)
      // Extract the PixelValue attribute
      const fieldsElement = xmlDoc.getElementsByTagName("FIELDS")[0];
      const pixelValue = fieldsElement.getAttribute("Classify.PixelValue");

      if (pixelValue != "noData") {
        // koraktor.set("NFK", pixelValue);
        console.log('OBS',pixelValue)
      }
    } else {
      // Handle the failure case
    }
  });

  console.log(
    getFeatureInfoUrl(
      "https://geoservices.julius-kuehn.de/geoserver/bkr/wms",
      "Bodenklimaraum",
      lat,
      lon,
      64,
      64,
      "1.3.0"
    )
  );

  fetchWithTimeout(
    getFeatureInfoUrl(
      "https://geoservices.julius-kuehn.de/geoserver/bkr/wms",
      "Bodenklimaraum",
      lat,
      lon,
      64,
      64,
      "1.3.0"
    ),
    isBusy,
    4000
  ).then((data) => {
    if (data) {
      const parser = new DOMParser();
      const doc = parser.parseFromString(data, "text/html");

      // Select the first <td> inside the table (BKR-NR)
      const bkrNrElement = doc.querySelector(
        ".soja_table tr:nth-of-type(2) td"
      );

      // Extract and return the BKR-NR value
      const bkr =  bkrNrElement ? bkrNrElement.textContent.trim() : null
      globalStore.get("SOIL").value["BKR"].default =  parseInt(bkr) ;

    } else {
      // Handle the failure case
    }
  });
  url: "https://geoservices.julius-kuehn.de/geoserver/bkr/wms?",
    console.log("Marker placed at:", position);
};
</script>