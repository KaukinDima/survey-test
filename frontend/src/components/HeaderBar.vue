<template>
  <header class="border-b bg-white sticky top-0 z-50">
    <div class="mx-auto max-w-7xl px-4 py-3 flex items-center gap-3">
      <div class="text-xl font-semibold">Интерактивная карта Костанайской области</div>

      <div class="ml-auto flex items-center gap-3">
        <label class="text-sm text-slate-600">Квартал:</label>
        <select
          class="rounded-lg border px-2 py-1 text-sm"
          :value="currentQuarter"
          @change="$emit('change-quarter', $event.target.value)"
        >
          <option v-for="opt in quarterOptions" :key="opt" :value="opt">{{ opt }}</option>
        </select>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: "HeaderBar",
  props: {
    currentQuarter: { type: String, required: true },
    quarterOptions: { type: Array, required: true },
  },
  emits: ["change-quarter"],
};
</script>
