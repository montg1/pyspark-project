<template>
  <div>
    <canvas ref="chartRef"></canvas>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import Chart from 'chart.js/auto'

export default {
  name: 'QualityChart',
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
        type: 'doughnut',
        data: {
          labels: Object.keys(props.data),
          datasets: [
            {
              label: 'Wine Count',
              data: Object.values(props.data),
              backgroundColor: [
                'rgba(34, 197, 94, 0.8)',
                'rgba(59, 130, 246, 0.8)',
                'rgba(107, 114, 128, 0.8)',
              ],
              borderColor: [
                'rgba(34, 197, 94, 1)',
                'rgba(59, 130, 246, 1)',
                'rgba(107, 114, 128, 1)',
              ],
              borderWidth: 2,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                padding: 15,
                font: { size: 12 },
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
