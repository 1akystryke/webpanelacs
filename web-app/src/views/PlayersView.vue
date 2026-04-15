<template>
  <div class="card">
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
      <div class="section-title">{{ t.players.title }}</div>
      <button class="btn btn-secondary" @click="refreshIFrame" :disabled="server.status !== 'online'">
        {{ t.players.refresh }}
      </button>
    </div>
    <div v-if="server.status === 'online'">
      <div class="iframe-container">
        <iframe id="players-entry-iframe" src="/api/entry" title="Entry list"></iframe>
      </div>
      <p style="margin-top: 12px; font-size: 13px; color: #64748b; text-align: center;">
        {{ t.players.realtimeHint }}
      </p>
    </div>
    <div v-else class="empty-state">
      <span style="font-size: 40px;">🔌</span>
      <h3>{{ t.players.serverOffline }}</h3>
      <p>{{ t.players.goToDashboard }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  t: {
    type: Object,
    required: true
  },
  server: {
    type: Object,
    required: true
  },
  refreshIFrame: {
    type: Function,
    required: true
  }
})
</script>
