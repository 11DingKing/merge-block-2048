<template>
  <div class="toast-container">
    <TransitionGroup name="toast-list" tag="div">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="toast"
        :class="toast.type"
      >
        <div class="toast-icon">
          <span v-if="toast.type === 'success'">✓</span>
          <span v-else-if="toast.type === 'error'">✕</span>
          <span v-else-if="toast.type === 'info'">ℹ</span>
          <span v-else>!</span>
        </div>
        <div class="toast-content">
          <div class="toast-message">{{ toast.message }}</div>
        </div>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { useToast } from '../composables/useToast'

const { toasts } = useToast()
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 0;
  right: 0;
  z-index: 10000;
  pointer-events: none;
  padding: 20px;
}

.toast {
  position: relative;
  min-width: 300px;
  max-width: 500px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  padding: 16px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  pointer-events: auto;
  animation: slideInRight 0.3s ease-out;
}

.toast.success {
  border-left: 4px solid #10b981;
}

.toast.error {
  border-left: 4px solid #ef4444;
}

.toast.info {
  border-left: 4px solid #3b82f6;
}

.toast.warning {
  border-left: 4px solid #f59e0b;
}

.toast-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 14px;
  flex-shrink: 0;
}

.toast.success .toast-icon {
  background: #10b981;
  color: #fff;
}

.toast.error .toast-icon {
  background: #ef4444;
  color: #fff;
}

.toast.info .toast-icon {
  background: #3b82f6;
  color: #fff;
}

.toast.warning .toast-icon {
  background: #f59e0b;
  color: #fff;
}

.toast-content {
  flex: 1;
}

.toast-message {
  color: #1f2937;
  font-size: 14px;
  line-height: 1.5;
  font-weight: 500;
}

.toast-list-move,
.toast-list-enter-active,
.toast-list-leave-active {
  transition: all 0.3s ease;
}

.toast-list-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-list-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.toast-list-leave-active {
  position: absolute;
  right: 20px;
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@media screen and (max-width: 520px) {
  .toast-container {
    padding: 10px;
  }
  
  .toast {
    min-width: auto;
    max-width: none;
    width: calc(100vw - 20px);
  }
}
</style>
