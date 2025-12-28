<template>
  <section>
    <h2>Work Experience</h2>
    <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-bottom:12px">
      <div v-if="isAuthed">
        <button class="btn" @click="showAdd=true"><i class="fas fa-plus"></i> Add Work</button>
      </div>
      <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center">
        <div style="position:relative">
          <button class="btn secondary" @click="toggleFilter"><i class="fas fa-filter"></i> Filter</button>
          <div v-if="filterOpen" class="card" style="position:absolute; top:110%; left:0; min-width:240px; z-index:10; padding:10px; display:flex; flex-direction:column; gap:8px">
            <strong>Roles</strong>
            <small style="color:#6b7280">Checked roles are hidden</small>
            <label v-for="role in roleOptions" :key="role" style="display:flex; align-items:center; gap:6px">
              <input type="checkbox" v-model="activeRoles" :value="role" />
              <span>{{ role }}</span>
            </label>
            <button class="btn secondary" style="padding:6px 10px; align-self:flex-start" @click="clearFilters"><i class="fas fa-undo"></i> Clear</button>
          </div>
        </div>
        <div style="position:relative">
          <button class="btn secondary" @click="toggleSort"><i class="fas fa-sort"></i> Sort: {{ sortLabel }}</button>
          <div v-if="sortOpen" class="card" style="position:absolute; top:110%; left:0; min-width:200px; z-index:10; padding:10px; display:flex; flex-direction:column; gap:6px">
            <button class="btn secondary" :class="{active: sortMode==='alpha-asc'}" @click="setSortAndClose('alpha-asc')">Company A → Z</button>
            <button class="btn secondary" :class="{active: sortMode==='alpha-desc'}" @click="setSortAndClose('alpha-desc')">Company Z → A</button>
            <button class="btn secondary" :class="{active: sortMode==='start-new'}" @click="setSortAndClose('start-new')">Start: Newest</button>
            <button class="btn secondary" :class="{active: sortMode==='start-old'}" @click="setSortAndClose('start-old')">Start: Oldest</button>
            <button class="btn secondary" :class="{active: sortMode==='end-new'}" @click="setSortAndClose('end-new')">End: Newest</button>
            <button class="btn secondary" :class="{active: sortMode==='end-old'}" @click="setSortAndClose('end-old')">End: Oldest</button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-for="w in filteredAndSorted" :key="w.id" class="card">
        <div style="display:flex; gap:12px; align-items:start">
          <img v-if="w.organization_logo" :src="getLogoUrl('work', w.id)" alt="Logo" style="width:48px; height:48px; object-fit:contain; border-radius:4px" />
          <div style="flex:1">
            <strong>{{ w.company_name }}</strong>
            <div>{{ w.role }}</div>
            <div>{{ formatDate(w.start_date) }} - {{ w.end_date ? formatDate(w.end_date) : 'Present' }}</div>
            <p style="white-space:pre-wrap">{{ w.description }}</p>
          </div>
        </div>
        <div v-if="isAuthed" class="card-actions">
          <button class="btn-icon secondary" @click="startEdit(w)" title="Edit"><i class="fas fa-edit"></i></button>
          <button class="btn-icon danger" @click="askRemoveWork(w)" title="Delete"><i class="fas fa-trash"></i></button>
        </div>
      </div>
    </div>

    <!-- Add Modal -->
    <Modal :open="showAdd" title="Add Work" @close="closeAdd">
      <div style="display:flex; gap:8px; flex-direction:column">
        <input class="input" v-model="newItem.company_name" placeholder="Company" />
        <input class="input" v-model="newItem.role" placeholder="Role" />
        <DatePicker v-model="newItem.start_date" placeholder="Start (YYYY-MM-DD)" />
        <DatePicker v-model="newItem.end_date" placeholder="End (YYYY-MM-DD)" />
        <textarea class="input" v-model="newItem.description" @keydown="handleDescriptionKeydown($event, newItem)" placeholder="Description (press Enter for new bullet)" rows="5" style="resize:vertical"></textarea>
        <label style="font-weight:600">Organization Logo (optional)</label>
        <FileDropzone
          accept="image/*"
          @selected="onNewLogoSelected"
          @cleared="onNewLogoCleared"
        >
          <template #label>
            <span>Upload organization logo (PNG, JPG, SVG)</span>
          </template>
        </FileDropzone>
        <div style="display:flex; gap:8px">
          <button class="btn" @click="addWork"><i class="fas fa-save"></i> Save</button>
          <button class="btn secondary" @click="closeAdd"><i class="fas fa-times"></i> Cancel</button>
        </div>
      </div>
      <p v-if="error" style="color:#fca5a5">{{ error }}</p>
    </Modal>

    <!-- Edit Modal -->
    <Modal :open="showEdit" title="Edit Work" @close="closeEdit">
      <div style="display:flex; gap:8px; flex-direction:column">
        <input class="input" v-model="editItem.company_name" placeholder="Company" />
        <input class="input" v-model="editItem.role" placeholder="Role" />
        <DatePicker v-model="editItem.start_date" placeholder="Start (YYYY-MM-DD)" />
        <DatePicker v-model="editItem.end_date" placeholder="End (YYYY-MM-DD)" />
        <textarea class="input" v-model="editItem.description" @keydown="handleDescriptionKeydown($event, editItem)" placeholder="Description (press Enter for new bullet)" rows="5" style="resize:vertical"></textarea>
        <label style="font-weight:600">Organization Logo (optional)</label>
        <FileDropzone
          accept="image/*"
          @selected="onEditLogoSelected"
          @cleared="onEditLogoCleared"
        >
          <template #label>
            <span>Upload new logo to replace existing (leave empty to keep current)</span>
          </template>
        </FileDropzone>
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
      title="Delete Work Record"
      :message="confirmMessage"
      @confirm="performDelete"
      @close="closeConfirm"
    />
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { apiGet, postWork, deleteWork, putWork, uploadWorkLogo } from '../lib/api.js'
import { isAuthed as authIsAuthed } from '../lib/auth.js'
import Modal from '../components/Modal.vue'
import ConfirmModal from '../components/ConfirmModal.vue'
import DatePicker from '../components/DatePicker.vue'
import FileDropzone from '../components/FileDropzone.vue'
import { formatDate } from '../lib/date.js'

const work = ref([])
const loading = ref(true)
const error = ref('')
const isAuthed = authIsAuthed
const activeRoles = ref([])
const filterOpen = ref(false)
const sortOpen = ref(false)
const sortMode = ref('start-new')
const newItem = ref({ company_name:'', role:'', start_date:'', end_date:'', description:'' })
const editItem = ref({ company_name:'', role:'', start_date:'', end_date:'', description:'' })
const newLogo = ref(null)
const editLogo = ref(null)
const showAdd = ref(false)
const showEdit = ref(false)
let editTargetId = null
const showConfirm = ref(false)
let deleteTargetId = null
const deleteItemLabel = ref('')
const confirmMessage = computed(() => `Delete "${deleteItemLabel.value}"? This cannot be undone.`)

function getLogoUrl(type, id) {
  const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
  return `${API_URL}/api/${type}/${id}/logo`
}

async function refresh(){
  try{
    work.value = await apiGet('/api/work')
  } finally {
    loading.value = false
  }
}
onMounted(refresh)

const roleOptions = computed(() => {
  const roles = new Set(work.value.map(w => w.role).filter(Boolean))
  return Array.from(roles).sort((a,b) => a.localeCompare(b))
})

const filteredAndSorted = computed(() => {
  const filtered = activeRoles.value.length
    ? work.value.filter(w => !activeRoles.value.includes(w.role))
    : work.value

  const toDate = v => v ? new Date(v) : null

  return [...filtered].sort((a,b) => {
    if(sortMode.value === 'alpha-asc') return a.company_name.localeCompare(b.company_name)
    if(sortMode.value === 'alpha-desc') return b.company_name.localeCompare(a.company_name)
    if(sortMode.value === 'start-new') return (toDate(b.start_date) - toDate(a.start_date))
    if(sortMode.value === 'start-old') return (toDate(a.start_date) - toDate(b.start_date))
    if(sortMode.value === 'end-new') return (toDate(b.end_date) || 0) - (toDate(a.end_date) || 0)
    if(sortMode.value === 'end-old') return (toDate(a.end_date) || 0) - (toDate(b.end_date) || 0)
    return 0
  })
})

function setSortAndClose(mode){
  sortMode.value = mode
  sortOpen.value = false
}
function clearFilters(){
  activeRoles.value = []
}
function toggleFilter(){
  filterOpen.value = !filterOpen.value
  if(filterOpen.value) sortOpen.value = false
}
function toggleSort(){
  sortOpen.value = !sortOpen.value
  if(sortOpen.value) filterOpen.value = false
}
const sortLabel = computed(() => {
  if(sortMode.value === 'alpha-asc') return 'Company A → Z'
  if(sortMode.value === 'alpha-desc') return 'Company Z → A'
  if(sortMode.value === 'start-new') return 'Start: Newest'
  if(sortMode.value === 'start-old') return 'Start: Oldest'
  if(sortMode.value === 'end-new') return 'End: Newest'
  if(sortMode.value === 'end-old') return 'End: Oldest'
  return 'Choose'
})

async function addWork(){
  error.value = ''
  try{
    const created = await postWork(newItem.value)
    const createdId = created?.data?.[0]?.id
    if (createdId && newLogo.value) {
      await uploadWorkLogo(createdId, newLogo.value)
    }
    newItem.value = { company_name:'', role:'', start_date:'', end_date:'', description:'' }
    newLogo.value = null
    await refresh()
    showAdd.value = false
  }catch(e){ error.value = 'Add failed' }
}

function startEdit(w){
  editItem.value = { company_name:w.company_name, role:w.role, start_date:w.start_date, end_date:w.end_date, description:w.description }
  editTargetId = w.id
  showEdit.value = true
}
function closeAdd(){ 
  showAdd.value = false
  newLogo.value = null
}
function closeEdit(){ 
  showEdit.value = false
  editTargetId = null
  editLogo.value = null
}
async function performEdit(){
  error.value = ''
  try{
    await putWork(editTargetId, editItem.value)
    if (editLogo.value) {
      await uploadWorkLogo(editTargetId, editLogo.value)
    }
    editLogo.value = null
    closeEdit()
    await refresh()
  }catch(e){ error.value = 'Update failed' }
}

function onNewLogoSelected(file){ newLogo.value = file }
function onNewLogoCleared(){ newLogo.value = null }
function onEditLogoSelected(file){ editLogo.value = file }
function onEditLogoCleared(){ editLogo.value = null }

function askRemoveWork(w){
  deleteTargetId = w.id
  deleteItemLabel.value = w.company_name
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
    await deleteWork(deleteTargetId)
    closeConfirm()
    await refresh()
  }catch(e){ error.value = 'Delete failed' }
}

function handleDescriptionKeydown(event, item){
  if(event.key === 'Enter'){
    // Allow Shift+Enter to insert a plain newline without bullet
    if(event.shiftKey){
      return
    }
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
