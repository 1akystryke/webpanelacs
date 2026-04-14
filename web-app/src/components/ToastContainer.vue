<template>
  <div class="toast-container">
    <div
      v-for="toast in toasts"
      :key="toast.id"
      :class="['toast', toast.type]"
      @click="removeToast(toast.id)"
    >
      <div class="toast-icon">{{ toast.icon }}</div>
      <div class="toast-content">
        <div class="toast-title">{{ toast.title }}</div>
        <div class="toast-message">{{ toast.message }}</div>
      </div>
      <button class="toast-close" @click.stop="removeToast(toast.id)">×</button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  toasts: {
    type: Array,
    required: true
  },
  removeToast: {
    type: Function,
    required: true
  }
})
</script>
