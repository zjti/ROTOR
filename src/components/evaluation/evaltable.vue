<script setup>
import { computed } from 'vue'

// Props
const props = defineProps({
  crops: {
    type: Array,
    required: true,
  }
})

// Fields to average instead of summing
const averageKeys = ['BioDiversityIndex']

// Find all nutrient keys dynamically
const nutrientKeys = computed(() => {
  const keys = new Set()
  props.crops.forEach(crop => {
    if (!crop.crop) return
    const entries = [...(crop.supplies ?? []), ...(crop.removals ?? [])]
    entries.forEach(item => {
      Object.keys(item).forEach(key => {
        if (['N', 'P', 'K', 'BioDiversityIndex'].includes(key)) {
          keys.add(key)
        }
      })
    })
  })
  return Array.from(keys)
})

// Helpers for totals
const getCropTotal = (crop, key) => {
  const entries = [...(crop.supplies ?? []), ...(crop.removals ?? [])]
  const values = entries.map(item => item[key]).filter(v => typeof v === 'number')
  if (!values.length) return 0
  if (averageKeys.includes(key)) {
    return values.reduce((a, b) => a + b, 0) / values.length
  } else {
    return values.reduce((a, b) => a + b, 0)
  }
}

const getGrandTotal = (key) => {
  const allValues = props.crops.flatMap(crop => {
    if (!crop.crop) return []
    return [...(crop.supplies ?? []), ...(crop.removals ?? [])]
      .map(item => item[key])
      .filter(v => typeof v === 'number')
  })
  if (!allValues.length) return 0
  if (averageKeys.includes(key)) {
    return allValues.reduce((a, b) => a + b, 0) / allValues.length
  } else {
    return allValues.reduce((a, b) => a + b, 0)
  }
}
</script>

<template>
  <table class="crop-table">
    <thead>
      <tr>
        <th>Crop</th>
        <th>Type</th>
        <th>Name</th>
        <th>Info</th>
        <th v-for="key in nutrientKeys" :key="'header-' + key">
          {{ averageKeys.includes(key) ? key + ' (avg)' : 'kg ' + key + '/ha' }}
        </th>
      </tr>
    </thead>

    <tbody>
      <template v-for="(crop, cropIndex) in crops">
        <template v-if="crop.crop">
          <tr v-for="(item, idx) in [...(crop.supplies ?? []), ...(crop.removals ?? [])]" :key="'row-' + cropIndex + '-' + idx">
            <template v-if="idx === 0">
              <td
                :rowspan="(crop.supplies?.length || 0) + (crop.removals?.length || 0)"
                class="crop-name"
              >
               <l>{{ crop.crop }}</l> 
              </td>
            </template>
            <td>{{ (crop.supplies ?? []).includes(item) ? 'Supply' : 'Removal' }}</td>
            <td>{{ item.supply_name || item.removal_name }}</td>
            <td>{{ item.supply_info || item.removal_info }}</td>
            <td v-for="key in nutrientKeys" :key="'cell-' + cropIndex + '-' + idx + '-' + key" class="num">
              {{ item[key] != null ? item[key].toFixed(1) : '' }}
            </td>
          </tr>

          <!-- Crop total row -->
          <tr class="crop-total" :key="'crop-total-' + cropIndex">
            <td colspan="4" class="right italic"></td>
            <td v-for="key in nutrientKeys" :key="'crop-total-' + cropIndex + '-' + key" class="num bold">
              {{ getCropTotal(crop, key).toFixed(1) }}
            </td>
          </tr>
        </template>
      </template>

      <!-- Grand total row -->
      <tr class="grand-total" :key="'grand-total'">
        <td colspan="4" class="right bold">Bilanz</td>
        <td v-for="key in nutrientKeys" :key="'grand-' + key" class="num bold">
          {{ getGrandTotal(key).toFixed(1) }}
        </td>
      </tr>
    </tbody>
  </table>
</template>

<style scoped>
.crop-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  font-family: sans-serif;
  font-size: 14px;
}

.crop-table th,
.crop-table td {
  border: 1px solid #ccc;
  padding: 6px 10px;
}

.crop-table th {
  background: #f4f4f4;
}

.crop-name {
  background: #eef;
  font-weight: bold;
  text-align: center;
}

.crop-total {
  background: #ddf;
}

.grand-total {
  background: #cce;
  font-weight: bold;
  font-size: 1rem;
}

.num {
  text-align: right;
}

.right {
  text-align: right;
}

.bold {
  font-weight: bold;
}

.italic {
  font-style: italic;
}
</style>
