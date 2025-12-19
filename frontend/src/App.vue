<template>
  <div class="app">
    <header class="app-header">
      <button class="hamburger-header" @click="sidebarOpen = !sidebarOpen" aria-label="Toggle sidebar">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </header>
    <button class="floating-theme-toggle" @click="isDark = !isDark">
      {{ isDark ? '☀️ Light' : '🌙 Dark' }}
    </button>
    <div class="app-main">
      <Sidebar />
      <main class="content">
        <router-view />
      </main>
    </div>
    <div v-if="sidebarOpen && isMobile" class="sidebar-overlay" @click="sidebarOpen = false"></div>
  </div>
</template>

<script setup>
import { ref, provide, computed, onMounted, onBeforeUnmount } from 'vue'
import { useTheme } from './lib/theme.js'
import Sidebar from './components/Sidebar.vue'

const { isDark } = useTheme()
const sidebarOpen = ref(false)
const isMobile = ref(false)

// Provide sidebar state to Sidebar component
provide('sidebarOpen', sidebarOpen)

// Check if mobile on mount and when window resizes
const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', checkMobile)
})
</script>

<style scoped>
.sidebar-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 998;
  top: 60px;
}
</style>
