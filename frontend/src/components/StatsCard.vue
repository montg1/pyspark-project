<template>
  <div class="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-6 border border-blue-200 hover:shadow-lg transition-shadow">
    <div class="flex items-center justify-between">
      <div>
        <p class="text-blue-600 font-semibold text-sm uppercase tracking-wide">{{ title }}</p>
        <p class="text-3xl font-bold text-gray-900 mt-2">{{ value }}</p>
      </div>
      <div class="text-5xl">{{ icon }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StatsCard',
  props: {
    title: String,
    value: [String, Number],
    icon: String,
    color: String,
  },
}
</script>
