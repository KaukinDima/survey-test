<template>
  <div class="bg-white rounded-2xl shadow p-4 col-span-12 lg:col-span-9">
    <div class="flex items-center justify-between mb-3">
      <h2 class="text-base font-semibold">Вопросы</h2>
      <div class="text-sm text-slate-600">
        <span v-if="activeCity">
          <span class="font-medium text-indigo-700">{{ activeCityName }}</span>
        </span>
      </div>
      <span v-if="loading" class="text-xs text-slate-500">Загрузка…</span>
    </div>
    <div v-if="questions.length">
      <div
        v-for="q in questions"
        :key="q.id"
        class="border border-slate-200 rounded-lg p-4 mb-3 hover:bg-slate-50"
      >
        <h3 class="font-medium text-slate-800 mb-2">{{ q.question }}</h3>
        <p class="text-xs text-slate-500 mb-3">
          Метрика:
          <span class="font-medium text-slate-700">{{ q.metric_name || "—" }}</span>
          ({{ q.metric_unit || "—" }})
        </p>

        <!-- Таблица значений -->
        <div class="overflow-x-auto">
          <table class="min-w-full text-xs border border-slate-200 rounded-md">
            <thead class="bg-slate-100">
              <tr>
                <th class="p-2 border-b border-slate-200 text-left w-32">Город</th>
                <th
                  v-for="(label, idx) in getOptionLabels(q)"
                  :key="idx"
                  class="p-2 border-b border-slate-200 text-left"
                >
                  {{ label }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(cityRow, idx) in q.city_values"
                :key="idx"
                class="hover:bg-slate-50"
              >
                <td class="p-2 border-b border-slate-100 font-medium">
                  {{ cityRow.city }}
                </td>
                <td
                  v-for="(label, i) in getOptionLabels(q)"
                  :key="i"
                  class="p-2 border-b border-slate-100 text-right tabular-nums"
                >
                  {{ formatValue(cityRow[label]) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-else class="text-xs text-slate-400">Нет данных для отображения.</div>
  </div>
</template>

<script>
export default {
  name: "QuestionsPanel",
  props: {
    questions: { type: Array, default: () => [] },
    loading: { type: Boolean, default: false },
    activeCity: { type: String, default: null },
    cities: { type: Array, default: () => [] },
  },
  computed: {
    activeCityName() {
      const city = this.cities.find(c => c.slug === this.activeCity);
      return city ? city.name : "";
    },
  },
  methods: {
    getOptionLabels(q) {
      if (!q || !Array.isArray(q.city_values) || !q.city_values.length) return [];
      const first = q.city_values.find(row => row && typeof row === "object");
      if (!first) return [];
      return Object.keys(first).filter(k => k !== "city");
    },
    formatValue(v) {
      if (v === undefined || v === null) return "—";
      const num = Number(v);
      return isNaN(num) ? v : `${num.toFixed(1)}%`;
    },
  },
};
</script>

<style scoped>
table {
  border-collapse: collapse;
  font-size: 13px;
}
th,
td {
  white-space: nowrap;
}
</style>
