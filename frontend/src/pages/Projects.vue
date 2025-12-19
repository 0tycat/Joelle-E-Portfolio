<template>
  <section>
    <h2>Other Information / Projects</h2>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-for="p in projects" :key="p.id" class="card">
        <strong>{{ p.project_name }}</strong>
        <p>{{ p.description }}</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { apiGet } from '../lib/api.js'

const projects = ref([])
const loading = ref(true)

onMounted(async () => {
  try{
    projects.value = await apiGet('/api/projects')
  } finally {
    loading.value = false
  }
})
</script>
