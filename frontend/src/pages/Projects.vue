<template>
  <section>
    <h2>Projects & Activities</h2>
    
    <!-- Tab Navigation -->
    <div style="display:flex; gap:8px; margin-bottom:16px; border-bottom:2px solid var(--border-color); flex-wrap:wrap">
      <button 
        @click="activeTab = 'community'" 
        :class="{ active: activeTab === 'community' }"
        style="padding:8px 16px; border:none; background:none; cursor:pointer; color:var(--text-primary); border-bottom:3px solid transparent; font-weight:500"
        :style="activeTab === 'community' ? { borderBottomColor: 'var(--primary-color)' } : {}"
      >
        Community
      </button>
      <button 
        @click="activeTab = 'module'" 
        :class="{ active: activeTab === 'module' }"
        style="padding:8px 16px; border:none; background:none; cursor:pointer; color:var(--text-primary); border-bottom:3px solid transparent; font-weight:500"
        :style="activeTab === 'module' ? { borderBottomColor: 'var(--primary-color)' } : {}"
      >
        Module Projects
      </button>
    </div>

    <!-- Community Service Tab -->
    <div v-if="activeTab === 'community'">
      <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-bottom:12px">
        <div v-if="isAuthed">
          <button class="btn" @click="showAddCommunity=true"><i class="fas fa-plus"></i> Add Community Service</button>
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center">
          <div style="position:relative">
            <button class="btn secondary" @click="toggleFilterCommunity"><i class="fas fa-filter"></i> Filter</button>
            <div v-if="filterOpenCommunity" class="card" style="position:absolute; top:110%; left:0; min-width:240px; z-index:10; padding:10px; display:flex; flex-direction:column; gap:8px">
              <strong>Roles</strong>
              <small style="color:#6b7280">Checked roles are hidden</small>
              <label v-for="role in roleOptions" :key="role" style="display:flex; align-items:center; gap:6px">
                <input type="checkbox" v-model="activeRoles" :value="role" />
                <span>{{ role }}</span>
              </label>
              <button class="btn secondary" style="padding:6px 10px; align-self:flex-start" @click="clearFiltersCommunity"><i class="fas fa-undo"></i> Clear</button>
            </div>
          </div>
          <div style="position:relative">
            <button class="btn secondary" @click="toggleSortCommunity"><i class="fas fa-sort"></i> Sort: {{ sortLabelCommunity }}</button>
            <div v-if="sortOpenCommunity" class="card" style="position:absolute; top:110%; left:0; min-width:200px; z-index:10; padding:10px; display:flex; flex-direction:column; gap:6px">
              <button class="btn secondary" :class="{active: sortModeCommunity==='alpha-asc'}" @click="setSortAndCloseCommunity('alpha-asc')">Name A → Z</button>
              <button class="btn secondary" :class="{active: sortModeCommunity==='alpha-desc'}" @click="setSortAndCloseCommunity('alpha-desc')">Name Z → A</button>
              <button class="btn secondary" :class="{active: sortModeCommunity==='start-new'}" @click="setSortAndCloseCommunity('start-new')">Start: Newest</button>
              <button class="btn secondary" :class="{active: sortModeCommunity==='start-old'}" @click="setSortAndCloseCommunity('start-old')">Start: Oldest</button>
              <button class="btn secondary" :class="{active: sortModeCommunity==='end-new'}" @click="setSortAndCloseCommunity('end-new')">End: Newest</button>
              <button class="btn secondary" :class="{active: sortModeCommunity==='end-old'}" @click="setSortAndCloseCommunity('end-old')">End: Oldest</button>
            </div>
          </div>
        </div>
      </div>
      <div v-if="loadingCommunity">Loading...</div>
      <div v-else>
        <div v-for="c in filteredAndSortedCommunity" :key="c.id" class="card">
          <strong>{{ c.programme_name }}</strong>
          <div>Role: {{ c.role }}</div>
          <div v-if="c.start_date || c.end_date" style="margin:4px 0">{{ formatDate(c.start_date) }} - {{ c.end_date ? formatDate(c.end_date) : 'Present' }}</div>
          <p style="white-space:pre-wrap">{{ c.description }}</p>
          <div v-if="isAuthed" class="card-actions">
            <button class="btn-icon secondary" @click="startEditCommunity(c)" title="Edit"><i class="fas fa-edit"></i></button>
            <button class="btn-icon danger" @click="askRemoveCommunity(c)" title="Delete"><i class="fas fa-trash"></i></button>
          </div>
        </div>
      </div>

      <!-- Add Community Modal -->
      <Modal :open="showAddCommunity" title="Add Community Service" @close="closeAddCommunity">
        <div style="display:flex; gap:8px; flex-direction:column">
          <input class="input" v-model="newCommunity.programme_name" placeholder="Programme Name" />
          <input class="input" v-model="newCommunity.role" placeholder="Role" />
          <div style="display:flex; gap:8px">
            <DatePicker v-model="newCommunity.start_date" placeholder="Start (YYYY-MM-DD)" />
            <DatePicker v-model="newCommunity.end_date" placeholder="End (YYYY-MM-DD)" />
          </div>
          <textarea class="input" v-model="newCommunity.description" @keydown="handleDescriptionKeydown($event, newCommunity)" placeholder="Description (press Enter for new bullet)" rows="5" style="resize:vertical"></textarea>
          <div style="display:flex; gap:8px">
            <button class="btn" @click="addCommunity"><i class="fas fa-save"></i> Save</button>
            <button class="btn secondary" @click="closeAddCommunity"><i class="fas fa-times"></i> Cancel</button>
          </div>
        </div>
        <p v-if="errorCommunity" style="color:#fca5a5">{{ errorCommunity }}</p>
      </Modal>

      <!-- Edit Community Modal -->
      <Modal :open="showEditCommunity" title="Edit Community Service" @close="closeEditCommunity">
        <div style="display:flex; gap:8px; flex-direction:column">
          <input class="input" v-model="editCommunity.programme_name" placeholder="Programme Name" />
          <input class="input" v-model="editCommunity.role" placeholder="Role" />
          <div style="display:flex; gap:8px">
            <DatePicker v-model="editCommunity.start_date" placeholder="Start (YYYY-MM-DD)" />
            <DatePicker v-model="editCommunity.end_date" placeholder="End (YYYY-MM-DD)" />
          </div>
          <textarea class="input" v-model="editCommunity.description" @keydown="handleDescriptionKeydown($event, editCommunity)" placeholder="Description (press Enter for new bullet)" rows="5" style="resize:vertical"></textarea>
          <div style="display:flex; gap:8px">
            <button class="btn" @click="performEditCommunity"><i class="fas fa-save"></i> Save</button>
            <button class="btn secondary" @click="closeEditCommunity"><i class="fas fa-times"></i> Cancel</button>
          </div>
        </div>
        <p v-if="errorCommunity" style="color:#fca5a5">{{ errorCommunity }}</p>
      </Modal>
    </div>

    <!-- Module Projects Tab -->
    <div v-if="activeTab === 'module'">
      <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-bottom:12px">
        <div v-if="isAuthed">
          <button class="btn" @click="showAddModule=true"><i class="fas fa-plus"></i> Add Module Project</button>
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center">
          <div style="position:relative">
            <button class="btn secondary" @click="toggleFilterModule"><i class="fas fa-filter"></i> Filter</button>
            <div v-if="filterOpenModule" class="card" style="position:absolute; top:110%; left:0; min-width:240px; z-index:10; padding:10px; display:flex; flex-direction:column; gap:8px">
              <strong>Projects</strong>
              <small style="color:#6b7280">Checked projects are hidden</small>
              <label v-for="name in moduleOptions" :key="name" style="display:flex; align-items:center; gap:6px">
                <input type="checkbox" v-model="activeModules" :value="name" />
                <span>{{ name }}</span>
              </label>
              <button class="btn secondary" style="padding:6px 10px; align-self:flex-start" @click="clearFiltersModule"><i class="fas fa-undo"></i> Clear</button>
            </div>
          </div>
          <div style="position:relative">
            <button class="btn secondary" @click="toggleSortModule"><i class="fas fa-sort"></i> Sort: {{ sortLabelModule }}</button>
            <div v-if="sortOpenModule" class="card" style="position:absolute; top:110%; left:0; min-width:200px; z-index:10; padding:10px; display:flex; flex-direction:column; gap:6px">
              <button class="btn secondary" :class="{active: sortModeModule==='alpha-asc'}" @click="setSortAndCloseModule('alpha-asc')">Name A to Z</button>
              <button class="btn secondary" :class="{active: sortModeModule==='alpha-desc'}" @click="setSortAndCloseModule('alpha-desc')">Name Z to A</button>
            </div>
          </div>
        </div>
      </div>
      <div v-if="loadingModule">Loading...</div>
      <div v-else>
        <div v-for="p in filteredAndSortedModule" :key="p.id" class="card">
          <strong>{{ p.project_name }}</strong>
          <p style="white-space:pre-wrap">{{ p.description }}</p>
          <div v-if="isAuthed" class="card-actions">
            <button class="btn-icon secondary" @click="startEditModule(p)" title="Edit"><i class="fas fa-edit"></i></button>
            <button class="btn-icon danger" @click="askRemoveModule(p)" title="Delete"><i class="fas fa-trash"></i></button>
          </div>
        </div>
      </div>

      <!-- Add Module Modal -->
      <Modal :open="showAddModule" title="Add Module Project" @close="closeAddModule">
        <div style="display:flex; gap:8px; flex-direction:column">
          <input class="input" v-model="newModule.project_name" placeholder="Project name" />
          <textarea class="input" v-model="newModule.description" @keydown="handleDescriptionKeydown($event, newModule)" placeholder="Description (press Enter for new bullet)" rows="5" style="resize:vertical"></textarea>
          <div style="display:flex; gap:8px">
            <button class="btn" @click="addModule"><i class="fas fa-save"></i> Save</button>
            <button class="btn secondary" @click="closeAddModule"><i class="fas fa-times"></i> Cancel</button>
          </div>
        </div>
        <p v-if="errorModule" style="color:#fca5a5">{{ errorModule }}</p>
      </Modal>

      <!-- Edit Module Modal -->
      <Modal :open="showEditModule" title="Edit Module Project" @close="closeEditModule">
        <div style="display:flex; gap:8px; flex-direction:column">
          <input class="input" v-model="editModule.project_name" placeholder="Project name" />
          <textarea class="input" v-model="editModule.description" @keydown="handleDescriptionKeydown($event, editModule)" placeholder="Description (press Enter for new bullet)" rows="5" style="resize:vertical"></textarea>
          <div style="display:flex; gap:8px">
            <button class="btn" @click="performEditModule"><i class="fas fa-save"></i> Save</button>
            <button class="btn secondary" @click="closeEditModule"><i class="fas fa-times"></i> Cancel</button>
          </div>
        </div>
        <p v-if="errorModule" style="color:#fca5a5">{{ errorModule }}</p>
      </Modal>
    </div>

    <!-- Confirm Delete Modal -->
    <ConfirmModal
      :open="showConfirm"
      title="Delete Item"
      :message="confirmMessage"
      @confirm="performDelete"
      @close="closeConfirm"
    />
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { apiGet, postProject, deleteProject, putProject, postCommunity, putCommunity, deleteCommunity } from '../lib/api.js'
import { isAuthed as authIsAuthed } from '../lib/auth.js'
import Modal from '../components/Modal.vue'
import ConfirmModal from '../components/ConfirmModal.vue'
import DatePicker from '../components/DatePicker.vue'
import { formatDate } from '../lib/date.js'

const activeTab = ref('community')
const isAuthed = authIsAuthed

// Community Service State
const community = ref([])
const loadingCommunity = ref(true)
const errorCommunity = ref('')
const activeRoles = ref([])
const filterOpenCommunity = ref(false)
const sortOpenCommunity = ref(false)
const sortModeCommunity = ref('start-new')
const newCommunity = ref({ programme_name:'', role:'', start_date:'', end_date:'', description:'' })
const editCommunity = ref({ programme_name:'', role:'', start_date:'', end_date:'', description:'' })
const showAddCommunity = ref(false)
const showEditCommunity = ref(false)
let editTargetCommunityId = null

// Module Projects State
const modules = ref([])
const loadingModule = ref(true)
const errorModule = ref('')
const activeModules = ref([])
const filterOpenModule = ref(false)
const sortOpenModule = ref(false)
const sortModeModule = ref('alpha-asc')
const newModule = ref({ project_name:'', description:'' })
const editModule = ref({ project_name:'', description:'' })
const showAddModule = ref(false)
const showEditModule = ref(false)
let editTargetModuleId = null

// Confirm Delete State
const showConfirm = ref(false)
let deleteTargetId = null
let deleteType = null
const deleteItemLabel = ref('')
const confirmMessage = computed(() => `Delete "${deleteItemLabel.value}"? This cannot be undone.`)

// Load data
async function loadAll(){
  try {
    community.value = await apiGet('/api/community')
  } finally {
    loadingCommunity.value = false
  }
  try {
    modules.value = await apiGet('/api/projects')
  } finally {
    loadingModule.value = false
  }
}
onMounted(loadAll)

// Community Computed
const roleOptions = computed(() => {
  const roles = new Set(community.value.map(c => c.role).filter(Boolean))
  return Array.from(roles).sort((a,b) => a.localeCompare(b))
})

const filteredAndSortedCommunity = computed(() => {
  const filtered = activeRoles.value.length
    ? community.value.filter(c => !activeRoles.value.includes(c.role))
    : community.value

  const toDate = v => v ? new Date(v) : null

  return [...filtered].sort((a,b) => {
    if(sortModeCommunity.value === 'alpha-asc') return a.programme_name.localeCompare(b.programme_name)
    if(sortModeCommunity.value === 'alpha-desc') return b.programme_name.localeCompare(a.programme_name)
    if(sortModeCommunity.value === 'start-new') return (toDate(b.start_date) - toDate(a.start_date))
    if(sortModeCommunity.value === 'start-old') return (toDate(a.start_date) - toDate(b.start_date))
    if(sortModeCommunity.value === 'end-new') return (toDate(b.end_date) || 0) - (toDate(a.end_date) || 0)
    if(sortModeCommunity.value === 'end-old') return (toDate(a.end_date) || 0) - (toDate(b.end_date) || 0)
    return 0
  })
})

const sortLabelCommunity = computed(() => {
  if(sortModeCommunity.value === 'alpha-asc') return 'Name A → Z'
  if(sortModeCommunity.value === 'alpha-desc') return 'Name Z → A'
  if(sortModeCommunity.value === 'start-new') return 'Start: Newest'
  if(sortModeCommunity.value === 'start-old') return 'Start: Oldest'
  if(sortModeCommunity.value === 'end-new') return 'End: Newest'
  if(sortModeCommunity.value === 'end-old') return 'End: Oldest'
  return 'Choose'
})

// Module Computed
const moduleOptions = computed(() => {
  const names = modules.value.map(p => p.project_name).filter(Boolean)
  return [...new Set(names)].sort((a, b) => a.localeCompare(b))
})

const filteredAndSortedModule = computed(() => {
  let list = modules.value
  if (activeModules.value.length) {
    list = list.filter(p => !activeModules.value.includes(p.project_name))
  }
  return [...list].sort((a, b) => {
    const nameA = a.project_name || ''
    const nameB = b.project_name || ''
    if (sortModeModule.value === 'alpha-desc') return nameB.localeCompare(nameA)
    return nameA.localeCompare(nameB)
  })
})

const sortLabelModule = computed(() => {
  if(sortModeModule.value === 'alpha-desc') return 'Name Z to A'
  return 'Name A to Z'
})

// Community Functions
async function addCommunity(){
  errorCommunity.value = ''
  try{
    await postCommunity(newCommunity.value)
    newCommunity.value = { programme_name:'', role:'', start_date:'', end_date:'', description:'' }
    await loadAll()
    showAddCommunity.value = false
  }catch(e){ errorCommunity.value = 'Add failed' }
}

function startEditCommunity(c){
  editCommunity.value = { programme_name:c.programme_name, role:c.role, start_date:c.start_date || '', end_date:c.end_date || '', description:c.description }
  editTargetCommunityId = c.id
  showEditCommunity.value = true
}

function closeAddCommunity(){ showAddCommunity.value = false }
function closeEditCommunity(){ showEditCommunity.value = false; editTargetCommunityId = null }

async function performEditCommunity(){
  errorCommunity.value = ''
  try{
    await putCommunity(editTargetCommunityId, editCommunity.value)
    closeEditCommunity()
    await loadAll()
  }catch(e){ errorCommunity.value = 'Update failed' }
}

function askRemoveCommunity(c){
  deleteTargetId = c.id
  deleteType = 'community'
  deleteItemLabel.value = c.programme_name
  showConfirm.value = true
}

function toggleFilterCommunity(){
  filterOpenCommunity.value = !filterOpenCommunity.value
  if (filterOpenCommunity.value) sortOpenCommunity.value = false
}

function toggleSortCommunity(){
  sortOpenCommunity.value = !sortOpenCommunity.value
  if (sortOpenCommunity.value) filterOpenCommunity.value = false
}

function clearFiltersCommunity(){
  activeRoles.value = []
}

function setSortAndCloseCommunity(mode){
  sortModeCommunity.value = mode
  sortOpenCommunity.value = false
}

// Module Functions
async function addModule(){
  errorModule.value = ''
  try{
    await postProject(newModule.value)
    newModule.value = { project_name:'', description:'' }
    await loadAll()
    showAddModule.value = false
  }catch(e){ errorModule.value = 'Add failed' }
}

function startEditModule(p){
  editModule.value = { project_name:p.project_name, description:p.description }
  editTargetModuleId = p.id
  showEditModule.value = true
}

function closeAddModule(){ showAddModule.value = false }
function closeEditModule(){ showEditModule.value = false; editTargetModuleId = null }

async function performEditModule(){
  errorModule.value = ''
  try{
    await putProject(editTargetModuleId, editModule.value)
    closeEditModule()
    await loadAll()
  }catch(err){ errorModule.value = 'Update failed' }
}

function askRemoveModule(p){
  deleteTargetId = p.id
  deleteType = 'module'
  deleteItemLabel.value = p.project_name
  showConfirm.value = true
}

function toggleFilterModule(){
  filterOpenModule.value = !filterOpenModule.value
  if (filterOpenModule.value) sortOpenModule.value = false
}

function toggleSortModule(){
  sortOpenModule.value = !sortOpenModule.value
  if (sortOpenModule.value) filterOpenModule.value = false
}

function clearFiltersModule(){
  activeModules.value = []
}

function setSortAndCloseModule(mode){
  sortModeModule.value = mode
  sortOpenModule.value = false
}

// Delete
function closeConfirm(){
  showConfirm.value = false
  deleteTargetId = null
  deleteType = null
  deleteItemLabel.value = ''
}

async function performDelete(){
  errorCommunity.value = ''
  errorModule.value = ''
  try{
    if(deleteType === 'community'){
      await deleteCommunity(deleteTargetId)
    } else if(deleteType === 'module'){
      await deleteProject(deleteTargetId)
    }
    closeConfirm()
    await loadAll()
  }catch(err){ 
    if(deleteType === 'community') errorCommunity.value = 'Delete failed'
    else if(deleteType === 'module') errorModule.value = 'Delete failed'
  }
}

function handleDescriptionKeydown(event, item){
  if(event.key === 'Enter'){
    if(event.shiftKey){
      return
    }
    event.preventDefault()
    const textarea = event.target
    const cursorPos = textarea.selectionStart
    const text = item.description || ''
    const beforeCursor = text.substring(0, cursorPos)
    const afterCursor = text.substring(cursorPos)
    
    const lines = beforeCursor.split('\n')
    const currentLine = lines[lines.length - 1]
    
    if(currentLine.trim() === '•' || currentLine.trim() === '-'){
      const newText = text.substring(0, cursorPos - currentLine.length) + afterCursor
      item.description = newText
      setTimeout(() => {
        textarea.selectionStart = textarea.selectionEnd = cursorPos - currentLine.length
      }, 0)
      return
    }
    
    const bullet = currentLine.trim().startsWith('•') || currentLine.trim().startsWith('-') ? '\n• ' : (beforeCursor.trim() === '' ? '• ' : '\n• ')
    item.description = beforeCursor + bullet + afterCursor
    
    setTimeout(() => {
      textarea.selectionStart = textarea.selectionEnd = cursorPos + bullet.length
    }, 0)
  }
}
</script>
