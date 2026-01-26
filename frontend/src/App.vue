<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50">
    <!-- Header -->
    <header class="bg-white shadow-sm sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">🍷 Wine Reviews</h1>
            <p class="text-gray-600 mt-1">Explore 58,000+ wine reviews from around the world</p>
          </div>
          <div v-if="apiStatus" class="flex items-center space-x-2">
            <div class="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
            <span class="text-sm text-green-600 font-medium">API Connected</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Stats Cards -->
      <section v-if="loading" class="mb-12">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div v-for="i in 4" :key="i" class="bg-white rounded-lg shadow p-6 animate-pulse">
            <div class="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
            <div class="h-8 bg-gray-200 rounded w-3/4"></div>
          </div>
        </div>
      </section>

      <section v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        <StatsCard 
          title="Total Wines" 
          :value="stats.totalWines" 
          icon="📊"
          color="blue"
        />
        <StatsCard 
          title="Quality: Excellent" 
          :value="stats.qualityDistribution.Excellent || 0" 
          icon="⭐"
          color="yellow"
        />
        <StatsCard 
          title="Quality: Good" 
          :value="stats.qualityDistribution.Good || 0" 
          icon="✓"
          color="green"
        />
        <StatsCard 
          title="Average Price" 
          :value="`$${stats.avgPrice.toFixed(2)}`" 
          icon="💰"
          color="purple"
        />
      </section>

      <!-- Charts Section -->
      <section v-if="!loading" class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        <div class="bg-white rounded-lg shadow-lg p-6">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">Quality Distribution</h2>
          <QualityChart :data="stats.qualityDistribution" />
        </div>

        <div class="bg-white rounded-lg shadow-lg p-6">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">Price Categories</h2>
          <PriceChart :data="stats.priceDistribution" />
        </div>
      </section>

      <!-- Top Varieties -->
      <section v-if="!loading" class="bg-white rounded-lg shadow-lg p-6 mb-12">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">Top Wine Varieties</h2>
        <TopVarietiesTable :varieties="stats.topVarieties" />
      </section>

      <!-- Top Countries -->
      <section v-if="!loading" class="bg-white rounded-lg shadow-lg p-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">Top Countries</h2>
        <CountriesTable :countries="stats.countries" />
      </section>
    </main>

    <!-- Footer -->
    <footer class="bg-gray-900 text-gray-300 mt-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <p class="text-center text-sm">
          Wine Reviews Dashboard • Built with Vue 3, FastAPI, and PySpark
        </p>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { wineApi } from '@/api/client'
import StatsCard from '@/components/StatsCard.vue'
import QualityChart from '@/components/QualityChart.vue'
import PriceChart from '@/components/PriceChart.vue'
import TopVarietiesTable from '@/components/TopVarietiesTable.vue'
import CountriesTable from '@/components/CountriesTable.vue'

export default {
  name: 'App',
  components: {
    StatsCard,
    QualityChart,
    PriceChart,
    TopVarietiesTable,
    CountriesTable,
  },
  setup() {
    const loading = ref(true)
    const apiStatus = ref(false)
    const stats = ref({
      totalWines: 0,
      qualityDistribution: {},
      priceDistribution: {},
      topVarieties: [],
      countries: [],
      avgPrice: 0,
    })

    const fetchData = async () => {
      try {
        loading.value = true

        // Check API health
        try {
          await wineApi.health()
          apiStatus.value = true
        } catch (err) {
          console.warn('API not available')
          apiStatus.value = false
        }

        // Fetch all data
        const [countryRes, qualityRes, priceRes, varietiesRes, countRes] = await Promise.all([
          wineApi.getCountryStats(),
          wineApi.getQualityDistribution(),
          wineApi.getPriceDistribution(),
          wineApi.getTopVarieties(15),
          wineApi.getTotalCount(),
        ])

        stats.value.countries = countryRes.data
        stats.value.qualityDistribution = qualityRes.data
        stats.value.priceDistribution = priceRes.data
        stats.value.topVarieties = varietiesRes.data
        stats.value.totalWines = countRes.data.total_wines

        // Calculate average price
        if (stats.value.countries.length > 0) {
          const avgPrice = stats.value.countries.reduce((sum, c) => sum + (c.avg_price || 0), 0) / stats.value.countries.length
          stats.value.avgPrice = avgPrice
        }
      } catch (error) {
        console.error('Error fetching data:', error)
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      fetchData()
      // Refresh data every 30 seconds
      setInterval(fetchData, 30000)
    })

    return {
      loading,
      apiStatus,
      stats,
    }
  },
}
</script>
