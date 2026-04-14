<template>
  <div class="card">
    <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
      <div>
        <div class="section-title">{{ t.logs.title }}</div>
        <p style="color: #64748b;">{{ t.logs.hint }}</p>
      </div>
      <div style="display: flex; gap: 12px;">
        <div class="auto-refresh-indicator" :class="{ active: logsAutoRefresh }">
          <span>{{ logsAutoRefresh ? '🔄' : '⏸️' }}</span>
          {{ logsAutoRefresh ? t.logs.autoRefreshOn : t.logs.autoRefreshOff }}
          <span v-if="logsAutoRefresh">({{ logsRefreshCountdown }}s)</span>
        </div>
        <button class="pause-btn" @click="toggleAutoRefresh">{{ logsAutoRefresh ? '⏸️' : '▶️' }}</button>
      </div>
    </div>
    <div class="logs-toolbar">
      <div style="display: flex; gap: 4px;">
        <span
          v-for="level in logLevels"
          :key="level"
          class="filter-badge"
          :class="{ active: logFilter === level }"
          @click="setLogFilter(level)"
        >
          {{ level === 'all' ? t.logs.all : level.toUpperCase() }}
        </span>
      </div>
      <div style="flex: 1;"></div>
      <button class="btn btn-secondary btn-small" @click="clearLogs">{{ t.logs.clear }}</button>
      <button class="btn btn-secondary btn-small" @click="fetchLogs" :disabled="logsLoading">
        <span v-if="logsLoading">⏳</span>
        <span v-else>{{ t.logs.refresh }}</span>
      </button>
    </div>
    <div v-if="filteredLogs.length > 0" class="logs-stats">
      {{ t.logs.showing }} {{ filteredLogs.length }} / {{ logs.length }} {{ t.logs.entries }}
    </div>
    <div class="logs-container" ref="logsContainer">
      <div v-if="filteredLogs.length === 0 && !logsLoading" style="color: #8b949e; text-align: center; padding: 40px;">
        {{ t.logs.noLogs }}
      </div>
      <div v-for="(log, index) in filteredLogs" :key="index" class="log-line" :class="getLogLevel(log)">
        <span class="log-level">{{ getLogLevelText(log) }}</span>
        <span class="log-message">{{ formatLogMessage(log) }}</span>
      </div>
      <div v-if="logsLoading && filteredLogs.length === 0" style="color: #8b949e; text-align: center; padding: 40px;">
        {{ t.logs.loading }}
      </div>
    </div>
    <p style="margin-top: 12px; font-size: 13px; color: #64748b; text-align: center;">
      {{ t.logs.autoRefreshHint }}
    </p>
  </div>
</template>

<script setup>
import { nextTick, ref, watch } from 'vue'

const props = defineProps({
  t: {
    type: Object,
    required: true
  },
  logs: {
    type: Array,
    required: true
  },
  filteredLogs: {
    type: Array,
    required: true
  },
  logsLoading: {
    type: Boolean,
    required: true
  },
  logsAutoRefresh: {
    type: Boolean,
    required: true
  },
  logsRefreshCountdown: {
    type: Number,
    required: true
  },
  logFilter: {
    type: String,
    required: true
  },
  logLevels: {
    type: Array,
    required: true
  },
  toggleAutoRefresh: {
    type: Function,
    required: true
  },
  clearLogs: {
    type: Function,
    required: true
  },
  fetchLogs: {
    type: Function,
    required: true
  },
  getLogLevel: {
    type: Function,
    required: true
  },
  getLogLevelText: {
    type: Function,
    required: true
  },
  formatLogMessage: {
    type: Function,
    required: true
  },
  setLogFilter: {
    type: Function,
    required: true
  }
})

const logsContainer = ref(null)

watch(
  () => props.filteredLogs.length,
  async () => {
    await nextTick()
    const container = logsContainer.value
    if (!container || !props.logsAutoRefresh) return
    const isNearBottom = container.scrollHeight - container.scrollTop - container.clientHeight < 100
    if (isNearBottom) container.scrollTop = container.scrollHeight
  }
)
</script>
