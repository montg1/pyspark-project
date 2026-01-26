<template>
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Country</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Wine Count</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Avg Points</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Avg Price</th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="country in countries.slice(0, 10)" :key="country.country" class="hover:bg-gray-50 transition-colors">
          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ country.country }}</td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{{ country.wine_count }}</td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
            <span class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-xs font-semibold">
              {{ country.avg_points || 'N/A' }}
            </span>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
            <span class="bg-green-100 text-green-800 px-3 py-1 rounded-full text-xs font-semibold">
              ${{ (country.avg_price || 0).toFixed(2) }}
            </span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'CountriesTable',
  props: {
    countries: Array,
  },
}
</script>
