<template>
    <div style="height: 400px">
      <Bar :data="chartData" :options="chartOptions" :height="null" :width="null" />
    </div>
  </template>
  
  <script setup>
  import {
    Chart as ChartJS,
    BarElement,
    CategoryScale,
    LinearScale,
    Tooltip,
    Legend
  } from 'chart.js'
  import { Bar } from 'vue-chartjs'
  import { computed } from 'vue'
  
  ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend)
  
  const props = defineProps({
    labels: Array, // ['Jan', 'Feb', ..., 'Dec']
    datasets: Array // result of your stackedData
  })
  
  const chartData = computed(() => ({
    labels: props.labels,
    datasets: props.datasets
  }))
  
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: { stacked: true },
      y: {
      stacked: true,
      title: {
        display: true,
        text: 'Arbeitskraftstunden (h/ha)', 
        font: {
          size: 14,
          weight: 'bold'
        }
      }
    }
    },
    plugins: {
      legend: { labels: { color: '#000' } },
      tooltip: {
        callbacks: {
          label(context) {
            const dataset = context.dataset
            const index = context.dataIndex
            const value = context.parsed.y

            const customTip = dataset.customTooltips?.[index]
            const label = dataset.label

            return `${label} - ${customTip} : ${value.toFixed(2)}` //|| `${label}: ${value}`
          }
        }
      }
    }
  }
  </script>
  
  <style scoped>
  div {
    height: 100%;
  }
  canvas {
    height: 100% !important;
    width: 100% !important;
  }
  </style>
  