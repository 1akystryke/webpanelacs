import { ref } from 'vue'

export function useToasts(t) {
  const toasts = ref([])
  const toastId = ref(0)

  const removeToast = (id) => {
    const index = toasts.value.findIndex((toast) => toast.id === id)
    if (index > -1) {
      setTimeout(() => {
        toasts.value = toasts.value.filter((toast) => toast.id !== id)
      }, 300)
    }
  }

  const showToast = (type, title, message, duration = 4000) => {
    const icons = {
      success: '✅',
      error: '❌',
      warning: '⚠️',
      info: 'ℹ️'
    }
    const id = ++toastId.value
    toasts.value.push({
      id,
      type,
      icon: icons[type] || 'ℹ️',
      title: title || t.value?.common?.[type] || '',
      message
    })
    setTimeout(() => removeToast(id), duration)
  }

  const success = (message, title = null) => showToast('success', title || t.value.common.success, message)
  const error = (message, title = null) => showToast('error', title || t.value.common.error, message)
  const warning = (message, title = null) => showToast('warning', title || t.value.common.warning, message)
  const info = (message, title = null) => showToast('info', title || t.value.common.info, message)

  return {
    toasts,
    showToast,
    removeToast,
    success,
    error,
    warning,
    info
  }
}
