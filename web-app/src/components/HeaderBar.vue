<template>
  <div class="header-bar">
    <div class="header-title">{{ title }}</div>

    <div class="header-actions">
      <span :class="['status', serverStatus]">
        {{ serverStatus === 'online' ? t.common.online : t.common.offline }}
      </span>

      <button class="lang-btn" @click="toggleLanguage">
        {{ locale === 'ru' ? '🇬🇧 EN' : '🇷🇺 RU' }}
      </button>
      <button class="logout-btn" @click="logout">{{ t.common.logout }}</button>

      <div class="admin-block">
        <div class="admin-text">
          <div class="admin-name">{{ t.common.admin }}</div>
          <div class="admin-email">admin@acserver.pro</div>
        </div>
        <div class="admin-avatar">A</div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  t: {
    type: Object,
    required: true
  },
  serverStatus: {
    type: String,
    required: true
  },
  locale: {
    type: String,
    required: true
  },
  toggleLanguage: {
    type: Function,
    required: true
  },
  logout: {
    type: Function,
    required: true
  }
})
</script>

<style scoped>
.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.admin-block {
  display: flex;
  align-items: center;
  gap: 12px;
}

.admin-text {
  text-align: right;
}

.admin-name {
  font-weight: 600;
  font-size: 15px;
}

.admin-email {
  font-size: 13px;
  color: #64748b;
}

.admin-avatar {
  width: 42px;
  height: 42px;
  background: linear-gradient(135deg, #ff2a2a, #ff6a6a);
  border-radius: 50%;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 20px;
}

@media (max-width: 900px) {
  .header-actions {
    flex-wrap: wrap;
    justify-content: flex-end;
  }
}
</style>
