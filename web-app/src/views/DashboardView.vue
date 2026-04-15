<template>
  <div class="flex">
    <div v-if="server.status === 'online'" class="card" style="flex: 2; min-width: 280px;">
      <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 16px;">
        <span style="font-size: 32px;">🏁</span>
        <div>
          <div style="font-size: 20px; font-weight: 600; color: #64748b;">{{ t.dashboard.currentTrack }}</div>
          <div style="font-size: 32px; font-weight: 700; line-height: 1.2;">{{ server.track || '—' }}</div>
        </div>
      </div>
      <div style="display: flex; align-items: baseline; gap: 8px;">
        <span style="font-size: 56px; font-weight: 700;">{{ server.clients || 0 }}</span>
        <span style="font-size: 28px; color: #64748b;">/{{ server.maxclients || 0 }}</span>
      </div>
      <p style="margin-top: 8px; color: #64748b; font-size: 16px;">{{ t.dashboard.playersOnline }}</p>
    </div>
    <div
      v-else
      class="card"
      style="flex: 2; min-width: 280px; display: flex; align-items: center; justify-content: center; flex-direction: column; gap: 16px;"
    >
      <span style="font-size: 48px;">🔴</span>
      <div style="font-size: 24px; font-weight: 600;">{{ t.dashboard.serverOffline }}</div>
      <p style="color: #64748b;">{{ t.dashboard.startToSee }}</p>
    </div>

    <div class="card" style="flex: 1; min-width: 240px; display: flex; flex-direction: column; justify-content: center;">
      <div style="display: flex; gap: 12px; flex-direction: column;">
        <button class="btn btn-primary" style="padding: 18px;" @click="start">
          {{ t.dashboard.startServer }}
        </button>
        <button class="btn btn-secondary" style="padding: 18px;" @click="stop">
          {{ t.dashboard.stopServer }}
        </button>
      </div>
      <p style="margin-top: 20px; font-size: 13px; color: #94a3b8; text-align: center;">
        {{ t.dashboard.manageHint }}
      </p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  server: {
    type: Object,
    required: true
  },
  t: {
    type: Object,
    required: true
  },
  start: {
    type: Function,
    required: true
  },
  stop: {
    type: Function,
    required: true
  }
})
</script>
