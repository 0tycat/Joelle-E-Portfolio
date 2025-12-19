<template>
  <section>
    <h2>Community Service</h2>
    <div v-if="isAuthed" style="margin-bottom:12px">
      <button class="btn" @click="showAdd=true">Add Community Service</button>
    </div>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-for="c in community" :key="c.id" class="card">
        <strong>{{ c.programme_name }}</strong>
        <div>Role: {{ c.role }}</div>
        <div v-if="c.start_date || c.end_date" style="margin:4px 0">{{ formatDate(c.start_date) }} - {{ c.end_date ? formatDate(c.end_date) : 'Present' }}</div>
        <p style="white-space:pre-wrap">{{ c.description }}</p>
        <div v-if="isAuthed" style="margin-top:8px; display:flex; gap:8px">
          <button class="btn secondary" @click="startEdit(c)">Edit</button>
          <button class="btn danger" @click="askRemoveCommunity(c)">Delete</button>
        </div>
      </div>
    </div>

    <!-- Add Modal -->
    <Modal :open="showAdd" title="Add Community Service" @close="closeAdd">
      <div style="display:flex; gap:8px; flex-direction:column">
        <input class="input" v-model="newItem.programme_name" placeholder="Programme Name" />
        <input class="input" v-model="newItem.role" placeholder="Role" />
        <div style="display:flex; gap:8px">
          <DatePicker v-model="newItem.start_date" placeholder="Start (YYYY-MM-DD)" />
          <DatePicker v-model="newItem.end_date" placeholder="End (YYYY-MM-DD)" />
        </div>
        <textarea class="input" v-model="newItem.description" @keydown="handleDescriptionKeydown($event, newItem)" placeholder="Description (press Enter for new bullet)" rows="5" style="resize:vertical"></textarea>
        <div style="display:flex; gap:8px">
          <button class="btn" @click="addCommunity">Save</button>
          <button class="btn secondary" @click="closeAdd">Cancel</button>
        </div>
      </div>
      <p v-if="error" style="color:#fca5a5">{{ error }}</p>
    </Modal>

    <!-- Edit Modal -->
    <Modal :open="showEdit" title="Edit Community Service" @close="closeEdit">
      <div style="display:flex; gap:8px; flex-direction:column">
        <input class="input" v-model="editItem.programme_name" placeholder="Programme Name" />
        <input class="input" v-model="editItem.role" placeholder="Role" />
        <div style="display:flex; gap:8px">
          <DatePicker v-model="editItem.start_date" placeholder="Start (YYYY-MM-DD)" />
          <DatePicker v-model="editItem.end_date" placeholder="End (YYYY-MM-DD)" />
        </div>
        <textarea class="input" v-model="editItem.description" @keydown="handleDescriptionKeydown($event, editItem)" placeholder="Description (press Enter for new bullet)" rows="5" style="resize:vertical"></textarea>
        <div style="display:flex; gap:8px">
          <button class="btn" @click="performEdit">Save</button>
          <button class="btn secondary" @click="closeEdit">Cancel</button>
        </div>
      </div>
      <p v-if="error" style="color:#fca5a5">{{ error }}</p>
    </Modal>

    <!-- Confirm Delete Modal -->
    <ConfirmModal
      :open="showConfirm"
      title="Delete Community Service"
      :message="confirmMessage"
      @confirm="performDelete"
      @close="closeConfirm"
    />
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { apiGet, postCommunity, putCommunity, deleteCommunity } from '../lib/api.js'
import { isAuthed as authIsAuthed } from '../lib/auth.js'
import Modal from '../components/Modal.vue'
import ConfirmModal from '../components/ConfirmModal.vue'
import DatePicker from '../components/DatePicker.vue'
import { formatDate } from '../lib/date.js'

const community = ref([])
const loading = ref(true)
const error = ref('')
const isAuthed = authIsAuthed
const newItem = ref({ programme_name:'', role:'', start_date:'', end_date:'', description:'' })
const editItem = ref({ programme_name:'', role:'', start_date:'', end_date:'', description:'' })
const showAdd = ref(false)
const showEdit = ref(false)
let editTargetId = null
const showConfirm = ref(false)
let deleteTargetId = null
const deleteItemLabel = ref('')
const confirmMessage = computed(() => `Delete "${deleteItemLabel.value}"? This cannot be undone.`)

async function refresh(){
  try{
    community.value = await apiGet('/api/community')
  } finally {
    loading.value = false
  }
}
onMounted(refresh)

async function addCommunity(){
  error.value = ''
  try{
    await postCommunity(newItem.value)
    newItem.value = { programme_name:'', role:'', start_date:'', end_date:'', description:'' }
    await refresh()
    showAdd.value = false
  }catch(e){ error.value = 'Add failed' }
}

function startEdit(c){
  editItem.value = { programme_name:c.programme_name, role:c.role, start_date:c.start_date || '', end_date:c.end_date || '', description:c.description }
  editTargetId = c.id
  showEdit.value = true
}
function closeAdd(){ showAdd.value = false }
function closeEdit(){ showEdit.value = false; editTargetId = null }
async function performEdit(){
  error.value = ''
  try{
    await putCommunity(editTargetId, editItem.value)
    closeEdit()
    await refresh()
  }catch(e){ error.value = 'Update failed' }
}

function askRemoveCommunity(c){
  deleteTargetId = c.id
  deleteItemLabel.value = c.programme_name
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
    await deleteCommunity(deleteTargetId)
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
