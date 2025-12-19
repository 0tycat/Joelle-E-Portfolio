<template>
  <section>
    <h2>Work Experience</h2>
    <div v-if="isAuthed" class="card" style="margin-bottom:12px">
      <h3>Add Work</h3>
      <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap">
        <input class="input" v-model="newItem.company_name" placeholder="Company" />
        <input class="input" v-model="newItem.role" placeholder="Role" />
        <input class="input" v-model="newItem.start_date" placeholder="Start (YYYY-MM-DD)" />
        <input class="input" v-model="newItem.end_date" placeholder="End (YYYY-MM-DD)" />
        <input class="input" v-model="newItem.description" placeholder="Description" />
        <button class="btn" @click="addWork">Add</button>
      </div>
      <p v-if="error" style="color:#fca5a5">{{ error }}</p>
    </div>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-for="w in work" :key="w.id" class="card">
        <strong>{{ w.company_name }}</strong>
        <div>{{ w.role }}</div>
        <div>{{ w.start_date }} - {{ w.end_date || 'Present' }}</div>
        <p>{{ w.description }}</p>
        <div v-if="isAuthed" style="margin-top:8px; display:flex; gap:8px">
          <button class="btn secondary" @click="startEdit(w)">Edit</button>
          <button class="btn danger" @click="removeWork(w)">Delete</button>
        </div>
        <div v-if="isAuthed && editingId===w.id" style="margin-top:8px; display:flex; gap:8px; flex-wrap:wrap">
          <input class="input" v-model="editItem.company_name" placeholder="Company" />
          <input class="input" v-model="editItem.role" placeholder="Role" />
          <input class="input" v-model="editItem.start_date" placeholder="Start (YYYY-MM-DD)" />
          <input class="input" v-model="editItem.end_date" placeholder="End (YYYY-MM-DD)" />
          <input class="input" v-model="editItem.description" placeholder="Description" />
          <button class="btn" @click="saveEdit(w)">Save</button>
          <button class="btn secondary" @click="cancelEdit">Cancel</button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { apiGet, postWork, deleteWork, putWork } from '../lib/api.js'
import { isAuthenticated } from '../lib/auth.js'

const work = ref([])
const loading = ref(true)
const error = ref('')
const isAuthed = computed(() => isAuthenticated())
const newItem = ref({ company_name:'', role:'', start_date:'', end_date:'', description:'' })
const editingId = ref(null)
const editItem = ref({ company_name:'', role:'', start_date:'', end_date:'', description:'' })

async function refresh(){
  try{
    work.value = await apiGet('/api/work')
  } finally {
    loading.value = false
  }
}
onMounted(refresh)

async function addWork(){
  error.value = ''
  try{
    await postWork(newItem.value)
    newItem.value = { company_name:'', role:'', start_date:'', end_date:'', description:'' }
    await refresh()
  }catch(e){ error.value = 'Add failed' }
}

function startEdit(w){
  editingId.value = w.id
  editItem.value = { company_name:w.company_name, role:w.role, start_date:w.start_date, end_date:w.end_date, description:w.description }
}
function cancelEdit(){ editingId.value = null }
async function saveEdit(w){
  error.value = ''
  try{
    await putWork(w.id, editItem.value)
    editingId.value = null
    await refresh()
  }catch(e){ error.value = 'Update failed' }
}

async function removeWork(w){
  try{
    await deleteWork(w.id)
    await refresh()
  }catch(e){ error.value = 'Delete failed' }
}
</script>
