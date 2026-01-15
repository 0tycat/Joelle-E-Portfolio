<template>
  <nav class="top-navbar">
    <div class="navbar-container">
      <!-- Logo/Brand -->
      <div class="navbar-brand">
        <RouterLink to="/" class="brand-text">
          <div class="brand-name">JOELLE LOW</div>
          <div class="brand-tagline">LEARNING TO ADAPT, STRATEGISING TO GROW</div>
        </RouterLink>
      </div>

      <!-- Menu Toggle for Mobile -->
      <button 
        class="navbar-toggle" 
        @click="isOpen = !isOpen"
        aria-label="Toggle menu"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>

      <!-- Navigation Links -->
      <ul class="navbar-menu" :class="{ active: isOpen }">
        <!-- E-Portfolio -->
        <li class="nav-item">
          <RouterLink to="/portfolio" @click="closeMenu" class="nav-link">
            E-Portfolio
          </RouterLink>
        </li>

        <!-- Resume Dropdown -->
        <li class="nav-item dropdown">
          <button class="nav-link dropdown-toggle" @click="toggleResume">
            RESUME
            <i class="fas fa-chevron-down"></i>
          </button>
          <ul class="dropdown-menu" v-show="resumeOpen">
            <li><RouterLink to="/education" @click="closeMenu" class="dropdown-link">Education</RouterLink></li>
            <li><RouterLink to="/skills" @click="closeMenu" class="dropdown-link">Skills</RouterLink></li>
            <li><RouterLink to="/experience" @click="closeMenu" class="dropdown-link">Work Experience</RouterLink></li>
          </ul>
        </li>

        <!-- Projects -->
        <li class="nav-item">
          <RouterLink to="/projects" @click="closeMenu" class="nav-link">
            Projects
          </RouterLink>
        </li>

        <!-- Interests -->
        <li class="nav-item">
          <RouterLink to="/interests" @click="closeMenu" class="nav-link">
            INTERESTS
          </RouterLink>
        </li>

        <!-- Auth Section -->
        <li class="nav-item auth-item">
          <button v-if="!isAuthed" class="btn btn-nav btn-owner-login" @click="goLogin">Owner's Login</button>
          <button v-else class="btn btn-nav btn-logout" @click="logout">Logout</button>
        </li>
      </ul>

      <!-- Theme Toggle (always visible) -->
      <button class="theme-toggle-navbar" @click="toggleTheme" title="Toggle dark/light mode">
        <i :class="isDark ? 'fas fa-sun' : 'fas fa-moon'"></i>
      </button>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { isAuthed, logout as doLogout } from '../lib/auth.js'
import { useTheme } from '../lib/theme.js'

const router = useRouter()
const isOpen = ref(false)
const resumeOpen = ref(false)
const { isDark, toggleTheme: doToggleTheme } = useTheme()

function closeMenu() {
  isOpen.value = false
  resumeOpen.value = false
}

function toggleResume(e) {
  e.preventDefault()
  resumeOpen.value = !resumeOpen.value
}

function toggleTheme() {
  doToggleTheme()
}

function goLogin(){
  router.push('/login')
  closeMenu()
}

async function logout(){
  await doLogout()
  router.push('/login')
  closeMenu()
}
</script>

<style scoped>
.top-navbar {
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  z-index: 999;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.navbar-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
}

.navbar-brand {
  display: flex;
  align-items: center;
  font-size: 18px;
  font-weight: 700;
  flex-shrink: 0;
}

.brand-text {
  color: var(--text-primary);
  text-decoration: none;
  letter-spacing: 1px;
  transition: color 0.3s ease;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.brand-text:hover {
  color: #3b82f6;
}

.brand-name {
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 1px;
}

.brand-tagline {
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.5px;
  opacity: 0.9;
}

.navbar-toggle {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 8px;
}

.navbar-toggle span {
  width: 24px;
  height: 2px;
  background: var(--text-primary);
  border-radius: 2px;
  transition: all 0.3s ease;
}

.navbar-menu {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 0;
  align-items: center;
}

.nav-item {
  position: relative;
  height: 100%;
  display: flex;
  align-items: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--text-secondary);
  text-decoration: none;
  padding: 8px 16px;
  transition: all 0.3s ease;
  font-size: 14px;
  font-weight: 500;
  background: none;
  border: none;
  cursor: pointer;
  letter-spacing: 0.5px;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: var(--text-primary);
  background: rgba(59, 130, 246, 0.1);
  border-radius: 4px;
}

.dropdown {
  position: relative;
}

.dropdown-toggle {
  position: relative;
}

.dropdown-toggle i {
  font-size: 10px;
  transition: transform 0.3s ease;
}

.dropdown:hover .dropdown-toggle i,
.dropdown-toggle.active i {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  min-width: 180px;
  list-style: none;
  margin: 8px 0 0 0;
  padding: 8px 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  z-index: 1000;
}

.dropdown-menu li {
  margin: 0;
}

.dropdown-link {
  display: block;
  color: var(--text-secondary);
  text-decoration: none;
  padding: 10px 16px;
  transition: all 0.2s ease;
  font-size: 13px;
}

.dropdown-link:hover {
  color: var(--text-primary);
  background: rgba(59, 130, 246, 0.15);
  padding-left: 24px;
}

.auth-item {
  margin-left: auto;
  padding-right: 12px;
}

.btn-nav {
  padding: 8px 16px;
  font-size: 13px;
  border-radius: 6px;
  font-weight: 600;
}

.btn-owner-login {
  background: #ff6b35;
  color: white;
  border: none;
}

.btn-owner-login:hover {
  background: #ff5520;
  transform: translateY(-2px);
}

.btn-logout {
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.btn-logout:hover {
  background: rgba(59, 130, 246, 0.1);
  color: var(--text-primary);
}

.btn-nav:not(.secondary):not(.btn-owner-login):not(.btn-logout) {
  background: #3b82f6;
  color: white;
}

.btn-nav:not(.secondary):not(.btn-owner-login):not(.btn-logout):hover {
  background: #2563eb;
}

.theme-toggle-navbar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: none;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  color: var(--text-primary);
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.theme-toggle-navbar:hover {
  background: rgba(59, 130, 246, 0.1);
  border-color: #3b82f6;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .navbar-toggle {
    display: flex;
    order: 2;
  }

  .navbar-menu {
    position: absolute;
    top: 70px;
    left: 0;
    right: 0;
    flex-direction: column;
    gap: 0;
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border-color);
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease;
    padding: 0;
  }

  .navbar-menu.active {
    max-height: 500px;
    padding: 12px 0;
  }

  .nav-item {
    width: 100%;
    height: auto;
    padding: 0;
    border-bottom: 1px solid var(--border-color);
  }

  .nav-item:last-child {
    border-bottom: none;
  }

  .nav-link {
    width: 100%;
    padding: 12px 20px;
    border-radius: 0;
    justify-content: space-between;
  }

  .nav-link:hover,
  .nav-link.router-link-active {
    background: rgba(59, 130, 246, 0.1);
  }

  .auth-item {
    margin-left: 0;
    padding-right: 0;
    width: 100%;
  }

  .btn-nav {
    width: calc(100% - 40px);
    margin: 8px 20px;
  }

  .dropdown-menu {
    position: static;
    border: none;
    background: var(--bg-tertiary);
    box-shadow: none;
    min-width: 100%;
    margin: 0;
    padding: 0;
  }

  .dropdown-link {
    padding-left: 40px;
  }

  .theme-toggle-navbar {
    order: 3;
  }

  .navbar-brand {
    order: 1;
  }
}
</style>
