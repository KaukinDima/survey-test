<template>
  <div class="bg-white rounded-2xl shadow p-3 col-span-12 lg:col-span-9">
    <div class="flex items-center justify-between mb-2">
      <div class="text-sm font-medium">Вопросы</div>
      <div v-if="loading" class="text-xs text-slate-500">Загрузка…</div>
    </div>

    <ul v-if="questions.length" class="space-y-2">
      <li v-for="q in questions" :key="q.id" class="border rounded-lg p-2 hover:bg-slate-50">
        <div class="font-medium">{{ q.code ? (q.code + '. ') : '' }}{{ q.title }}</div>
        <div v-if="q.section" class="text-xs text-slate-500 mt-1">Раздел: {{ q.section.title }}</div>
      </li>
    </ul>
    <div v-else class="text-xs text-slate-400">Нет результатов.</div>
  </div>
</template>

<script>
export default {
  name: "QuestionsPanel",
  props: {
    questions: { type: Array, default: () => [] },
    loading: { type: Boolean, default: false },
  },
};
</script>
