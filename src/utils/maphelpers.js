import { parse } from "vue/compiler-sfc";


export function createColorLegend(colorScale, minValue, maxValue, steps, title = "") {

    // Calculate step size
    const stepSize = (maxValue - minValue) / (steps - 1);

    // Start building the HTML
    let html = "";


    // Add the table
    html += `<table style="border-collapse: collapse; width: 100px; margin: 20px;">`;

    for (let i = 0; i < steps; i++) {
        const value = minValue + i * stepSize;
        const color = colorScale(value).hex();

        // Add a row for each step
        html += `
        <tr>
          <td style="background-color: ${color}; height: 20px; width:20px; border: 1px solid #000;"></td>
          <td style="height: 20px; text-align: center; border: 1px solid #000;">${value.toFixed(
            1
        )}</td>
        </tr>
      `;
    }
    if (title) {
        html += `<tr>
        <td colspan=2 style="height: 20px; text-align: center; border: 1px solid #000;">${title}</td></tr>`;
    }


    // Close the table
    html += `</table>`;

    return html;
}

export function read_geo_raster(geoRaster, click_event, out_ref) {
    const { lat, lng } = click_event.latlng;
    
    const { pixelHeight, pixelWidth, xmin, ymax } = geoRaster; // GeoTIFF metadata

    // Convert lat/lng to pixel coordinates
    const xPixel = Math.floor((lng - xmin) / pixelWidth);
    const yPixel = Math.floor((ymax - lat) / pixelHeight);

    // Ensure coordinates are within bounds
    if (xPixel >= 0 && xPixel < geoRaster.width && yPixel >= 0 && yPixel < geoRaster.height) {
        const values = geoRaster.values.map((band) => band[yPixel][xPixel]); // Extract values from all bands

        out_ref.value = Math.round(100* values[0])/ 100
        //   alert(`GeoTIFF Values at (${lat.toFixed(5)}, ${lng.toFixed(5)}):\nRed: ${values[0]}\nGreen: ${values[1]}\nBlue: ${values[2]}`);
    } else {
        //   alert("Clicked outside raster bounds.");
    }
}

export function getFeatureInfoUrl(wmsUrl, layerName, lat, lon, width = 256, height = 256, version = "1.3.0", buffer = 0.01) {
    // Create a small bounding box around the lat/lon (simulating a viewport)
    const minx = lon - buffer;
    const maxx = lon + buffer;
    const miny = lat - buffer;
    const maxy = lat + buffer;
    
    // WMS 1.3.0 uses CRS=EPSG:4326 (lat, lon), while WMS 1.1.1 uses SRS=EPSG:4326 (lon, lat)
    const isVersion130 = version === "1.3.0";

    // Center pixel coordinates
    const i = Math.round(width / 2);
    const j = Math.round(height / 2);

//     https://geoservices.julius-kuehn.de/geoserver/bkr/wms?
// SERVICE=WMS
// &VERSION=1.3.0
// &REQUEST=GetFeatureInfo
// &LAYERS=Bodenklimaraum
// &QUERY_LAYERS=Bodenklimaraum
// &STYLES=
// &BBOX=45,5,55,15
// &CRS=EPSG:4326
// &WIDTH=800
// &HEIGHT=600
// &I=400
// &J=300
// &INFO_FORMAT=text/html

    // Construct the GetFeatureInfo URL
    var url;
    if (isVersion130){
        url = `${wmsUrl}?SERVICE=WMS&VERSION=${version}&REQUEST=GetFeatureInfo` +
                    `&LAYERS=${layerName}&QUERY_LAYERS=${layerName}` +
                    `&INFO_FORMAT=text/html` +
                    `&CRS=EPSG:4326` +
                    `&BBOX=${miny},${minx},${maxy},${maxx}` +
                    `&WIDTH=${width}&HEIGHT=${height}&I=${i}&J=${j}`;
    }else{
        url = `${wmsUrl}?SERVICE=WMS&VERSION=${version}&REQUEST=GetFeatureInfo` +
                    `&LAYERS=${layerName}&QUERY_LAYERS=${layerName}` +
                    `&INFO_FORMAT=application/json` +
                    `&SRS=EPSG:4326` +
                    `&BBOX=${minx},${miny},${maxx},${maxy}` +
                    `&WIDTH=${width}&HEIGHT=${height}&I=${i}&J=${j}`;
    }
    return url;
};


export function read_wfs(map, url, marker) {

    

    var wmsUrl = 'https://datahub.uba.de/server/services/Lu/Hintergrund%C2%ADbelastungs%C2%ADdaten_Stickstoff/MapServer/WMSServer';
 

    console.log(Math.round(click_event.containerPoint.x));

    var params = {
        request: 'GetFeatureInfo',
        service: 'WMS',
        srs: 'EPSG:4326',
        styles: '',
        transparent: true,
        version: '1.1.1',
        format: 'image/png',
        bbox: `${bbox.getWest()},${bbox.getSouth()},${bbox.getEast()},${bbox.getNorth()}`,
        height: height,
        width: width,
        layers: '0',
        query_layers: '0',
        info_format: 'text/html', // Try 'text/plain' if this does not work
        x: Math.round(click_event.containerPoint.x),
        y: Math.round(click_event.containerPoint.y)
    };

    fetch(wmsUrl + '?' + new URLSearchParams(params))
        .then(response => response.text())  // Read response as text
        .then(data => parse_wfs(data, out_ref)) // Print raw text
        .catch(error => console.error('Error fetching feature info:', error));
}

function parse_wfs(data, out_ref) {
    // console.log(data);

    const parser = new DOMParser();
    const doc = parser.parseFromString(data, 'text/html');
    const rows = doc.querySelectorAll('table tr');

    // console.log(rows[1].querySelector('td:nth-child(2)').textContent);
    out_ref.value = parseInt(rows[1].querySelector('td:nth-child(2)').textContent, 10)
}
 

// Function to fetch URL content with a time limit
export async function fetchWithTimeout(url, busy_ref, timeout = 10000,) {
    const controller = new AbortController();
    const signal = controller.signal;

    // Set the request state to 1 (in progress)
    busy_ref.value  += 1;

    // Set a timeout to abort the request if it takes too long
    const timeoutId = setTimeout(() => {
        controller.abort();
        console.log("Request timed out");
        busy_ref.value  -= 1; // Set the request state to 0 (completed)
        return;
    }, timeout);

    try {
        const response = await fetch(url, { signal });

        // Clear the timeout if the request completes in time
        clearTimeout(timeoutId);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.text(); // or response.text() if not JSON
        console.log("Request successful:", data);

        // Set the request state to 0 (completed)
        busy_ref.value -= 1; 

        return data;
    } catch (error) {
        console.error("Request failed:", error);

        // Set the request state to 0 (completed)
        busy_ref.value  -= 1; 

        return null;
    }
}
 