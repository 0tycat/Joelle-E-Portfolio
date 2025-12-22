<template>
  <section>
    <h2>Other Information / Projects</h2>
    <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-bottom:12px">
      <div v-if="isAuthed">
        <button class="btn" @click="showAdd=true"><i class="fas fa-plus"></i> Add Project</button>
      </div>
      <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center">
        <div style="position:relative">
          <button class="btn secondary" @click="toggleFilter"><i class="fas fa-filter"></i> Filter</button>
          <div v-if="filterOpen" class="card" style="position:absolute; top:110%; left:0; min-width:240px; z-index:10; padding:10px; display:flex; flex-direction:column; gap:8px">
            <strong>Projects</strong>
            <small style="color:#6b7280">Checked projects are hidden</small>
            <label v-for="name in projectOptions" :key="name" style="display:flex; align-items:center; gap:6px">
              <input type="checkbox" v-model="activeProjects" :value="name" />
              <span>{{ name }}</span>
            </label>
            <button class="btn secondary" style="padding:6px 10px; align-self:flex-start" @click="clearFilters"><i class="fas fa-undo"></i> Clear</button>
          </div>
        </div>
        <div style="position:relative">
          <button class="btn secondary" @click="toggleSort"><i class="fas fa-sort"></i> Sort: {{ sortLabel }}</button>
          <div v-if="sortOpen" class="card" style="position:absolute; top:110%; left:0; min-width:200px; z-index:10; padding:10px; display:flex; flex-direction:column; gap:6px">
            <button class="btn secondary" :class="{active: sortMode==='alpha-asc'}" @click="setSortAndClose('alpha-asc')">Name A to Z</button>
            <button class="btn secondary" :class="{active: sortMode==='alpha-desc'}" @click="setSortAndClose('alpha-desc')">Name Z to A</button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-for="p in filteredAndSorted" :key="p.id" class="card">
        <strong>{{ p.project_name }}</strong>
        <p style="white-space:pre-wrap">{{ p.description }}</p>
        <div v-if="isAuthed" class="card-actions">
          <button class="btn-icon secondary" @click="startEdit(p)" title="Edit"><i class="fas fa-edit"></i></button>
          <button class="btn-icon danger" @click="askRemoveProject(p)" title="Delete"><i class="fas fa-trash"></i></button>
        </div>
      </div>
    </div>

    <!-- Add Modal -->
    <Modal :open="showAdd" title="Add Project" @close="closeAdd">
      <div style="display:flex; gap:8px; flex-direction:column">
        <input class="input" v-model="newItem.project_name" placeholder="Project name" />
        <textarea class="input" v-model="newItem.description" @keydown="handleDescriptionKeydown($event, newItem)" placeholder="Description (press Enter for new bullet)" rows="5" style="resize:vertical"></textarea>
        <div style="display:flex; gap:8px">
          <button class="btn" @click="addProject"><i class="fas fa-save"></i> Save</button>
          <button class="btn secondary" @click="closeAdd"><i class="fas fa-times"></i> Cancel</button>
        </div>
      </div>
      <p v-if="error" style="color:#fca5a5">{{ error }}</p>
    </Modal>

    <!-- Edit Modal -->
    <Modal :open="showEdit" title="Edit Project" @close="closeEdit">
      <div style="display:flex; gap:8px; flex-direction:column">
        <input class="input" v-model="editItem.project_name" placeholder="Project name" />
        <textarea class="input" v-model="editItem.description" @keydown="handleDescriptionKeydown($event, editItem)" placeholder="Description (press Enter for new bullet)" rows="5" style="resize:vertical"></textarea>
        <div style="display:flex; gap:8px">
          <button class="btn" @click="performEdit"><i class="fas fa-save"></i> Save</button>
          <button class="btn secondary" @click="closeEdit"><i class="fas fa-times"></i> Cancel</button>
        </div>
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
const filterOpen = ref(false)
const sortOpen = ref(false)
const activeProjects = ref([])
const sortMode = ref('alpha-asc')
const projectOptions = computed(() => {
  const names = projects.value.map(p => p.project_name).filter(Boolean)
  return [...new Set(names)].sort((a, b) => a.localeCompare(b))
})
const sortLabel = computed(() => {
  switch (sortMode.value) {
    case 'alpha-desc':
      return 'Name Z to A'
    case 'alpha-asc':
    default:
      return 'Name A to Z'
  }
})
const filteredAndSorted = computed(() => {
  let list = projects.value
  if (activeProjects.value.length) {
    list = list.filter(p => !activeProjects.value.includes(p.project_name))
  }
  return [...list].sort((a, b) => {
    const nameA = a.project_name || ''
    const nameB = b.project_name || ''
    if (sortMode.value === 'alpha-desc') return nameB.localeCompare(nameA)
    return nameA.localeCompare(nameB)
  })
})

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

function toggleFilter(){
  filterOpen.value = !filterOpen.value
  if (filterOpen.value) sortOpen.value = false
}
function toggleSort(){
  sortOpen.value = !sortOpen.value
  if (sortOpen.value) filterOpen.value = false
}
function clearFilters(){
  activeProjects.value = []
}
function setSortAndClose(mode){
  sortMode.value = mode
  sortOpen.value = false
}

function handleDescriptionKeydown(event, item){
  if(event.key === 'Enter' && !event.shiftKey){
    event.preventDefault()
    const textarea = event.target
    const cursorPos = textarea.selectionStart
    const text = item.description || ''
    const beforeCursor = text.substring(0, cursorPos)
    const afterCursor = text.substring(cursorPos)
    
    // Check if we're at the start or if the line is empty
    const lines = beforeCursor.split('\n')
    const currentLine = lines[lines.length - 1]
    
    // If current line is just a bullet, remove it instead of adding new one
    if(currentLine.trim() === '•' || currentLine.trim() === '-'){
      const newText = text.substring(0, cursorPos - currentLine.length) + afterCursor
      item.description = newText
      setTimeout(() => {
        textarea.selectionStart = textarea.selectionEnd = cursorPos - currentLine.length
      }, 0)
      return
    }
    
    // Add new bullet point
    const bullet = currentLine.trim().startsWith('•') || currentLine.trim().startsWith('-') ? '\n• ' : (beforeCursor.trim() === '' ? '• ' : '\n• ')
    item.description = beforeCursor + bullet + afterCursor
    
    setTimeout(() => {
      textarea.selectionStart = textarea.selectionEnd = cursorPos + bullet.length
    }, 0)
  }
}
</script>
