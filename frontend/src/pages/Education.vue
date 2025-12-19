<template>
  <section>
    <h2>Education</h2>
    <div v-if="isAuthed" class="card" style="margin-bottom:12px">
      <h3>Add Education</h3>
      <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap">
        <input class="input" v-model="newItem.institute_name" placeholder="Institute" />
        <input class="input" v-model="newItem.certification" placeholder="Certification" />
        <input class="input" v-model="newItem.start_date" placeholder="Start (YYYY-MM-DD)" />
        <input class="input" v-model="newItem.finish_date" placeholder="Finish (YYYY-MM-DD)" />
        <button class="btn" @click="addEducation">Add</button>
      </div>
      <p v-if="error" style="color:#fca5a5">{{ error }}</p>
    </div>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-for="e in education" :key="e.id" class="card">
        <strong>{{ e.institute_name }}</strong>
        <div>{{ e.certification }}</div>
        <div>{{ e.start_date }} - {{ e.finish_date }}</div>
        <div v-if="isAuthed" style="margin-top:8px; display:flex; gap:8px">
          <button class="btn secondary" @click="startEdit(e)">Edit</button>
          <button class="btn danger" @click="removeEducation(e)">Delete</button>
        </div>
        <div v-if="isAuthed && editingId===e.id" style="margin-top:8px; display:flex; gap:8px; flex-wrap:wrap">
          <input class="input" v-model="editItem.institute_name" placeholder="Institute" />
          <input class="input" v-model="editItem.certification" placeholder="Certification" />
          <input class="input" v-model="editItem.start_date" placeholder="Start (YYYY-MM-DD)" />
          <input class="input" v-model="editItem.finish_date" placeholder="Finish (YYYY-MM-DD)" />
          <button class="btn" @click="saveEdit(e)">Save</button>
          <button class="btn secondary" @click="cancelEdit">Cancel</button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { apiGet, postEducation, deleteEducation, putEducation } from '../lib/api.js'
import { isAuthenticated } from '../lib/auth.js'

const education = ref([])
const loading = ref(true)
const error = ref('')
const isAuthed = computed(() => isAuthenticated())
const newItem = ref({ institute_name:'', certification:'', start_date:'', finish_date:'' })
const editingId = ref(null)
const editItem = ref({ institute_name:'', certification:'', start_date:'', finish_date:'' })

async function refresh(){
  try{
    education.value = await apiGet('/api/education')
  } finally {
    loading.value = false
  }
}
onMounted(refresh)

async function addEducation(){
  error.value = ''
  try{
    await postEducation(newItem.value)
    newItem.value = { institute_name:'', certification:'', start_date:'', finish_date:'' }
    await refresh()
  }catch(e){ error.value = 'Add failed' }
}

function startEdit(e){
  editingId.value = e.id
  editItem.value = { institute_name:e.institute_name, certification:e.certification, start_date:e.start_date, finish_date:e.finish_date }
}
function cancelEdit(){ editingId.value = null }
async function saveEdit(e){
  error.value = ''
  try{
    await putEducation(e.id, editItem.value)
    editingId.value = null
    await refresh()
  }catch(err){ error.value = 'Update failed' }
}

async function removeEducation(e){
  try{
    await deleteEducation(e.id)
    await refresh()
  }catch(err){ error.value = 'Delete failed' }
}
</script>
