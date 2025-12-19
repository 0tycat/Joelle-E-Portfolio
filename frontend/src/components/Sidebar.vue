<template>
  <aside class="sidebar">
    <h1>Joelle Portfolio</h1>
    <div style="margin-bottom:12px">
      <button v-if="!isAuthed" class="btn" @click="goLogin">Login</button>
      <button v-else class="btn secondary" @click="logout">Logout</button>
    </div>
    <nav class="nav">
      <RouterLink to="/skills">Skills</RouterLink>
      <RouterLink to="/experience">Work Experience</RouterLink>
      <RouterLink to="/education">Education</RouterLink>
      <RouterLink to="/other-information">Other Information</RouterLink>
    </nav>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { isAuthenticated, logout as doLogout } from '../lib/auth.js'

const router = useRouter()
const isAuthed = computed(() => isAuthenticated())

function goLogin(){
  router.push('/login')
}
async function logout(){
  await doLogout()
  router.push('/login')
}
</script>
