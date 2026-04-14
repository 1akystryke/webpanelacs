<template>
  <div class="card">
    <div class="card-title"><span>🖥️</span> {{ t.session.serverCard }}</div>
    <div class="label">{{ t.session.serverName }}</div>
    <input
      v-model="session.name"
      type="text"
      class="input"
      style="margin-bottom: 16px;"
      :placeholder="t.session.serverNamePlaceholder"
    />
    <div class="label">{{ t.session.password }}</div>
    <input
      v-model="session.password"
      type="text"
      class="input"
      style="margin-bottom: 16px;"
      :placeholder="t.session.passwordPlaceholder"
    />
    <div class="label">{{ t.session.adminPassword }}</div>
    <input
      v-model="session.adminPassword"
      type="text"
      class="input"
      style="margin-bottom: 20px;"
      :placeholder="t.session.adminPasswordPlaceholder"
    />
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;">
      <div>
        <div class="label">UDP_PORT</div>
        <input v-model.number="session.udpPort" type="number" class="input" />
      </div>
      <div>
        <div class="label">TCP_PORT</div>
        <input v-model.number="session.tcpPort" type="number" class="input" />
      </div>
      <div>
        <div class="label">HTTP_PORT</div>
        <input v-model.number="session.httpPort" type="number" class="input" />
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  session: {
    type: Object,
    required: true
  },
  t: {
    type: Object,
    required: true
  }
})
</script>
