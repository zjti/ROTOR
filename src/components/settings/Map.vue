<script setup>
import { onMounted, ref, nextTick } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { langf } from "@/main.js";



// import  "georaster-layer-for-leaflet";
// import GeoRaster from "georaster";

// import icon from "leaflet/dist/images/marker-icon.png";
// import iconShadow from "leaflet/dist/images/marker-icon.png";

const MIcon = L.icon({
  iconUrl: "map/marker-icon.png",
  iconSize: [38, 64], // size of the icon

  iconAnchor: [22, 64], // point of the icon which will correspond to marker's location
  // iconSize: [41, 41],
  // iconAnchor: [41, 41],
});

// import { createColorLegend, read_wfs, read_geo_raster } from "@/utils/maphelpers.js";

const props = defineProps({
  // isbusy: {
  //   type: Object,
  //   required: true,
  // },
  wmsLayers: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["marker-placed", "load", "loading"]);

const mapContainer = ref(null);
let map;
let currentLayer = null; // Track the currently visible layer
let currentLegend = null;
let marker;
const opacity = ref(0.5);
const my_layers = {};
const my_legends = {};

onMounted(async () => {
  await nextTick(); // Ensures DOM is fully updated

  if (!mapContainer.value) return;

  // Initialize Leaflet map
  map = L.map(mapContainer.value).setView([51.1657, 10.4515], 6);

  map.on('click', function (e) {
      // Get the coordinates of the click
      const { lat, lng } = e.latlng;

      setMarker(e.latlng)
    });

  // Add OpenStreetMap tile layer
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);

  // Load layers
  loadLayers();

  // Add custom controls for layer switching, marker, and opacity
  addCustomControls();

  // Handle map resizing when the container changes size
  setTimeout(() => {
    map.invalidateSize();
  }, 400);
});

const loadLayers = () => {
  for (const [key, layerInfo] of Object.entries(props.wmsLayers)) {
    if (layerInfo.type == "wms") {
      const wmsLayer = L.tileLayer.wms(layerInfo.url, {
        layers: layerInfo.layer,
        version: layerInfo.version,
        transparent: true,
        format: "image/png",
      });

      wmsLayer.on("loading", () => {
        emit("loading");
      });

      wmsLayer.on("load", () => {
        emit("load");
      });

      my_layers[key] = wmsLayer;
      // Set the first layer as the current layer (if no layer is currently visible)
      
      if (layerInfo.hasOwnProperty('legend')) {
        const legend = L.control({ position: "bottomright" });
        
        legend.onAdd = function (map) {
          const div = L.DomUtil.create("div", "info legend");
          div.innerHTML = layerInfo.legend
          return div
        };
        my_legends[key] = legend

        
      }
      if (!currentLayer) {
        currentLayer = wmsLayer;
        
        switchLayer(key);
      }
    }  
  }
};


const addCustomControls = () => {
  // Control for layer switching (HTML <select> dropdown)
  const layerControl = L.control({ position: "topright" });
  layerControl.onAdd = () => {
    const container = L.DomUtil.create("div"); //leaflet-bar leaflet-control

    
    container.addEventListener("click", (e) => {
      e.stopPropagation();
    });
    container.style.backgroundColor = "#fff";
    const txt = L.DomUtil.create("span", "", container);
    txt.innerHTML = langf("LAYER")+":";

    const select = L.DomUtil.create("select", "", container);
    select.style.width = "150px"; // Adjust width as needed

    // Add options to the dropdown
    for (const [key, layerInfo] of Object.entries(props.wmsLayers)) {
      const option = L.DomUtil.create("option", "", select);
      option.value = key;
      option.text = layerInfo.name;
    }

    // Handle layer switching when the dropdown value changes
    select.onchange = (e) => {
      const selectedKey = e.target.value;
      switchLayer(selectedKey);
    };

    const button = L.DomUtil.create("button", "", container);
    button.innerHTML = "📍";
    button.style.fontSize = "20px";
    button.style.cursor = "pointer";
    button.onclick = () => {
      const center = map.getCenter();
      setMarker(center);
    };
    L.DomUtil.create("br", "", container);
    const input = L.DomUtil.create("input", "", container);
    input.type = "range";
    input.min = "0";
    input.max = "1";
    input.step = "0.1";
    input.value = opacity.value;
    input.style.width = "100%";
    input.oninput = (e) => {
      opacity.value = parseFloat(e.target.value);
      setOpacity(opacity.value);
      

    };

    // Inline CSS for the slider container
    input.style.width = "100%"; // Full width
    input.style.height = "15px"; // Height of the track
    input.style.background = "#ddd"; // Background color of the track
    input.style.outline = "none"; // Remove outline
    input.style.opacity = "0.7"; // Slightly transparent
    input.style.transition = "opacity 0.2s"; // Smooth transition
    input.style.borderRadius = "10px"; // Rounded corners for the track

    // Hover effect
    input.addEventListener("mouseover", () => {
      input.style.opacity = "1"; // Fully opaque on hover
    });
    input.addEventListener("mouseout", () => {
      input.style.opacity = "0.7"; // Reset opacity when not hovering
    });

    // Inline CSS for the slider thumb (using pseudo-elements is not possible inline, so we use a workaround)
    input.style.setProperty("-webkit-appearance", "none"); // Remove default styling
    input.style.setProperty("appearance", "none"); // Remove default styling

    // Workaround for thumb styling (limited in inline CSS)
    input.style.setProperty("--thumb-size", "25px"); // Custom property for thumb size
    input.style.setProperty("--thumb-color", "#4CAF50"); // Custom property for thumb color

    // Use a small script to dynamically inject styles for the thumb
    const style = document.createElement("style");
    style.textContent = `
  input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: var(--thumb-size);
    height: var(--thumb-size);
    background: var(--thumb-color);
    cursor: pointer;
    border-radius: 50%;
  }
  input[type="range"]::-moz-range-thumb {
    width: var(--thumb-size);
    height: var(--thumb-size);
    background: var(--thumb-color);
    cursor: pointer;
    border-radius: 50%;
  }
`;
    document.head.appendChild(style);

    // Stop event propagation for mouse events on the slider
    input.addEventListener("mousedown", (e) => {
      e.stopPropagation();
    });

    input.addEventListener("click", (e) => {
      e.stopPropagation();
    });


    input.addEventListener("mouseup", (e) => {
      e.stopPropagation();
    });

    input.addEventListener("mousemove", (e) => {
      e.stopPropagation();
    });

    return container;
  };
  layerControl.addTo(map);
};

const setMarker = (latlng) => {
  if (marker) {
    map.removeLayer(marker);
  }
  marker = L.marker(latlng, { icon: MIcon }).addTo(map);
  console.log(marker);
  const { lat, lng } = latlng;
  map.setView([lat, lng], 11);
  emit("marker-placed", { lat: lat, lng: lng });
};

const setOpacity = (value) => {
  if (currentLayer) {
    currentLayer.setOpacity(value);
  }
};

// Function to switch layers
const switchLayer = (layerKey) => {
  const layerInfo = props.wmsLayers[layerKey];
  if (layerInfo) {
    if (currentLegend) {
      map.removeControl(currentLegend);
    }
    // Remove the current layer from the map
    if (currentLayer) {
      map.removeLayer(currentLayer);
    }

    // Add the new layer to the map
    currentLayer = my_layers[layerKey];
    currentLayer.addTo(map);
    if (layerKey in my_legends) {
      currentLegend = my_legends[layerKey];
      console.log(currentLegend)
      currentLegend.addTo(map);
    } else {
      currentLegend = null;
    }
    currentLayer.setOpacity(opacity.value); // Apply current opacity to the new layer
  }
};

defineExpose({
  setOpacity,
});
</script>
 
<template>
  <div ref="mapContainer" style="width: 100%; height: 600px"></div>
</template>

<style scoped>
.custom-slider {
  -webkit-appearance: none; /* Remove default styling */
  appearance: none;
  width: 100%; /* Full width */
  height: 15px; /* Increase height of the track */
  background: #ddd; /* Background color of the track */
  outline: none; /* Remove outline */
  opacity: 0.7; /* Slightly transparent */
  transition: opacity 0.2s; /* Smooth transition */
}

.custom-slider:hover {
  opacity: 1; /* Fully opaque on hover */
}

/* Styling the slider thumb */
.custom-slider::-webkit-slider-thumb {
  -webkit-appearance: none; /* Remove default styling */
  appearance: none;
  width: 25px; /* Increase width of the thumb */
  height: 25px; /* Increase height of the thumb */
  background: #4caf50; /* Green color */
  cursor: pointer; /* Pointer cursor */
  border-radius: 50%; /* Circular thumb */
}

.custom-slider::-moz-range-thumb {
  width: 25px; /* Increase width of the thumb */
  height: 25px; /* Increase height of the thumb */
  background: #4caf50; /* Green color */
  cursor: pointer; /* Pointer cursor */
  border-radius: 50%; /* Circular thumb */
}

/* Styling the slider track */
.custom-slider::-webkit-slider-runnable-track {
  width: 100%;
  height: 15px; /* Height of the track */
  background: #ddd; /* Background color of the track */
  border-radius: 10px; /* Rounded corners */
}

.custom-slider::-moz-range-track {
  width: 100%;
  height: 15px; /* Height of the track */
  background: #ddd; /* Background color of the track */
  border-radius: 10px; /* Rounded corners */
}
</style>