<template>
  <div class="app">
    <header class="app-header">
      <button class="hamburger-header" @click="sidebarOpen = !sidebarOpen" aria-label="Toggle sidebar">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </header>
    <button class="floating-theme-toggle" @click="isDark = !isDark" title="Toggle dark/light mode">
      <i :class="isDark ? 'fas fa-sun' : 'fas fa-moon'"></i>
      {{ isDark ? 'Light' : 'Dark' }}
    </button>
    <div class="app-main">
      <Sidebar />
      <main class="content">
        <router-view />
      </main>
    </div>
    <div v-if="sidebarOpen && isMobile" class="sidebar-overlay" @click="sidebarOpen = false"></div>

    <!-- Session Timeout Warning Modal -->
    <div v-if="showSessionWarning" class="session-modal-overlay">
      <div class="session-modal">
        <div class="session-modal-header">
          <i class="fas fa-exclamation-triangle"></i>
          Session Expiring
        </div>
        <div class="session-modal-content">
          Your session will expire in 5 minutes due to inactivity. Click below to stay logged in.
        </div>
        <div class="session-modal-actions">
          <button class="btn" @click="handleStayLoggedIn">Stay Logged In</button>
          <button class="btn secondary" @click="handleLogoutNow">Logout Now</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, provide, computed, onMounted, onBeforeUnmount } from 'vue'
import { useTheme } from './lib/theme.js'
import { logout, initializeAuth } from './lib/auth.js'
import { useSessionTimeout } from './lib/sessionTimeout.js'
import Sidebar from './components/Sidebar.vue'
import '@fortawesome/fontawesome-free/css/all.min.css'

const { isDark } = useTheme()
const sidebarOpen = ref(false)
const isMobile = ref(false)
const showSessionWarning = ref(false)
const isInitializing = ref(true)

// Use session timeout composable
useSessionTimeout()

// Provide sidebar state to Sidebar component
provide('sidebarOpen', sidebarOpen)

// Check if mobile on mount and when window resizes
const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768
}

// Handle session warning events
const handleSessionWarning = (event) => {
  showSessionWarning.value = true
}

const handleSessionExpired = (event) => {
  showSessionWarning.value = false
  // User will be logged out automatically by the composable
}

const handleStayLoggedIn = () => {
  showSessionWarning.value = false
  // Activity tracking will automatically reset the timer
}

const handleLogoutNow = () => {
  showSessionWarning.value = false
  logout()
}

onMounted(async () => {
  // Initialize auth on app startup - validate tokens and potentially refresh them
  await initializeAuth()
  isInitializing.value = false
  
  checkMobile()
  window.addEventListener('resize', checkMobile)
  window.addEventListener('session:warning', handleSessionWarning)
  window.addEventListener('session:expired', handleSessionExpired)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', checkMobile)
  window.removeEventListener('session:warning', handleSessionWarning)
  window.removeEventListener('session:expired', handleSessionExpired)
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

.session-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.session-modal {
  background: var(--bg-secondary, #1e1e2e);
  border: 1px solid var(--border-color, #3a3a4a);
  border-radius: 8px;
  padding: 24px;
  max-width: 400px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
}

.session-modal-header {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 18px;
  font-weight: bold;
  color: #ff9800;
  margin-bottom: 16px;
}

.session-modal-header i {
  font-size: 24px;
}

.session-modal-content {
  color: var(--text-secondary, #b0b0c0);
  margin-bottom: 24px;
  line-height: 1.5;
}

.session-modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.session-modal-actions .btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.session-modal-actions .btn {
  background: #4CAF50;
  color: white;
}

.session-modal-actions .btn:hover {
  background: #45a049;
}

.session-modal-actions .btn.secondary {
  background: #757575;
  color: white;
}

.session-modal-actions .btn.secondary:hover {
  background: #616161;
}
</style>
