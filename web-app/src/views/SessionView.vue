<template>
  <div>
    <div style="margin-bottom: 24px;">
      <div class="section-title">{{ t.session.title }}</div>
      <p style="color: #64748b;">{{ t.session.changesHint }}</p>
    </div>

    <div class="session-cards-grid">
      <ServerCard :session="session" :t="t" />
      <TrackCard :session="session" :tracks="tracks" :t="t" />
      <CarsCard
        :session="session"
        :cars="cars"
        :t="t"
        :add-car="addCar"
        :remove-car="removeCar"
        :get-car-skins="getCarSkins"
      />
      <SessionParamsCard :session="session" :t="t" />
      <WeatherCard
        :t="t"
        :weather="weather"
        :weather-list="weatherList"
        :add-weather-slot="addWeatherSlot"
        :remove-weather-slot="removeWeatherSlot"
      />
    </div>

    <div style="margin-top: 32px; text-align: right;">
      <button class="btn btn-primary" style="padding: 16px 40px; font-size: 17px;" @click="saveSession" :disabled="saving">
        <span v-if="saving"><span class="spinner"></span> {{ t.session.saving }}</span>
        <span v-else>{{ t.session.saveSession }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import ServerCard from '../components/session/ServerCard.vue'
import TrackCard from '../components/session/TrackCard.vue'
import CarsCard from '../components/session/CarsCard.vue'
import SessionParamsCard from '../components/session/SessionParamsCard.vue'
import WeatherCard from '../components/session/WeatherCard.vue'

defineProps({
  t: {
    type: Object,
    required: true
  },
  session: {
    type: Object,
    required: true
  },
  tracks: {
    type: Array,
    required: true
  },
  cars: {
    type: Array,
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
  saving: {
    type: Boolean,
    required: true
  },
  addCar: {
    type: Function,
    required: true
  },
  removeCar: {
    type: Function,
    required: true
  },
  addWeatherSlot: {
    type: Function,
    required: true
  },
  removeWeatherSlot: {
    type: Function,
    required: true
  },
  saveSession: {
    type: Function,
    required: true
  },
  getCarSkins: {
    type: Function,
    required: true
  }
})
</script>
