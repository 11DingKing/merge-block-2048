import { ref } from 'vue'

// 全局toast状态
const toasts = ref([])

export function useToast() {
  const show = (message, type = 'info', duration = 3000) => {
    const id = Date.now() + Math.random()
    const toast = {
      id,
      message,
      type,
      duration
    }
    
    toasts.value.push(toast)
    
    // 自动移除
    if (duration > 0) {
      setTimeout(() => {
        remove(id)
      }, duration)
    }
    
    return id
  }
  
  const remove = (id) => {
    const index = toasts.value.findIndex(t => t.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }
  
  const success = (message, duration = 3000) => show(message, 'success', duration)
  const error = (message, duration = 3000) => show(message, 'error', duration)
  const info = (message, duration = 3000) => show(message, 'info', duration)
  const warning = (message, duration = 3000) => show(message, 'warning', duration)
  
  return {
    toasts,
    show,
    remove,
    success,
    error,
    info,
    warning
  }
}
