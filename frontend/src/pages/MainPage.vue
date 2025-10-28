<template>
  <div class="bg-slate-50 text-slate-800 min-h-screen">
    <HeaderBar
      :current-quarter="currentQuarter"
      :quarter-options="quarterOptions"
      @change-quarter="onQuarterChange"
    />

    <main class="mx-auto max-w-7xl px-4 py-6 grid grid-cols-12 gap-4">
      <!-- Сайдбар -->
      <Sidebar
        class="col-span-12 lg:col-span-3"
        :cities="cities"
        :sections="sections"
        :active-city="activeCity"
        :active-section-id="currentSurveyId"
        :search="search"
        @update:search="val => search = val"
        @run-search="loadQuestions"
        @select-city="selectCity"
        @select-section="selectSection"
        @reset-all="resetAll"
        @scroll-to="scrollTo"
      />

      <!-- Основная панель -->
      <div class="col-span-12 lg:col-span-9 space-y-4">
        <MapPanel
          :cities="cities"
          :active-city="activeCity"
          @select-city="selectCity"
        />

        <QuestionsPanel
          :questions="questions"
          :loading="questionsLoading"
          :active-city="activeCity"
          :cities="cities"
        />
      </div>
    </main>
  </div>
</template>

<script>
import HeaderBar from "@/components/HeaderBar.vue";
import Sidebar from "@/components/Sidebar.vue";
import MapPanel from "@/components/MapPanel.vue";
import QuestionsPanel from "@/components/QuestionsPanel.vue";
import { fetchCities, fetchSurveysByWaveCode, fetchGroupedQuestions } from "@/composables/useApi";

export default {
  name: "MainPage",
  components: { HeaderBar, Sidebar, MapPanel, QuestionsPanel },
  data() {
    return {
      currentQuarter: "2025Q3",
      quarterOptions: ["2025Q3", "2025Q4", "2025M07", "2025M08", "2025M09"],

      cities: [],
      activeCity: null,
      defaultRegionSlug: "kostanayskaya-oblast",

      sections: [],
      currentSurveyId: null,

      search: "",
      questions: [],
      questionsLoading: false,
    };
  },

  async mounted() {
    await this.loadCities();
    const oblast = this.cities.find(c => c.slug === this.defaultRegionSlug);
    if (oblast) this.activeCity = oblast.slug;

    await this.loadSections();
    if (this.sections.length) {
      this.currentSurveyId = this.sections[0].id;
    }

    await this.loadQuestions();
  },

  methods: {
    async loadCities() {
      try {
        this.cities = await fetchCities();
      } catch (e) {
        console.error("cities error", e);
      }
    },

    async loadSections() {
      try {
        const surveys = await fetchSurveysByWaveCode(this.currentQuarter);
        this.sections = Array.isArray(surveys) ? surveys : [];
      } catch (e) {
        console.error("surveys error", e);
        this.sections = [];
      }
    },

    async loadQuestions() {
      this.questionsLoading = true;
      try {
        const response = await fetchGroupedQuestions({
          wave: this.currentQuarter,
          survey_id: this.currentSurveyId,
          city: this.activeCity,
        });
        this.questions = response;
      } catch (e) {
        console.error("questions error", e);
      } finally {
        this.questionsLoading = false;
      }
    },
    async onQuarterChange(code) {
      this.currentQuarter = code;
      await this.loadSections();
      this.currentSurveyId = this.sections[0]?.id || null;
      await this.loadQuestions();
    },

    async selectCity(slug) {
      this.activeCity = slug;
      // фильтрация по городу (опционально)
      await this.loadQuestions();
    },

    async selectSection(surveyId) {
      this.currentSurveyId = surveyId;
      await this.loadQuestions();
    },

    async resetAll() {
      this.search = "";
      await this.loadQuestions();
    },

    scrollTo(id) {
      const el = document.getElementById(id);
      if (el) el.scrollIntoView({ behavior: "smooth" });
    },
  },
};
</script>
