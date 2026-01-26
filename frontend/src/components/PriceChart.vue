<template>
  <div>
    <canvas ref="chartRef"></canvas>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import Chart from 'chart.js/auto'

export default {
  name: 'PriceChart',
  props: {
    data: Object,
  },
  setup(props) {
    const chartRef = ref(null)
    let chartInstance = null

    const createChart = () => {
      if (!chartRef.value || !props.data || Object.keys(props.data).length === 0) return

      const ctx = chartRef.value.getContext('2d')

      if (chartInstance) {
        chartInstance.destroy()
      }

      chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: Object.keys(props.data),
          datasets: [
            {
              label: 'Wine Count',
              data: Object.values(props.data),
              backgroundColor: 'rgba(168, 85, 247, 0.8)',
              borderColor: 'rgba(168, 85, 247, 1)',
              borderWidth: 1,
              borderRadius: 4,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            legend: {
              display: false,
            },
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: function (value) {
                  return value.toLocaleString()
                },
              },
            },
          },
        },
      })
    }

    onMounted(() => {
      createChart()
    })

    watch(() => props.data, () => {
      createChart()
    }, { deep: true })

    return { chartRef }
  },
}
</script>
