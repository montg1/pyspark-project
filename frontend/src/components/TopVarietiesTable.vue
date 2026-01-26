<template>
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Rank</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Variety</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Count</th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="(variety, idx) in varieties" :key="variety.variety" class="hover:bg-gray-50 transition-colors">
          <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-blue-600">{{ idx + 1 }}</td>
          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ variety.variety }}</td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{{ variety.count.toLocaleString() }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'TopVarietiesTable',
  props: {
    varieties: Array,
  },
}
</script>
