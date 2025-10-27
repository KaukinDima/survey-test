<!-- src/components/MapPanel.vue -->
<template>
  <div class="bg-white rounded-2xl shadow p-3">
    <div class="text-sm font-medium mb-2 flex justify-between items-center">
      <span>Карта (Leaflet)</span>
      <span class="text-xs text-slate-400">
        Клик по району = выделение
      </span>
    </div>
    <div ref="mapEl" id="map" class="w-full h-[480px] rounded-xl border border-slate-200"></div>
  </div>
</template>

<script>
import L from "leaflet";
import "leaflet/dist/leaflet.css";

export default {
  name: "MapPanel",
  props: {
    cities: { type: Array, default: () => [] },
    activeCity: { type: String, default: null },
  },
  data() {
    return {
      map: null,
      oblastLayer: null,
      cityLayers: {},
      outlineColors: [
        "#ef4444", "#f97316", "#f59e0b", "#eab308", "#84cc16",
        "#22c55e", "#10b981", "#14b8a6", "#06b6d4", "#0ea5e9",
        "#3b82f6", "#6366f1", "#8b5cf6", "#a855f7", "#d946ef",
        "#ec4899", "#f43f5e", "#fb7185", "#fdba74", "#a3e635"
      ],
    };
  },
  watch: {
    cities: { handler() { this.renderAll(); }, deep: true },
    activeCity() { this.highlightActive(); },
  },
  mounted() {
    this.map = L.map(this.$refs.mapEl, { zoomControl: true }).setView([53.2, 63.6], 6);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 18,
      attribution: "© OpenStreetMap",
    }).addTo(this.map);

    this.renderAll();
  },
  methods: {
    parseFeature(f) {
      if (!f) return null;
      if (typeof f === "string") {
        try { return JSON.parse(f); } catch { return null; }
      }
      return f;
    },

    clearMap() {
      this.map.eachLayer(layer => {
        if (layer instanceof L.TileLayer) return; // оставляем OSM
        this.map.removeLayer(layer);
      });
      this.cityLayers = {};
      this.oblastLayer = null;
    },

    renderAll() {
      if (!this.map || !this.cities.length) return;
      this.clearMap();

      // 1️⃣ Область (фон)
      const oblast = this.cities.find(c => c.is_oblast);
      if (oblast) {
        const feat = this.parseFeature(oblast.feature);
        if (feat) {
          this.oblastLayer = L.geoJSON(feat, {
            style: {
              color: "#9ca3af",
              weight: 1.2,
              fillColor: "#cbd5e1",
              fillOpacity: 0.1,
            },
          }).addTo(this.map);
          this.oblastLayer.bringToBack();
        }
      }

      // 2️⃣ Районы
      const districts = this.cities
        .filter(c => !c.is_oblast)
        .slice()
        .sort((a, b) => (a.sort_order ?? 0) - (b.sort_order ?? 0));

      districts.forEach((city, idx) => {
        const feat = this.parseFeature(city.feature);
        if (!feat) return;

        const color = this.outlineColors[idx % this.outlineColors.length];

        const layer = L.geoJSON(feat, {
          style: {
            color,
            weight: 2,
            opacity: 1,
            fillOpacity: 0,
          },
        });

        // hover-подсветка без tooltip
        layer.on("mouseover", (e) => {
          e.target.setStyle({ weight: 3.5, opacity: 1 });
        });
        layer.on("mouseout", (e) => {
          e.target.setStyle({ weight: 2, opacity: 1 });
        });

        // клик — выбор города
        layer.on("click", () => this.$emit("select-city", city.slug));

        layer.addTo(this.map);
        this.cityLayers[city.slug] = layer;
      });

      this.$nextTick(() => {
        this.highlightActive();
        this.map.invalidateSize();
      });
    },

    highlightActive() {
      if (!this.map) return;

      // сброс стилей
      Object.entries(this.cityLayers).forEach(([slug, layer]) => {
        const idx = Object.keys(this.cityLayers).indexOf(slug);
        const color = this.outlineColors[idx % this.outlineColors.length];
        layer.setStyle({ color, weight: 2, fillOpacity: 0 });
      });

      // выделение выбранного
      const activeLayer = this.activeCity && this.cityLayers[this.activeCity];
      if (activeLayer) {
        activeLayer.setStyle({
          color: "#1e3a8a",
          weight: 4,
          fillOpacity: 0.25,
          fillColor: "#3b82f6",
        });
        activeLayer.bringToFront();
        const bounds = activeLayer.getBounds();
        if (bounds.isValid()) {
          this.map.fitBounds(bounds, { padding: [20, 20], maxZoom: 9 });
        }
      } else if (this.oblastLayer) {
        const b = this.oblastLayer.getBounds();
        if (b.isValid()) this.map.fitBounds(b, { padding: [16, 16] });
      }
    },
  },
};
</script>

<style>
#map {
  contain: layout paint;
}

/* отключаем названия/подсказки */
.leaflet-tooltip,
.city-tooltip {
  display: none !important;
}

.leaflet-marker-icon {
  display: none !important;
}
</style>
