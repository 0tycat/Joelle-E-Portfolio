<template>
  <section>
    <h2>E-Portfolio</h2>

    <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-bottom:12px">
      <div v-if="isAuthed">
        <button class="btn" @click="showAdd=true"><i class="fas fa-plus"></i> Add Activity</button>
      </div>
    </div>

    <div v-if="loading">Loading...</div>
    <div v-else>
      <p v-if="error" style="color:#fca5a5">{{ error }}</p>
      <div v-else>
        <div v-if="items.length===0" class="card">No activities yet.</div>
        <div v-for="item in items" :key="item.id" class="card">
          <strong>{{ item.activity_name }}</strong>
          <p style="white-space:pre-wrap">{{ item.description }}</p>
          <div v-if="isAuthed" class="card-actions">
            <button class="btn-icon secondary" @click="startEdit(item)" title="Edit"><i class="fas fa-edit"></i></button>
            <button class="btn-icon danger" @click="askRemove(item)" title="Delete"><i class="fas fa-trash"></i></button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Modal -->
    <Modal :open="showAdd" title="Add E-Portfolio Activity" @close="closeAdd">
      <div style="display:flex; gap:8px; flex-direction:column">
        <input class="input" v-model="newItem.activity_name" placeholder="Activity name" />
        <textarea class="input" v-model="newItem.description" @keydown="handleDescriptionKeydown($event, newItem)" placeholder="Description (press Enter for new bullet)" rows="5" style="resize:vertical"></textarea>
        <div style="display:flex; gap:8px">
          <button class="btn" @click="addItem"><i class="fas fa-save"></i> Save</button>
          <button class="btn secondary" @click="closeAdd"><i class="fas fa-times"></i> Cancel</button>
        </div>
      </div>
      <p v-if="error" style="color:#fca5a5">{{ error }}</p>
    </Modal>

    <!-- Edit Modal -->
    <Modal :open="showEdit" title="Edit Activity" @close="closeEdit">
      <div style="display:flex; gap:8px; flex-direction:column">
        <input class="input" v-model="editItem.activity_name" placeholder="Activity name" />
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
      title="Delete Activity"
      :message="confirmMessage"
      @confirm="performDelete"
      @close="closeConfirm"
    />
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { apiGet, postEPortfolio, deleteEPortfolio, putEPortfolio } from '../lib/api.js'
import { isAuthed as authIsAuthed } from '../lib/auth.js'
import Modal from '../components/Modal.vue'
import ConfirmModal from '../components/ConfirmModal.vue'

const items = ref([])
const loading = ref(true)
const error = ref('')
const isAuthed = authIsAuthed
const newItem = ref({ activity_name:'', description:'' })
const editItem = ref({ activity_name:'', description:'' })
const showAdd = ref(false)
const showEdit = ref(false)
let editTargetId = null
const showConfirm = ref(false)
let deleteTargetId = null
const deleteItemLabel = ref('')
const confirmMessage = computed(() => `Delete "${deleteItemLabel.value}"? This cannot be undone.`)

async function refresh(){
  try{
    error.value = ''
    items.value = await apiGet('/api/e-portfolio')
  } catch (e) {
    console.error('Failed to load e-portfolio:', e)
    error.value = 'Failed to load E-Portfolio. Please check the API service.'
  } finally {
    loading.value = false
  }
}
onMounted(refresh)

async function addItem(){
  error.value = ''
  try{
    await postEPortfolio(newItem.value)
    newItem.value = { activity_name:'', description:'' }
    await refresh()
    showAdd.value = false
  }catch(e){ error.value = 'Add failed' }
}

function startEdit(p){
  editItem.value = { activity_name:p.activity_name, description:p.description }
  editTargetId = p.id
  showEdit.value = true
}
function closeAdd(){ showAdd.value = false }
function closeEdit(){ showEdit.value = false; editTargetId = null }
async function performEdit(){
  error.value = ''
  try{
    await putEPortfolio(editTargetId, editItem.value)
    closeEdit()
    await refresh()
  }catch(err){ error.value = 'Update failed' }
}

function askRemove(p){
  deleteTargetId = p.id
  deleteItemLabel.value = p.activity_name
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
    await deleteEPortfolio(deleteTargetId)
    closeConfirm()
    await refresh()
  }catch(err){ error.value = 'Delete failed' }
}

function handleDescriptionKeydown(event, item){
  if(event.key === 'Enter' && !event.shiftKey){
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
