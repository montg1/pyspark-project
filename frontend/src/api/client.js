import axios from 'axios'

// Use relative API path for Docker compatibility
// In Docker: http://frontend/api/ proxies to http://backend:8000/
// In dev: http://localhost:5173/api/ proxies to http://localhost:8000/
const API_BASE_URL = '/api'

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
