<template>
  <div>
    <div style="margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center">
      <div>
        <div class="section-title">{{ t.presets.title }}</div>
        <p style="color: #64748b; margin: 4px 0 0">{{ t.presets.hint }}</p>
      </div>
    </div>

    <div v-if="presets.length === 0" class="card" style="text-align: center; padding: 40px">
      <span style="font-size: 48px; margin-bottom: 16px; display: inline-block">🗂️</span>
      <div style="font-size: 18px; color: #64748b">{{ t.presets.noPresets }}</div>
    </div>

    <div class="presets-grid">
      <div v-for="preset in presets" :key="preset.name" class="preset-card">
        <!-- Header -->
        <div class="preset-header">
          <div class="preset-info">
            <div class="preset-title">{{ preset.name }}</div>
            <div class="preset-subtitle">
              {{ preset.track }} {{ preset.trackVariant ? `(${preset.trackVariant})` : "" }}
            </div>
          </div>
          <div class="preset-actions">
            <button class="btn-apply" @click="applyPreset(preset)">{{ t.presets.apply }}</button>
            <button class="btn-delete" @click="deletePreset(preset)">{{ t.presets.delete }}</button>
          </div>
        </div>

        <!-- Cars Section -->
        <div class="preset-section">
          <div class="preset-section-title">
            {{ t.presets.cars }}
            <span class="section-count">{{ preset.cars?.length || 0 }}</span>
          </div>
          <div v-if="preset.cars && preset.cars.length > 0" class="cars-list">
            <div v-for="(car, index) in preset.cars" :key="index" class="car-item">
              <div class="car-name">{{ car.name || car.id }}</div>
              <div class="car-params">
                <span v-if="car.restrictor" class="car-param">
                  {{ t.presets.restrictor }}: {{ car.restrictor }}%
                </span>
                <span v-if="car.ballast" class="car-param">
                  {{ t.presets.ballast }}: {{ car.ballast }}kg
                </span>
                <span v-if="car.skin" class="car-param">
                  {{ t.presets.skin }}: {{ car.skin }}
                </span>
              </div>
            </div>
          </div>
          <div v-else class="empty-state">
            {{ t.presets.noCars }}
          </div>
        </div>

        <!-- Session Parameters - Time -->
        <div class="preset-section">
          <div class="preset-section-title">{{ t.presets.sessionTime }}</div>
          <div class="params-grid">
            <div class="param-item">
              <span class="param-label">{{ t.presets.practice }}</span>
              <span class="param-value">{{ preset.practiceDuration ?? "-" }}</span>
            </div>
            <div class="param-item">
              <span class="param-label">{{ t.presets.qualifying }}</span>
              <span class="param-value">{{ preset.qualifyingDuration ?? "-" }}</span>
            </div>
            <div class="param-item">
              <span class="param-label">{{ t.presets.loopCount }}</span>
              <span class="param-value">{{ preset.raceLaps ?? "-" }}</span>
            </div>
          </div>
        </div>

        <!-- Session Parameters - Mode Settings -->
        <div class="preset-section">
          <div class="preset-section-title">{{ t.presets.modeSettings }}</div>
          <div class="params-grid">
            <div class="param-item">
              <span class="param-label">{{ t.presets.pickupMode }}</span>
              <span class="param-value" :class="{ active: preset.pickupMode == 1 }">
                {{ preset.pickupMode == 1 ? t.presets.enabled : t.presets.disabled }}
              </span>
            </div>
            <div class="param-item">
              <span class="param-label">{{ t.presets.loopMode }}</span>
              <span class="param-value" :class="{ active: preset.loopMode == 1 }">
                {{ preset.loopMode == 1 ? t.presets.enabled : t.presets.disabled }}
              </span>
            </div>
            <div class="param-item">
              <span class="param-label">{{ t.presets.registerToLobby }}</span>
              <span class="param-value" :class="{ active: preset.registerToLobby == 1 }">
                {{ preset.registerToLobby == 1 ? t.presets.enabled : t.presets.disabled }}
              </span>
            </div>
          </div>
        </div>

        <!-- Session Parameters - Tyre Settings -->
        <div class="preset-section">
          <div class="preset-section-title">{{ t.presets.tyreSettings }}</div>
          <div class="params-grid">
            <div class="param-item">
              <span class="param-label">{{ t.presets.tyreWear }}</span>
              <span class="param-value">{{ preset.tyreWear ?? "-" }}</span>
            </div>
            <div class="param-item">
              <span class="param-label">{{ t.presets.allowedTyresOut }}</span>
              <span class="param-value">{{ preset.allowedTyresOut ?? "-" }}</span>
            </div>
            <div class="param-item">
              <span class="param-label">{{ t.presets.legalTyres }}</span>
              <span class="param-value">{{ preset.legalTyres ?? "-" }}</span>
            </div>
            <div class="param-item">
              <span class="param-label">{{ t.presets.tyreBlanketsAllowed }}</span>
              <span class="param-value" :class="{ active: preset.tyreBlanketsAllowed == 1 }">
                {{ preset.tyreBlanketsAllowed == 1 ? t.presets.enabled : t.presets.disabled }}
              </span>
            </div>
          </div>
        </div>

        <!-- Session Parameters - Assist Settings -->
        <div class="preset-section">
          <div class="preset-section-title">{{ t.presets.assistSettings }}</div>
          <div class="params-grid params-grid-single">
            <div class="param-item">
              <span class="param-label">{{ t.presets.absAllowed }}</span>
              <span class="param-value" :class="{ active: preset.absAllowed == 1 }">
                {{ preset.absAllowed == 1 ? t.presets.enabled : t.presets.disabled }}
              </span>
            </div>
            <div class="param-item">
              <span class="param-label">{{ t.presets.tcAllowed }}</span>
              <span class="param-value" :class="{ active: preset.tcAllowed == 1 }">
                {{ preset.tcAllowed == 1 ? t.presets.enabled : t.presets.disabled }}
              </span>
            </div>
            <div class="param-item">
              <span class="param-label">{{ t.presets.stabilityAllowed }}</span>
              <span class="param-value" :class="{ active: preset.stabilityAllowed == 1 }">
                {{ preset.stabilityAllowed == 1 ? t.presets.enabled : t.presets.disabled }}
              </span>
            </div>
            <div class="param-item">
              <span class="param-label">{{ t.presets.autoclutchAllowed }}</span>
              <span class="param-value" :class="{ active: preset.autoclutchAllowed == 1 }">
                {{ preset.autoclutchAllowed == 1 ? t.presets.enabled : t.presets.disabled }}
              </span>
            </div>
            <div class="param-item">
              <span class="param-label">{{ t.presets.forceVirtualMirror }}</span>
              <span class="param-value" :class="{ active: preset.forceVirtualMirror == 1 }">
                {{ preset.forceVirtualMirror == 1 ? t.presets.enabled : t.presets.disabled }}
              </span>
            </div>
          </div>
        </div>

        <!-- Other Parameters -->
        <div class="preset-section">
          <div class="preset-section-title">{{ t.presets.otherSettings }}</div>
          <div class="params-grid">
            <div class="param-item">
              <span class="param-label">{{ t.presets.damage }}</span>
              <span class="param-value">{{ preset.damage ?? "-" }}</span>
            </div>
            <div class="param-item">
              <span class="param-label">{{ t.presets.fuelConsumption }}</span>
              <span class="param-value">{{ preset.fuelConsumption ?? "-" }}</span>
            </div>
            <div class="param-item">
              <span class="param-label">{{ t.presets.sunAngle }}</span>
              <span class="param-value">{{ preset.sunAngle ?? "-" }}</span>
            </div>
          </div>
        </div>

        <!-- Weather Section -->
        <div class="preset-section">
          <div class="preset-section-title">{{ t.presets.weather }}</div>
          <div v-if="preset.weather && preset.weather.length > 0" class="weather-list">
            <div v-for="(slot, index) in preset.weather" :key="index" class="weather-item">
              <span class="weather-graphics">{{ slot.graphics }}</span>
              <span class="weather-temp">{{ slot.baseTemperatureAmbient }} / {{ slot.baseTemperatureRoad }}</span>
            </div>
          </div>
          <div v-else class="empty-state">
            {{ t.presets.noWeather }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  t: { type: Object, required: true },
  presets: { type: Array, required: true },
  applyPreset: { type: Function, required: true },
  deletePreset: { type: Function, required: true },
});
</script>

<style scoped>
.presets-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
  gap: 20px;
}

.preset-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  transition: box-shadow 0.2s ease;
  min-width: 0;
  overflow-x: auto;
}

.preset-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.preset-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e5e7eb;
  flex-wrap: wrap;
}

.preset-info {
  flex: 1;
  min-width: 0;
}

.preset-title {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 4px;
  word-break: break-word;
  overflow-wrap: break-word;
}

.preset-subtitle {
  font-size: 13px;
  color: #6b7280;
  word-break: break-word;
  overflow-wrap: break-word;
}

.preset-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.preset-actions button {
  padding: 6px 12px;
  font-size: 13px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
  white-space: nowrap;
}

.btn-apply {
  background: #dc2626;
  color: white;
}

.btn-apply:hover {
  background: #b91c1c;
}

.btn-delete {
  background: #f3f4f6;
  color: #6b7280;
  border: 1px solid #e5e7eb;
}

.btn-delete:hover {
  background: #e5e7eb;
  color: #dc2626;
}

.preset-section {
  margin-top: 20px;
}

.preset-section-title {
  font-weight: 600;
  font-size: 14px;
  color: #374151;
  margin-bottom: 12px;
  padding-bottom: 6px;
  border-bottom: 1px solid #f3f4f6;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.section-count {
  background: #f3f4f6;
  color: #6b7280;
  font-size: 11px;
  font-weight: 500;
  padding: 2px 6px;
  border-radius: 10px;
}

.params-grid {
  display: grid;
  gap: 8px;
  grid-template-columns: repeat(2, 1fr);
}

.params-grid-single {
  grid-template-columns: 1fr;
}

.param-item {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 12px;
  font-size: 13px;
  padding: 6px 0;
  min-width: 0;
}

.param-label {
  color: #6b7280;
  flex-shrink: 0;
  max-width: 70%;
  word-break: break-word;
  overflow-wrap: break-word;
}

.param-value {
  color: #374151;
  font-weight: 500;
  text-align: right;
  flex-shrink: 0;
  word-break: keep-all;
}

.param-value.active {
  color: #10b981;
}

.cars-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 300px;
  overflow-y: auto;
  padding-right: 4px;
}

.cars-list::-webkit-scrollbar {
  width: 6px;
}

.cars-list::-webkit-scrollbar-track {
  background: #f3f4f6;
  border-radius: 3px;
}

.cars-list::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.cars-list::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.car-item {
  background: #f9fafb;
  padding: 10px 12px;
  border-radius: 8px;
  border-left: 3px solid #dc2626;
  transition: all 0.2s ease;
  word-break: break-word;
  overflow-wrap: break-word;
}

.car-item:hover {
  background: #f3f4f6;
}

.car-name {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 6px;
  font-size: 13px;
  word-break: break-word;
  overflow-wrap: break-word;
}

.car-params {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  font-size: 12px;
  color: #6b7280;
}

.car-param {
  color: #6b7280;
  word-break: break-word;
  overflow-wrap: break-word;
}

.weather-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.weather-item {
  background: #f9fafb;
  padding: 8px 12px;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  font-size: 13px;
  flex-wrap: wrap;
}

.weather-graphics {
  font-weight: 500;
  color: #374151;
  word-break: break-word;
  overflow-wrap: break-word;
}

.weather-temp {
  color: #6b7280;
  font-size: 12px;
  flex-shrink: 0;
  white-space: nowrap;
}

.empty-state {
  text-align: center;
  padding: 16px;
  color: #9ca3af;
  font-size: 13px;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px dashed #e5e7eb;
  word-break: break-word;
  overflow-wrap: break-word;
}

/* Адаптация для маленьких экранов */
@media (max-width: 768px) {
  .presets-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .preset-card {
    padding: 16px;
  }
  
  .params-grid {
    grid-template-columns: 1fr;
    gap: 6px;
  }
  
  .param-item {
    padding: 4px 0;
  }
  
  .preset-header {
    flex-direction: column;
  }
  
  .preset-actions {
    width: 100%;
  }
  
  .preset-actions button {
    flex: 1;
    white-space: nowrap;
  }
  
  .weather-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .weather-temp {
    white-space: normal;
  }
}

/* Адаптация для очень длинных слов */
@media (max-width: 480px) {
  .preset-card {
    padding: 12px;
  }
  
  .param-label {
    max-width: 60%;
    font-size: 12px;
  }
  
  .param-value {
    font-size: 12px;
  }
  
  .car-params {
    flex-direction: column;
    gap: 4px;
  }
}
</style>