<template>
  <aside class="sidebar" :class="{ open: isOpen }">
    <nav class="nav">
      <RouterLink to="/skills" @click="closeOnMobile">Skills</RouterLink>
      <RouterLink to="/experience" @click="closeOnMobile">Work Experience</RouterLink>
      <RouterLink to="/education" @click="closeOnMobile">Education</RouterLink>
      <RouterLink to="/other-information" @click="closeOnMobile">Other Information</RouterLink>
      <div class="auth-section">
        <button v-if="!isAuthed" class="btn" @click="goLogin">Login</button>
        <button v-else class="btn secondary" @click="logout">Logout</button>
      </div>
    </nav>
  </aside>
</template>

<script setup>
import { inject } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { isAuthed, logout as doLogout } from '../lib/auth.js'

const router = useRouter()
const isOpen = inject('sidebarOpen')

function closeOnMobile() {
  // Close sidebar on mobile after navigation
  if (window.innerWidth <= 768) {
    isOpen.value = false
  }
}

function goLogin(){
  router.push('/login')
}

async function logout(){
  await doLogout()
  router.push('/login')
}
</script>

<style scoped>
.sidebar {
  width: 260px;
  background: var(--bg-secondary);
  padding: 16px;
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease;
}

.nav {
  display: flex;
  flex-direction: column;
}

.auth-section {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--border-color);
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 60px;
    width: 260px;
    max-height: calc(100% - 60px);
    z-index: 999;
    transform: translateX(-100%);
    overflow-y: auto;
  }

  .sidebar.open {
    transform: translateX(0);
  }
}
</style>
