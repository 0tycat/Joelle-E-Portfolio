<template>
  <aside class="sidebar" :class="{ open: isOpen }">
    <nav class="nav">
      <!-- E-Portfolio -->
      <div class="nav-item">
        <RouterLink to="/portfolio" @click="closeOnMobile" class="nav-link">
          E-Portfolio
        </RouterLink>
      </div>

      <!-- Resume Section -->
      <div class="nav-section">
        <button 
          class="section-toggle" 
          @click="toggleResume"
          :class="{ active: resumeOpen }"
        >
          <span class="toggle-icon">▼</span>
          Resume
        </button>
        <div v-show="resumeOpen" class="section-items">
          <RouterLink to="/education" @click="closeOnMobile" class="nav-link">
            Education
          </RouterLink>
          <RouterLink to="/skills" @click="closeOnMobile" class="nav-link">
            Skills
          </RouterLink>
          <RouterLink to="/experience" @click="closeOnMobile" class="nav-link">
            Work Experience
          </RouterLink>
        </div>
      </div>

      <!-- Projects Section -->
      <div class="nav-section">
        <button 
          class="section-toggle" 
          @click="toggleProjects"
          :class="{ active: projectsOpen }"
        >
          <span class="toggle-icon">▼</span>
          Projects
        </button>
        <div v-show="projectsOpen" class="section-items">
          <RouterLink to="/community" @click="closeOnMobile" class="nav-link">
            Community Service
          </RouterLink>
          <!-- CCA to be added when data table is formed -->
        </div>
      </div>

      <!-- Interests Section -->
      <div class="nav-item">
        <RouterLink to="/interests" @click="closeOnMobile" class="nav-link">
          Interests
        </RouterLink>
      </div>

      <!-- Auth Section -->
      <div class="auth-section">
        <button v-if="!isAuthed" class="btn" @click="goLogin">Login</button>
        <button v-else class="btn secondary" @click="logout">Logout</button>
      </div>
    </nav>
  </aside>
</template>

<script setup>
import { inject, ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { isAuthed, logout as doLogout } from '../lib/auth.js'

const router = useRouter()
const isOpen = inject('sidebarOpen')
const resumeOpen = ref(true)
const projectsOpen = ref(true)

function toggleResume() {
  resumeOpen.value = !resumeOpen.value
}

function toggleProjects() {
  projectsOpen.value = !projectsOpen.value
}

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
  gap: 16px;
}

.nav-item {
  display: flex;
  flex-direction: column;
}

.nav-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.section-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  background: transparent;
  border: none;
  color: var(--text-primary);
  font-weight: 600;
  font-size: 12px;
  text-transform: uppercase;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.section-toggle:hover {
  background: var(--bg-hover);
  color: var(--btn-primary);
}

.section-toggle.active {
  color: var(--btn-primary);
}

.toggle-icon {
  display: inline-block;
  transition: transform 0.3s ease;
  font-size: 10px;
}

.section-toggle.active .toggle-icon {
  transform: rotate(-180deg);
}

.section-items {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding-left: 12px;
  border-left: 2px solid var(--border-color);
}

.nav-link {
  padding: 10px 12px;
  color: var(--text-primary);
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.2s ease;
  font-size: 14px;
}

.nav-link:hover {
  background: var(--bg-hover);
  color: var(--btn-primary);
}

.nav-link.router-link-active {
  background: var(--btn-primary);
  color: white;
  font-weight: 500;
}

.auth-section {
  margin-top: auto;
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
