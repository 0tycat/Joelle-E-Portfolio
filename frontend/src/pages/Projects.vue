<template>
  <section>
    <h2>Other Information / Projects</h2>
    <div v-if="isAuthed" style="margin-bottom:12px">
      <button class="btn" @click="showAdd=true">Add Project</button>
    </div>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-for="p in projects" :key="p.id" class="card">
        <strong>{{ p.project_name }}</strong>
        <p>{{ p.description }}</p>
        <div v-if="isAuthed" style="margin-top:8px; display:flex; gap:8px">
          <button class="btn secondary" @click="startEdit(p)">Edit</button>
          <button class="btn danger" @click="askRemoveProject(p)">Delete</button>
        </div>
      </div>
    </div>

    <!-- Add Modal -->
    <Modal :open="showAdd" title="Add Project" @close="closeAdd">
      <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap">
        <input class="input" v-model="newItem.project_name" placeholder="Project name" />
        <input class="input" v-model="newItem.description" placeholder="Description" />
        <button class="btn" @click="addProject">Save</button>
        <button class="btn secondary" @click="closeAdd">Cancel</button>
      </div>
      <p v-if="error" style="color:#fca5a5">{{ error }}</p>
    </Modal>

    <!-- Edit Modal -->
    <Modal :open="showEdit" title="Edit Project" @close="closeEdit">
      <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap">
        <input class="input" v-model="editItem.project_name" placeholder="Project name" />
        <input class="input" v-model="editItem.description" placeholder="Description" />
        <button class="btn" @click="performEdit">Save</button>
        <button class="btn secondary" @click="closeEdit">Cancel</button>
      </div>
      <p v-if="error" style="color:#fca5a5">{{ error }}</p>
    </Modal>

    <!-- Confirm Delete Modal -->
    <ConfirmModal
      :open="showConfirm"
      title="Delete Project"
      :message="confirmMessage"
      @confirm="performDelete"
      @close="closeConfirm"
    />
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { apiGet, postProject, deleteProject, putProject } from '../lib/api.js'
import { isAuthed as authIsAuthed } from '../lib/auth.js'
import Modal from '../components/Modal.vue'
import ConfirmModal from '../components/ConfirmModal.vue'

const projects = ref([])
const loading = ref(true)
const error = ref('')
const isAuthed = authIsAuthed
const newItem = ref({ project_name:'', description:'' })
const editItem = ref({ project_name:'', description:'' })
const showAdd = ref(false)
const showEdit = ref(false)
let editTargetId = null
const showConfirm = ref(false)
let deleteTargetId = null
const deleteItemLabel = ref('')
const confirmMessage = computed(() => `Delete "${deleteItemLabel.value}"? This cannot be undone.`)

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
    showAdd.value = false
  }catch(e){ error.value = 'Add failed' }
}

function startEdit(p){
  editItem.value = { project_name:p.project_name, description:p.description }
  editTargetId = p.id
  showEdit.value = true
}
function closeAdd(){ showAdd.value = false }
function closeEdit(){ showEdit.value = false; editTargetId = null }
async function performEdit(){
  error.value = ''
  try{
    await putProject(editTargetId, editItem.value)
    closeEdit()
    await refresh()
  }catch(err){ error.value = 'Update failed' }
}

async function removeProject(p){
  // replaced by askRemoveProject
}

function askRemoveProject(p){
  deleteTargetId = p.id
  deleteItemLabel.value = p.project_name
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
    await deleteProject(deleteTargetId)
    closeConfirm()
    await refresh()
  }catch(err){ error.value = 'Delete failed' }
}
</script>
