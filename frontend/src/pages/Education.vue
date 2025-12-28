<template>
  <section>
    <h2>Education</h2>
    <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-bottom:12px">
      <div v-if="isAuthed">
        <button class="btn" @click="showAdd=true"><i class="fas fa-plus"></i> Add Education</button>
      </div>
      <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center">
        <div style="position:relative">
          <button class="btn secondary" @click="toggleFilter"><i class="fas fa-filter"></i> Filter</button>
          <div v-if="filterOpen" class="card" style="position:absolute; top:110%; left:0; min-width:240px; z-index:10; padding:10px; display:flex; flex-direction:column; gap:8px">
            <strong>Institutes</strong>
            <small style="color:#6b7280">Checked institutes are hidden</small>
            <label v-for="inst in instituteOptions" :key="inst" style="display:flex; align-items:center; gap:6px">
              <input type="checkbox" v-model="activeInstitutes" :value="inst" />
              <span>{{ inst }}</span>
            </label>
            <button class="btn secondary" style="padding:6px 10px; align-self:flex-start" @click="clearFilters"><i class="fas fa-undo"></i> Clear</button>
          </div>
        </div>
        <div style="position:relative">
          <button class="btn secondary" @click="toggleSort"><i class="fas fa-sort"></i> Sort: {{ sortLabel }}</button>
          <div v-if="sortOpen" class="card" style="position:absolute; top:110%; left:0; min-width:200px; z-index:10; padding:10px; display:flex; flex-direction:column; gap:6px">
            <button class="btn secondary" :class="{active: sortMode==='alpha-asc'}" @click="setSortAndClose('alpha-asc')">Institute A → Z</button>
            <button class="btn secondary" :class="{active: sortMode==='alpha-desc'}" @click="setSortAndClose('alpha-desc')">Institute Z → A</button>
            <button class="btn secondary" :class="{active: sortMode==='start-new'}" @click="setSortAndClose('start-new')">Start: Newest</button>
            <button class="btn secondary" :class="{active: sortMode==='start-old'}" @click="setSortAndClose('start-old')">Start: Oldest</button>
            <button class="btn secondary" :class="{active: sortMode==='end-new'}" @click="setSortAndClose('end-new')">Finish: Newest</button>
            <button class="btn secondary" :class="{active: sortMode==='end-old'}" @click="setSortAndClose('end-old')">Finish: Oldest</button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-for="e in filteredAndSorted" :key="e.id" class="card">
        <div style="display:flex; gap:12px; align-items:start">
          <img v-if="e.organization_logo" :src="getLogoUrl('education', e.id)" alt="Logo" style="width:48px; height:48px; object-fit:contain; border-radius:4px" />
          <div style="flex:1">
            <strong>{{ e.institute_name }}</strong>
            <div>{{ e.certification }}</div>
            <div>{{ formatDate(e.start_date) }} - {{ e.finish_date ? formatDate(e.finish_date) : 'Present' }}</div>
          </div>
        </div>
        <div v-if="isAuthed" class="card-actions">
          <button class="btn-icon secondary" @click="startEdit(e)" title="Edit"><i class="fas fa-edit"></i></button>
          <button class="btn-icon danger" @click="askRemoveEducation(e)" title="Delete"><i class="fas fa-trash"></i></button>
        </div>
      </div>
    </div>

    <!-- Add Modal -->
    <Modal :open="showAdd" title="Add Education" @close="closeAdd">
      <div style="display:flex; gap:8px; flex-direction:column">
        <input class="input" v-model="newItem.institute_name" placeholder="Institute" />
        <input class="input" v-model="newItem.certification" placeholder="Certification" />
        <DatePicker v-model="newItem.start_date" placeholder="Start (YYYY-MM-DD)" />
        <DatePicker v-model="newItem.finish_date" placeholder="Finish (YYYY-MM-DD)" />
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
          <button class="btn" @click="addEducation"><i class="fas fa-save"></i> Save</button>
          <button class="btn secondary" @click="closeAdd"><i class="fas fa-times"></i> Cancel</button>
        </div>
      </div>
      <p v-if="error" style="color:#fca5a5">{{ error }}</p>
    </Modal>

    <!-- Edit Modal -->
    <Modal :open="showEdit" title="Edit Education" @close="closeEdit">
      <div style="display:flex; gap:8px; flex-direction:column">
        <input class="input" v-model="editItem.institute_name" placeholder="Institute" />
        <input class="input" v-model="editItem.certification" placeholder="Certification" />
        <DatePicker v-model="editItem.start_date" placeholder="Start (YYYY-MM-DD)" />
        <DatePicker v-model="editItem.finish_date" placeholder="Finish (YYYY-MM-DD)" />
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
      title="Delete Education Record"
      :message="confirmMessage"
      @confirm="performDelete"
      @close="closeConfirm"
    />
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { apiGet, postEducation, deleteEducation, putEducation, uploadEducationLogo } from '../lib/api.js'
import { isAuthed as authIsAuthed } from '../lib/auth.js'
import Modal from '../components/Modal.vue'
import ConfirmModal from '../components/ConfirmModal.vue'
import DatePicker from '../components/DatePicker.vue'
import FileDropzone from '../components/FileDropzone.vue'
import { formatDate } from '../lib/date.js'

const education = ref([])
const loading = ref(true)
const error = ref('')
const isAuthed = authIsAuthed
const activeInstitutes = ref([])
const filterOpen = ref(false)
const sortOpen = ref(false)
const sortMode = ref('start-new')
const newItem = ref({ institute_name:'', certification:'', start_date:'', finish_date:'' })
const editItem = ref({ institute_name:'', certification:'', start_date:'', finish_date:'' })
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
    education.value = await apiGet('/api/education')
  } finally {
    loading.value = false
  }
}
onMounted(refresh)

const instituteOptions = computed(() => {
  const set = new Set(education.value.map(e => e.institute_name).filter(Boolean))
  return Array.from(set).sort((a,b) => a.localeCompare(b))
})

const filteredAndSorted = computed(() => {
  const filtered = activeInstitutes.value.length
    ? education.value.filter(e => !activeInstitutes.value.includes(e.institute_name))
    : education.value

  const toDate = v => v ? new Date(v) : null

  return [...filtered].sort((a,b) => {
    if(sortMode.value === 'alpha-asc') return a.institute_name.localeCompare(b.institute_name)
    if(sortMode.value === 'alpha-desc') return b.institute_name.localeCompare(a.institute_name)
    if(sortMode.value === 'start-new') return (toDate(b.start_date) - toDate(a.start_date))
    if(sortMode.value === 'start-old') return (toDate(a.start_date) - toDate(b.start_date))
    if(sortMode.value === 'end-new') return (toDate(b.finish_date) || 0) - (toDate(a.finish_date) || 0)
    if(sortMode.value === 'end-old') return (toDate(a.finish_date) || 0) - (toDate(b.finish_date) || 0)
    return 0
  })
})

function setSortAndClose(mode){
  sortMode.value = mode
  sortOpen.value = false
}
function clearFilters(){
  activeInstitutes.value = []
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
  if(sortMode.value === 'alpha-asc') return 'Institute A → Z'
  if(sortMode.value === 'alpha-desc') return 'Institute Z → A'
  if(sortMode.value === 'start-new') return 'Start: Newest'
  if(sortMode.value === 'start-old') return 'Start: Oldest'
  if(sortMode.value === 'end-new') return 'Finish: Newest'
  if(sortMode.value === 'end-old') return 'Finish: Oldest'
  return 'Choose'
})

async function addEducation(){
  error.value = ''
  try{
    const created = await postEducation(newItem.value)
    const createdId = created?.data?.[0]?.id
    if (createdId && newLogo.value) {
      await uploadEducationLogo(createdId, newLogo.value)
    }
    newItem.value = { institute_name:'', certification:'', start_date:'', finish_date:'' }
    newLogo.value = null
    await refresh()
    showAdd.value = false
  }catch(e){ error.value = 'Add failed' }
}

function startEdit(e){
  editItem.value = { institute_name:e.institute_name, certification:e.certification, start_date:e.start_date, finish_date:e.finish_date }
  editTargetId = e.id
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
    await putEducation(editTargetId, editItem.value)
    if (editLogo.value) {
      await uploadEducationLogo(editTargetId, editLogo.value)
    }
    editLogo.value = null
    closeEdit()
    await refresh()
  }catch(err){ error.value = 'Update failed' }
}

function onNewLogoSelected(file){ newLogo.value = file }
function onNewLogoCleared(){ newLogo.value = null }
function onEditLogoSelected(file){ editLogo.value = file }
function onEditLogoCleared(){ editLogo.value = null }

async function removeEducation(e){
  // replaced by askRemoveEducation
}

function askRemoveEducation(e){
  deleteTargetId = e.id
  deleteItemLabel.value = e.institute_name
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
    await deleteEducation(deleteTargetId)
    closeConfirm()
    await refresh()
  }catch(err){ error.value = 'Delete failed' }
}
</script>
