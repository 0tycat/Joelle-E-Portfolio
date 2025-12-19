<template>
  <section>
    <h2>Skills</h2>
    <div v-if="isAuthed" style="margin-bottom:12px">
      <button class="btn" @click="showAdd=true">Add Skill</button>
    </div>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-for="s in skills" :key="s.id" class="card">
        <strong>{{ s.skill_name }}</strong>
        <div>Proficiency: {{ s.proficiency }}</div>
        <div v-if="isAuthed" style="margin-top:8px; display:flex; gap:8px">
          <button class="btn secondary" @click="startEdit(s)">Edit</button>
          <button class="btn danger" @click="askRemoveSkill(s)">Delete</button>
        </div>
      </div>
    </div>

    <!-- Add Modal -->
    <Modal :open="showAdd" title="Add Skill" @close="closeAdd">
      <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap">
        <input class="input" v-model="newSkill.skill_name" placeholder="Skill name" />
        <input class="input" v-model="newSkill.proficiency" placeholder="Proficiency (1-3)" />
        <button class="btn" @click="addSkill">Save</button>
        <button class="btn secondary" @click="closeAdd">Cancel</button>
      </div>
      <p v-if="error" style="color:#fca5a5">{{ error }}</p>
    </Modal>

    <!-- Edit Modal -->
    <Modal :open="showEdit" title="Edit Skill" @close="closeEdit">
      <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap">
        <input class="input" v-model="editSkill.skill_name" />
        <input class="input" v-model="editSkill.proficiency" />
        <button class="btn" @click="performEdit">Save</button>
        <button class="btn secondary" @click="closeEdit">Cancel</button>
      </div>
      <p v-if="error" style="color:#fca5a5">{{ error }}</p>
    </Modal>

    <!-- Confirm Delete Modal -->
    <ConfirmModal
      :open="showConfirm"
      title="Delete Skill"
      :message="confirmMessage"
      @confirm="performDelete"
      @close="closeConfirm"
    />
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { apiGet, postSkill, putSkill, deleteSkill } from '../lib/api.js'
import { isAuthed } from '../lib/auth.js'
import Modal from '../components/Modal.vue'
import ConfirmModal from '../components/ConfirmModal.vue'

const skills = ref([])
const loading = ref(true)
const error = ref('')
const newSkill = ref({ skill_name:'', proficiency:'' })
const editingId = ref(null)
const editSkill = ref({ skill_name:'', proficiency:'' })
const showAdd = ref(false)
const showEdit = ref(false)
let editTargetId = null
const showConfirm = ref(false)
let deleteTargetId = null
const deleteItemLabel = ref('')
const confirmMessage = computed(() => `Delete "${deleteItemLabel.value}"? This cannot be undone.`)

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
    showAdd.value = false
  }catch(e){ error.value = 'Add failed' }
}

function startEdit(s){
  editSkill.value = { skill_name: s.skill_name, proficiency: s.proficiency }
  editTargetId = s.id
  showEdit.value = true
}
function closeAdd(){ showAdd.value = false }
function closeEdit(){ showEdit.value = false; editTargetId = null }
async function performEdit(){
  error.value = ''
  try{
    await putSkill(editTargetId, editSkill.value)
    closeEdit()
    await refresh()
  }catch(e){ error.value = 'Update failed' }
}
async function removeSkill(s){
  // replaced by askRemoveSkill
}

function askRemoveSkill(s){
  deleteTargetId = s.id
  deleteItemLabel.value = s.skill_name
  showConfirm.value = true
}
function closeConfirm(){
  showConfirm.value = false
  deleteTargetId = null
  deleteItemLabel.value = ''
}
async function performDelete(){
  error.value = ''
  try{
    await deleteSkill(deleteTargetId)
    closeConfirm()
    await refresh()
  }catch(e){ error.value = 'Delete failed' }
}
</script>
