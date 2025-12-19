<template>
  <section>
    <h2>Work Experience</h2>
    <div v-if="isAuthed" style="margin-bottom:12px">
      <button class="btn" @click="showAdd=true"><i class="fas fa-plus"></i> Add Work</button>
    </div>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-for="w in work" :key="w.id" class="card">
        <strong>{{ w.company_name }}</strong>
        <div>{{ w.role }}</div>
        <div>{{ formatDate(w.start_date) }} - {{ w.end_date ? formatDate(w.end_date) : 'Present' }}</div>
        <p style="white-space:pre-wrap">{{ w.description }}</p>
        <div v-if="isAuthed" style="margin-top:8px; display:flex; gap:8px">
          <button class="btn secondary" @click="startEdit(w)"><i class="fas fa-edit"></i> Edit</button>
          <button class="btn danger" @click="askRemoveWork(w)"><i class="fas fa-trash"></i> Delete</button>
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
import { apiGet, postWork, deleteWork, putWork } from '../lib/api.js'
import { isAuthed as authIsAuthed } from '../lib/auth.js'
import Modal from '../components/Modal.vue'
import ConfirmModal from '../components/ConfirmModal.vue'
import DatePicker from '../components/DatePicker.vue'
import { formatDate } from '../lib/date.js'

const work = ref([])
const loading = ref(true)
const error = ref('')
const isAuthed = authIsAuthed
const newItem = ref({ company_name:'', role:'', start_date:'', end_date:'', description:'' })
const editItem = ref({ company_name:'', role:'', start_date:'', end_date:'', description:'' })
const showAdd = ref(false)
const showEdit = ref(false)
let editTargetId = null
const showConfirm = ref(false)
let deleteTargetId = null
const deleteItemLabel = ref('')
const confirmMessage = computed(() => `Delete "${deleteItemLabel.value}"? This cannot be undone.`)

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
    showAdd.value = false
  }catch(e){ error.value = 'Add failed' }
}

function startEdit(w){
  editItem.value = { company_name:w.company_name, role:w.role, start_date:w.start_date, end_date:w.end_date, description:w.description }
  editTargetId = w.id
  showEdit.value = true
}
function closeAdd(){ showAdd.value = false }
function closeEdit(){ showEdit.value = false; editTargetId = null }
async function performEdit(){
  error.value = ''
  try{
    await putWork(editTargetId, editItem.value)
    closeEdit()
    await refresh()
  }catch(e){ error.value = 'Update failed' }
}

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
