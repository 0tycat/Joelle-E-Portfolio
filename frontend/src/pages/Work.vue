<template>
  <section>
    <h2>Work Experience</h2>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-for="w in work" :key="w.id" class="card">
        <strong>{{ w.company_name }}</strong>
        <div>{{ w.role }}</div>
        <div>{{ w.start_date }} - {{ w.end_date || 'Present' }}</div>
        <p>{{ w.description }}</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { apiGet } from '../lib/api.js'

const work = ref([])
const loading = ref(true)

onMounted(async () => {
  try{
    work.value = await apiGet('/api/work')
  } finally {
    loading.value = false
  }
})
</script>
