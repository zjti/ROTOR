<template>
    <div style="height: 100%">
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
  
  // Register Bar chart components
  ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend)
  
  const props = defineProps({
    labels: Array,
    data: Array,
    title: String
  })
  
  // Chart data
  const chartData = computed(() => ({
    labels: props.labels,
    datasets: [
      {
        label: props.title,
        data: props.data,
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderRadius: 4,
        barThickness: 'flex'
      }
    ]
  }))
  
  // Chart options
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        ticks: {
          color: '#000',
          maxTicksLimit: 12
        }
      },
      y: {
        ticks: {
          color: '#000'
        }
      }
    },
    plugins: {
      legend: {
        labels: {
          color: '#000'
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
  