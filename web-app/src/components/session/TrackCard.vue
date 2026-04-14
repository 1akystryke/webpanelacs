<template>
  <div class="card">
    <div class="card-title"><span>🏁</span> {{ t.session.trackCard }}</div>
    <div class="label">{{ t.session.track }}</div>
    <select v-model="session.track" class="input" style="margin-bottom: 20px;">
      <option v-for="track in tracks" :key="track.id" :value="track.id">
        {{ track.name || track.id }}
      </option>
    </select>
    <div v-if="session.trackVariants.length !== 0">
      <div class="label">{{ t.session.trackVariant }}</div>
      <select v-model="session.trackVariant" class="input">
        <option v-for="variant in session.trackVariants" :key="variant" :value="variant">
          {{ variant }}
        </option>
      </select>
    </div>
    <p style="margin-top: 20px; font-size: 13px; color: #94a3b8;">{{ t.session.trackHint }}</p>
  </div>
</template>

<script setup>
defineProps({
  session: {
    type: Object,
    required: true
  },
  tracks: {
    type: Array,
    required: true
  },
  t: {
    type: Object,
    required: true
  }
})
</script>
