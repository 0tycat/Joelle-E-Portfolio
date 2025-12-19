<template>
  <section>
    <h2>Education</h2>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-for="e in education" :key="e.id" class="card">
        <strong>{{ e.institute_name }}</strong>
        <div>{{ e.certification }}</div>
        <div>{{ e.start_date }} - {{ e.finish_date }}</div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { apiGet } from '../lib/api.js'

const education = ref([])
const loading = ref(true)

onMounted(async () => {
  try{
    education.value = await apiGet('/api/education')
  } finally {
    loading.value = false
  }
})
</script>
