<template>
  <section>
    <h2>Skills</h2>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-for="s in skills" :key="s.id" class="card">
        <strong>{{ s.skill_name }}</strong>
        <div>Proficiency: {{ s.proficiency }}</div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { apiGet } from '../lib/api.js'

const skills = ref([])
const loading = ref(true)

onMounted(async () => {
  try{
    skills.value = await apiGet('/api/skills')
  } finally {
    loading.value = false
  }
})
</script>
