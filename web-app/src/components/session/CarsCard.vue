<template>
  <div class="card" style="display: flex; flex-direction: column;">
    <div class="card-title"><span>🏎️</span> {{ t.session.carsCard }}</div>
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
      <div class="label" style="margin-bottom: 0;">{{ t.session.carsLabel }} ({{ session.cars.length }})</div>
      <button class="btn btn-secondary btn-small" @click="addCar">+ {{ t.session.addCar }}</button>
    </div>

    <div class="car-list">
      <div
        v-if="session.cars.length === 0"
        style="padding: 24px; text-align: center; color: #94a3b8; background: #f8fafc; border-radius: 20px;"
      >
        {{ t.session.noCars }}
      </div>

      <div v-for="(car, idx) in session.cars" :key="idx" class="car-card">
        <div class="car-card-header">
          <div class="car-model-select">
            <select v-model="car.model" class="input">
              <option v-for="carOption in cars" :key="carOption.id" :value="carOption.id">
                {{ carOption.name }}
              </option>
            </select>
          </div>

          <div class="car-skin-select">
            <select v-model="car.skin" class="input">
              <option v-for="skin in getCarSkins(car.model)" :key="skin" :value="skin">
                {{ skin }}
              </option>
            </select>
          </div>
          <button class="remove-car-btn" @click="removeCar(idx)" :title="t.session.remove">✕</button>
        </div>

        <div class="car-card-controls">
          <div class="restrictor-group">
            <span>🔧</span>
            <input v-model.number="car.restrictor" type="number" min="0" max="100" step="1" placeholder="0" />
            <span>%</span>
          </div>
          <div class="ballast-group">
            <span>⚖️</span>
            <input v-model.number="car.ballast" type="number" min="0" step="1" placeholder="0" />
            <span>{{ t.session.kg }}</span>
          </div>
        </div>
      </div>
    </div>
    <p style="margin-top: 20px; font-size: 13px; color: #94a3b8;">{{ t.session.restrictorHint }}</p>
  </div>
</template>

<script setup>
defineProps({
  session: {
    type: Object,
    required: true
  },
  cars: {
    type: Array,
    required: true
  },
  t: {
    type: Object,
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
  getCarSkins: {
    type: Function,
    required: true
  }
})
</script>
