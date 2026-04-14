<template>
  <v-navigation-drawer width="260" class="sidebar" permanent>
    <div class="logo">AC Control</div>

    <div
      v-for="item in items"
      :key="item.key"
      class="nav-item"
      :class="{ active: tab === item.key }"
      @click="selectTab(item.key)"
    >
      {{ item.label }}
    </div>

    <div class="sidebar-footer">
      Assetto Corsa Dedicated<br />
      <span>v1.92 • Production Build</span>
    </div>
  </v-navigation-drawer>
</template>

<script setup>
const props = defineProps({
  tab: {
    type: String,
    required: true
  },
  items: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['update:tab'])

const selectTab = (key) => {
  emit('update:tab', key)
}
</script>

<style scoped>
.sidebar-footer {
  margin-top: auto;
  padding-top: 40px;
  border-top: 1px solid #334155;
  font-size: 13px;
  color: #64748b;
}

.sidebar-footer span {
  color: #94a3b8;
}
</style>
