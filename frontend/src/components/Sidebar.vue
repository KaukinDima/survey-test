<template>
  <aside class="flex flex-col gap-4">
    <!-- Поиск -->
    <div class="bg-white rounded-2xl shadow p-3">
      <div class="text-sm font-medium mb-2">Поиск по вопросам</div>
      <div class="relative flex gap-2">
        <input
          type="search"
          :value="search"
          @input="$emit('update:search', $event.target.value)"
          placeholder="введите слово или код вопроса…"
          class="w-full rounded-xl border border-slate-200 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
        <button @click="$emit('run-search')" class="px-3 py-2 text-sm rounded-lg bg-indigo-600 text-white">Найти</button>
      </div>
    </div>

    <!-- Территории -->
    <div class="bg-white rounded-2xl shadow p-3">
      <div class="flex items-center justify-between">
        <div class="text-sm font-medium">Территории</div>
        <button @click="$emit('reset-all')" class="text-xs px-2 py-1 rounded-lg bg-slate-100 hover:bg-slate-200">Сбросить всё</button>
      </div>
      <ul class="mt-2 space-y-1 text-sm max-h-80 overflow-auto">
        <li v-for="c in cities" :key="c.slug">
          <button
            class="w-full text-left px-2 py-1 rounded-lg hover:bg-slate-100"
            @click="$emit('select-city', c.slug)"
          >
            {{ c.name }}
          </button>
        </li>
      </ul>
    </div>

    <!-- Разделы (= surveys этой волны) -->
    <div class="bg-white rounded-2xl shadow p-3">
      <div class="text-sm font-medium mb-2">Разделы</div>
      <nav class="space-y-1 text-sm">
        <button
          v-for="s in sections"
          :key="s.id"
          class="block w-full text-left px-2 py-1 rounded-lg hover:bg-slate-100"
          :class="{'bg-slate-100 font-semibold': s.id === activeSectionId}"
          @click="$emit('select-section', s.id)"
        >
          {{ s.title }}
        </button>
      </nav>
    </div>
  </aside>
</template>

<script>
export default {
  name: "Sidebar",
  props: {
    cities: { type: Array, default: () => [] },
    sections: { type: Array, default: () => [] }, // surveys
    activeCity: { type: String, default: null },
    activeSectionId: { type: Number, default: null }, // текущий survey
    search: { type: String, default: "" },
  },
};
</script>
