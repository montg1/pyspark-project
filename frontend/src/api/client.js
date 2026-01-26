import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const wineApi = {
  // Health check
  health() {
    return api.get('/health')
  },

  // Statistics endpoints
  getCountryStats() {
    return api.get('/stats/countries')
  },

  getQualityDistribution() {
    return api.get('/stats/quality-distribution')
  },

  getPriceDistribution() {
    return api.get('/stats/price-distribution')
  },

  getTopVarieties(limit = 10) {
    return api.get('/stats/top-varieties', { params: { limit } })
  },

  getTotalCount() {
    return api.get('/stats/total-count')
  },

  // Wine data
  getWines(limit = 100, offset = 0) {
    return api.get('/wines', { params: { limit, offset } })
  },
}

export default api
