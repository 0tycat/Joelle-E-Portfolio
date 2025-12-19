<template>
  <section>
    <h2>Other Information / Projects</h2>
    <div v-if="isAuthed" class="card" style="margin-bottom:12px">
      <h3>Add Project</h3>
      <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap">
        <input class="input" v-model="newItem.project_name" placeholder="Project name" />
        <input class="input" v-model="newItem.description" placeholder="Description" />
        <button class="btn" @click="addProject">Add</button>
      </div>
      <p v-if="error" style="color:#fca5a5">{{ error }}</p>
    </div>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-for="p in projects" :key="p.id" class="card">
        <strong>{{ p.project_name }}</strong>
        <p>{{ p.description }}</p>
        <div v-if="isAuthed" style="margin-top:8px; display:flex; gap:8px">
          <button class="btn secondary" @click="startEdit(p)">Edit</button>
          <button class="btn danger" @click="removeProject(p)">Delete</button>
        </div>
        <div v-if="isAuthed && editingId===p.id" style="margin-top:8px; display:flex; gap:8px; flex-wrap:wrap">
          <input class="input" v-model="editItem.project_name" placeholder="Project name" />
          <input class="input" v-model="editItem.description" placeholder="Description" />
          <button class="btn" @click="saveEdit(p)">Save</button>
          <button class="btn secondary" @click="cancelEdit">Cancel</button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { apiGet, postProject, deleteProject, putProject } from '../lib/api.js'
import { isAuthenticated } from '../lib/auth.js'

const projects = ref([])
const loading = ref(true)
const error = ref('')
const isAuthed = computed(() => isAuthenticated())
const newItem = ref({ project_name:'', description:'' })
const editingId = ref(null)
const editItem = ref({ project_name:'', description:'' })

async function refresh(){
  try{
    projects.value = await apiGet('/api/projects')
  } finally {
    loading.value = false
  }
}
onMounted(refresh)

async function addProject(){
  error.value = ''
  try{
    await postProject(newItem.value)
    newItem.value = { project_name:'', description:'' }
    await refresh()
  }catch(e){ error.value = 'Add failed' }
}

function startEdit(p){
  editingId.value = p.id
  editItem.value = { project_name:p.project_name, description:p.description }
}
function cancelEdit(){ editingId.value = null }
async function saveEdit(p){
  error.value = ''
  try{
    await putProject(p.id, editItem.value)
    editingId.value = null
    await refresh()
  }catch(err){ error.value = 'Update failed' }
}

async function removeProject(p){
  try{
    await deleteProject(p.id)
    await refresh()
  }catch(err){ error.value = 'Delete failed' }
}
</script>
