<template>
  <section>
    <h2>Skills</h2>
    <!-- Admin controls: visible only when logged in -->
    <div v-if="isAuthed" class="card" style="margin-bottom:12px">
      <h3>Add Skill</h3>
      <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap">
        <input class="input" v-model="newSkill.skill_name" placeholder="Skill name" />
        <input class="input" v-model="newSkill.proficiency" placeholder="Proficiency (1-3)" />
        <button class="btn" @click="addSkill">Add</button>
      </div>
      <p v-if="error" style="color:#fca5a5">{{ error }}</p>
    </div>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-for="s in skills" :key="s.id" class="card">
        <strong>{{ s.skill_name }}</strong>
        <div>Proficiency: {{ s.proficiency }}</div>
        <div v-if="isAuthed" style="margin-top:8px; display:flex; gap:8px">
          <button class="btn secondary" @click="startEdit(s)">Edit</button>
          <button class="btn danger" @click="removeSkill(s)">Delete</button>
        </div>
        <div v-if="isAuthed && editingId===s.id" style="margin-top:8px; display:flex; gap:8px; flex-wrap:wrap">
          <input class="input" v-model="editSkill.skill_name" />
          <input class="input" v-model="editSkill.proficiency" />
          <button class="btn" @click="saveEdit(s)">Save</button>
          <button class="btn secondary" @click="cancelEdit">Cancel</button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { apiGet, postSkill, putSkill, deleteSkill } from '../lib/api.js'
import { isAuthenticated } from '../lib/auth.js'

const skills = ref([])
const loading = ref(true)
const error = ref('')
const isAuthed = computed(() => isAuthenticated())
const newSkill = ref({ skill_name:'', proficiency:'' })
const editingId = ref(null)
const editSkill = ref({ skill_name:'', proficiency:'' })

async function refresh(){
  try{
    skills.value = await apiGet('/api/skills')
  } finally {
    loading.value = false
  }
}
onMounted(refresh)

async function addSkill(){
  error.value = ''
  try{
    if(!newSkill.value.skill_name || !newSkill.value.proficiency){
      error.value = 'Provide skill name and proficiency'
      return
    }
    await postSkill(newSkill.value)
    newSkill.value = { skill_name:'', proficiency:'' }
    await refresh()
  }catch(e){ error.value = 'Add failed' }
}

function startEdit(s){
  editingId.value = s.id
  editSkill.value = { skill_name: s.skill_name, proficiency: s.proficiency }
}
function cancelEdit(){ editingId.value = null }
async function saveEdit(s){
  error.value = ''
  try{
    await putSkill(s.id, editSkill.value)
    editingId.value = null
    await refresh()
  }catch(e){ error.value = 'Update failed' }
}
async function removeSkill(s){
  try{
    await deleteSkill(s.id)
    await refresh()
  }catch(e){ error.value = 'Delete failed' }
}
</script>
