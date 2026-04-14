<template>
  <div class="card" style="grid-column: span 2;">
    <div class="card-title"><span>🌤️</span> {{ t.session.weatherCard }}</div>
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
      <p style="color: #64748b; font-size: 14px;">{{ t.session.weatherHint }}</p>
      <button class="btn btn-secondary btn-small" @click="addWeatherSlot">+ {{ t.session.addWeatherSlot }}</button>
    </div>
    <div class="weather-slots-container">
      <div v-for="(slot, index) in weather" :key="index" class="weather-slot">
        <div class="weather-slot-header">
          <div class="weather-slot-title">{{ t.session.weatherSlot }} {{ index + 1 }}</div>
          <button
            v-if="weather.length > 1"
            class="btn-icon"
            @click="removeWeatherSlot(index)"
            :title="t.session.removeWeatherSlot"
          >
            ✕
          </button>
        </div>
        <div class="weather-grid">
          <div>
            <div class="label">{{ t.session.graphics }}</div>
            <select v-model="slot.graphics" class="input">
              <option v-for="item in weatherList" :key="item.weather" :value="item.weather">
                {{ item.pretty_name }}
              </option>
            </select>
          </div>
          <div></div>
          <div>
            <div class="label">{{ t.session.baseTempAmbient }}</div>
            <input v-model.number="slot.baseTemperatureAmbient" type="number" class="input" />
          </div>
          <div>
            <div class="label">{{ t.session.baseTempRoad }}</div>
            <input v-model.number="slot.baseTemperatureRoad" type="number" class="input" />
          </div>
          <div>
            <div class="label">{{ t.session.variationAmbient }}</div>
            <input v-model.number="slot.variationAmbient" type="number" class="input" />
          </div>
          <div>
            <div class="label">{{ t.session.variationRoad }}</div>
            <input v-model.number="slot.variationRoad" type="number" class="input" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  t: {
    type: Object,
    required: true
  },
  weather: {
    type: Array,
    required: true
  },
  weatherList: {
    type: Array,
    required: true
  },
  addWeatherSlot: {
    type: Function,
    required: true
  },
  removeWeatherSlot: {
    type: Function,
    required: true
  }
})
</script>
