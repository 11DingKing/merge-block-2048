<template>
  <div class="app">
    <Game2048 />
    <ToastContainer />
  </div>
</template>

<script setup>
import Game2048 from './components/Game2048.vue'
import ToastContainer from './components/ToastContainer.vue'
</script>

<style scoped>
.app {
  width: 100%;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
