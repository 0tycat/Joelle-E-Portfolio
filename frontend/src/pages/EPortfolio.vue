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
          <div v-if="item.activity_type" style="color:#6b7280; font-size:0.9em">{{ item.activity_type }}</div>
          <div v-if="item.start_date || item.finish_date" style="margin:4px 0">
            {{ formatDate(item.start_date) }} - {{ item.finish_date ? formatDate(item.finish_date) : 'Present' }}
          </div>
          <div v-if="item.organisation_module"><strong>Organisation/Module:</strong> {{ item.organisation_module }}</div>
          <p v-if="item.description" style="white-space:pre-wrap; margin-top:8px"><strong>Description:</strong><br/>{{ item.description }}</p>
          <p v-if="item.what_i_did" style="white-space:pre-wrap; margin-top:8px"><strong>What I Did:</strong><br/>{{ item.what_i_did }}</p>
          <p v-if="item.skills_tools_acquired" style="white-space:pre-wrap; margin-top:8px"><strong>Skills & Tools:</strong><br/>{{ item.skills_tools_acquired }}</p>
          <p v-if="item.takeaways" style="white-space:pre-wrap; margin-top:8px"><strong>Key Takeaways:</strong><br/>{{ item.takeaways }}</p>
          <!-- Hide raw links text; files are shown below as chips -->
          <p v-if="item.relevance_career" style="white-space:pre-wrap; margin-top:8px"><strong>Relevance to Career:</strong><br/>{{ item.relevance_career }}</p>
          <div v-if="evidenceList(item).length" style="margin-top:8px">
            <div style="font-size:0.85em; color:#6b7280; margin-bottom:4px">Evidence Files</div>
            <div v-for="(f, idx) in evidenceList(item)" :key="idx" style="margin:4px 8px 0 0; display:inline-flex; align-items:center; gap:6px; padding:6px 10px; border:1px solid var(--border-color); border-radius:6px; background:var(--bg-tertiary)">
              <i class="fas fa-file"></i>
              <span style="font-size:0.9em">{{ f.label }}</span>
              <span style="color:#d1d5db">|</span>
              <button @click="previewEvidenceItem(item.id, f)" style="background:none; border:none; color:#2563eb; text-decoration:underline; cursor:pointer; padding:0; font-size:inherit" title="Preview file">
                <i class="fas fa-eye"></i> Preview
              </button>
              <span style="color:#d1d5db">|</span>
              <button @click="downloadEvidenceItem(item.id, f)" style="background:none; border:none; color:#2563eb; text-decoration:underline; cursor:pointer; padding:0; font-size:inherit" title="Download file">
                <i class="fas fa-download"></i> Download
              </button>
              <template v-if="isAuthed">
                <span style="color:#d1d5db">|</span>
                <button @click="removeEvidenceItem(item.id, f)" style="background:none; border:none; color:#ef4444; text-decoration:underline; cursor:pointer; padding:0; font-size:inherit" title="Remove file">
                  <i class="fas fa-times"></i> Remove
                </button>
              </template>
            </div>
          </div>
          <div v-if="isAuthed" class="card-actions">
            <button class="btn-icon secondary" @click="startEdit(item)" title="Edit"><i class="fas fa-edit"></i></button>
            <button class="btn-icon danger" @click="askRemove(item)" title="Delete"><i class="fas fa-trash"></i></button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Modal -->
    <Modal :open="showAdd" title="Add E-Portfolio Activity" @close="closeAdd">
      <div style="display:flex; gap:8px; flex-direction:column; max-height:70vh; overflow-y:auto">
        <input class="input" v-model="newItem.activity_name" placeholder="Activity Name *" />
        <input class="input" v-model="newItem.activity_type" placeholder="Activity Type (e.g., Academic Project, Community Service)" />
        <DatePicker v-model="newItem.start_date" placeholder="Start Date (YYYY-MM-DD)" />
        <DatePicker v-model="newItem.finish_date" placeholder="Finish Date (YYYY-MM-DD) - leave empty for Present" />
        <input class="input" v-model="newItem.organisation_module" placeholder="Organisation / Module" />
        <textarea class="input" v-model="newItem.description" @keydown="insertBulletOnEnter" placeholder="Description / Purpose & Context" rows="3" style="resize:vertical"></textarea>
        <textarea class="input" v-model="newItem.what_i_did" @keydown="insertBulletOnEnter" placeholder="What I Did" rows="3" style="resize:vertical"></textarea>
        <textarea class="input" v-model="newItem.skills_tools_acquired" @keydown="insertBulletOnEnter" placeholder="Skills & Tools Applied/Acquired" rows="3" style="resize:vertical"></textarea>
        <textarea class="input" v-model="newItem.takeaways" @keydown="insertBulletOnEnter" placeholder="What I Learned / Key Takeaways" rows="3" style="resize:vertical"></textarea>
        <textarea class="input" v-model="newItem.artefacts_evidence_links_texts" @keydown="insertBulletOnEnter" placeholder="Evidence / Artefacts / Links" rows="2" style="resize:vertical"></textarea>
        <textarea class="input" v-model="newItem.relevance_career" @keydown="insertBulletOnEnter" placeholder="Relevance to Internship / Career" rows="2" style="resize:vertical"></textarea>
        <label style="font-weight:600">Evidence Files — drag & drop (multiple files supported)</label>
        <FileDropzone
          :accept="fileAccept"
          :multiple="true"
          @selected="onNewFilesSelected"
          @cleared="onNewFilesCleared"
        >
          <template #label>
            <strong>Drag & drop</strong> files here, or <span class="link">click to choose</span>.
            <div v-if="newFiles.length > 0" style="color:#059669; font-size:0.85em; margin-top:6px">
              {{ newFiles.length }} file(s) selected
            </div>
            <div v-else style="color:#6b7280; font-size:0.85em; margin-top:6px">
              Files will be uploaded right after Save. You can select multiple files.
            </div>
          </template>
        </FileDropzone>
        <div style="display:flex; gap:8px">
          <button class="btn" @click="addItem"><i class="fas fa-save"></i> Save</button>
          <button class="btn secondary" @click="closeAdd"><i class="fas fa-times"></i> Cancel</button>
        </div>
      </div>
      <p v-if="error" style="color:#fca5a5; margin-top:8px">{{ error }}</p>
    </Modal>

    <!-- Edit Modal -->
    <Modal :open="showEdit" title="Edit Activity" @close="closeEdit">
      <div style="display:flex; gap:8px; flex-direction:column; max-height:70vh; overflow-y:auto">
        <input class="input" v-model="editItem.activity_name" placeholder="Activity Name *" />
        <input class="input" v-model="editItem.activity_type" placeholder="Activity Type" />
        <DatePicker v-model="editItem.start_date" placeholder="Start Date (YYYY-MM-DD)" />
        <DatePicker v-model="editItem.finish_date" placeholder="Finish Date (YYYY-MM-DD) - leave empty for Present" />
        <input class="input" v-model="editItem.organisation_module" placeholder="Organisation / Module" />
        <textarea class="input" v-model="editItem.description" @keydown="insertBulletOnEnter" placeholder="Description / Purpose & Context" rows="3" style="resize:vertical"></textarea>
        <textarea class="input" v-model="editItem.what_i_did" @keydown="insertBulletOnEnter" placeholder="What I Did" rows="3" style="resize:vertical"></textarea>
        <textarea class="input" v-model="editItem.skills_tools_acquired" @keydown="insertBulletOnEnter" placeholder="Skills & Tools Applied/Acquired" rows="3" style="resize:vertical"></textarea>
        <textarea class="input" v-model="editItem.takeaways" @keydown="insertBulletOnEnter" placeholder="What I Learned / Key Takeaways" rows="3" style="resize:vertical"></textarea>
        <textarea class="input" v-model="editItem.artefacts_evidence_links_texts" @keydown="insertBulletOnEnter" placeholder="Evidence / Artefacts / Links" rows="2" style="resize:vertical"></textarea>
        <textarea class="input" v-model="editItem.relevance_career" @keydown="insertBulletOnEnter" placeholder="Relevance to Internship / Career" rows="2" style="resize:vertical"></textarea>
        <label style="font-weight:600">Evidence Files — drag & drop (multiple files supported)</label>
        <FileDropzone
          :accept="fileAccept"
          :multiple="true"
          @selected="onEditFilesSelected"
          @cleared="onEditFilesCleared"
        >
          <template #label>
            <strong>Drag & drop</strong> files here, or <span class="link">click to choose</span>.
            <div v-if="editFiles.length > 0" style="color:#059669; font-size:0.85em; margin-top:6px">
              {{ editFiles.length }} file(s) selected (will replace existing files)
            </div>
            <div v-else style="color:#6b7280; font-size:0.85em; margin-top:6px">
              Leave empty to keep existing files. Select new files to replace all existing files.
            </div>
          </template>
        </FileDropzone>
        <div v-if="editEvidence.length" style="margin-top:8px">
          <div style="font-size:0.85em; color:#6b7280; margin-bottom:4px">Existing Attachments</div>
          <div v-for="(f, idx) in editEvidence" :key="idx" style="margin:4px 8px 0 0; display:inline-flex; align-items:center; gap:6px; padding:6px 10px; border:1px solid var(--border-color); border-radius:6px; background:var(--bg-tertiary)">
            <i class="fas fa-file"></i>
            <span style="font-size:0.9em">{{ f.label }}</span>
            <span style="color:#d1d5db">|</span>
            <button @click="previewEvidenceItem(editTargetId, f)" style="background:none; border:none; color:#2563eb; text-decoration:underline; cursor:pointer; padding:0; font-size:inherit" title="Preview file">
              <i class="fas fa-eye"></i> Preview
            </button>
            <span style="color:#d1d5db">|</span>
            <button @click="downloadEvidenceItem(editTargetId, f)" style="background:none; border:none; color:#2563eb; text-decoration:underline; cursor:pointer; padding:0; font-size:inherit" title="Download file">
              <i class="fas fa-download"></i> Download
            </button>
            <span style="color:#d1d5db">|</span>
            <button @click="removeEvidenceItem(editTargetId, f, true)" style="background:none; border:none; color:#ef4444; text-decoration:underline; cursor:pointer; padding:0; font-size:inherit" title="Remove file">
              <i class="fas fa-times"></i> Remove
            </button>
          </div>
        </div>
        <div style="display:flex; gap:8px">
          <button class="btn" @click="performEdit"><i class="fas fa-save"></i> Save</button>
          <button class="btn secondary" @click="closeEdit"><i class="fas fa-times"></i> Cancel</button>
        </div>
      </div>
      <p v-if="error" style="color:#fca5a5; margin-top:8px">{{ error }}</p>
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
import { apiGet, postEPortfolio, deleteEPortfolio, putEPortfolio, uploadEPortfolioFiles, clearEPortfolioFile, deleteEPortfolioFile, listEPortfolioFiles } from '../lib/api.js'
import { isAuthed as authIsAuthed } from '../lib/auth.js'
import Modal from '../components/Modal.vue'
import ConfirmModal from '../components/ConfirmModal.vue'
import DatePicker from '../components/DatePicker.vue'
import FileDropzone from '../components/FileDropzone.vue'
import { formatDate } from '../lib/date.js'

const items = ref([])
const loading = ref(true)
const error = ref('')
const isAuthed = authIsAuthed
const newItem = ref({
  activity_name: '',
  activity_type: '',
  start_date: '',
  finish_date: '',
  organisation_module: '',
  description: '',
  what_i_did: '',
  skills_tools_acquired: '',
  takeaways: '',
  artefacts_evidence_links_texts: '',
  relevance_career: ''
})
const editItem = ref({
  activity_name: '',
  activity_type: '',
  start_date: '',
  finish_date: '',
  organisation_module: '',
  description: '',
  what_i_did: '',
  skills_tools_acquired: '',
  takeaways: '',
  artefacts_evidence_links_texts: '',
  relevance_career: ''
})
const newFiles = ref([])
const editFiles = ref([])
const editEvidence = ref([])
const fileAccept = [
  'application/pdf',
  'image/*',
  'text/*',
  'text/csv',
  'application/csv',
  // Excel MIME types and extensions
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', // .xlsx
  'application/vnd.ms-excel', // legacy .xls
  'application/vnd.ms-excel.sheet.macroEnabled.12', // .xlsm
  '.xlsx', '.xls', '.xlsm', '.csv'
].join(',')
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
    const created = await postEPortfolio(newItem.value)
    const createdId = created?.data?.[0]?.id
    if(createdId && newFiles.value.length > 0){
      await uploadEPortfolioFiles(createdId, newFiles.value)
    }
    newItem.value = {
      activity_name: '',
      activity_type: '',
      start_date: '',
      finish_date: '',
      organisation_module: '',
      description: '',
      what_i_did: '',
      skills_tools_acquired: '',
      takeaways: '',
      artefacts_evidence_links_texts: '',
      relevance_career: ''
    }
    newFiles.value = []
    await refresh()
    showAdd.value = false
  }catch(e){ error.value = e?.message || 'Add failed' }
}

async function startEdit(p){
  editItem.value = {
    activity_name: p.activity_name || '',
    activity_type: p.activity_type || '',
    start_date: p.start_date || '',
    finish_date: p.finish_date || '',
    organisation_module: p.organisation_module || '',
    description: p.description || '',
    what_i_did: p.what_i_did || '',
    skills_tools_acquired: p.skills_tools_acquired || '',
    takeaways: p.takeaways || '',
    artefacts_evidence_links_texts: p.artefacts_evidence_links_texts || '',
    relevance_career: p.relevance_career || ''
  }
  editTargetId = p.id
  showEdit.value = true
  try{
    const response = await listEPortfolioFiles(editTargetId)
    // Backend returns { items: [{source: 'bytea', index: 0}, {source: 'url', url: '...'}, ...] }
    const items = response?.items || []
    let urlCounter = 0
    editEvidence.value = items.map((item) => {
      if (item.source === 'bytea') {
        return { source: 'bytea', index: item.index, label: `File ${item.index + 1}` }
      } else {
        const label = `Link ${++urlCounter}`
        return { source: 'url', url: item.url, index: items.filter(i => i.source === 'url').indexOf(item), label }
      }
    })
  }catch(e){ 
    console.error('Failed to list files:', e)
    editEvidence.value = [] 
  }
}
function closeAdd(){ showAdd.value = false }
function closeEdit(){ showEdit.value = false; editTargetId = null }
async function performEdit(){
  error.value = ''
  try{
    await putEPortfolio(editTargetId, editItem.value)
    if(editFiles.value.length > 0){
      await uploadEPortfolioFiles(editTargetId, editFiles.value)
    }
    editFiles.value = []
    closeEdit()
    await refresh()
  }catch(err){ error.value = err?.message || 'Update failed' }
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

function onNewFilesSelected(files){ newFiles.value = Array.isArray(files) ? files : [files] }
function onNewFilesCleared(){ newFiles.value = [] }
function onEditFilesSelected(files){ editFiles.value = Array.isArray(files) ? files : [files] }
function onEditFilesCleared(){ editFiles.value = [] }

function evidenceList(item){
  const list = []
  const files = item?.artefacts_evidence_files
  if (typeof files === 'string' && files){
    list.push({ source:'bytea', index:0, label:'File 1' })
  } else if (Array.isArray(files)){
    files.forEach((_, i) => list.push({ source:'bytea', index:i, label:`File ${i+1}` }))
  }
  const links = (item?.artefacts_evidence_links_texts || '').split('\n').map(s => s.trim()).filter(Boolean)
  links.forEach((u, i) => list.push({ source:'url', url:u, index:i, label:`Link ${i+1}` }))
  return list
}

function previewEvidenceItem(itemId, f){
  if (f.source === 'url') { window.open(f.url, '_blank'); return }
  const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
  window.open(`${API_URL}/api/e-portfolio/${itemId}/preview/${f.index}`, '_blank')
}
function downloadEvidenceItem(itemId, f){
  if (f.source === 'url') {
    const a = document.createElement('a'); a.href = f.url; a.download = ''; document.body.appendChild(a); a.click(); document.body.removeChild(a); return
  }
  const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
  const a = document.createElement('a'); a.href = `${API_URL}/api/e-portfolio/${itemId}/download/${f.index}`; a.download = `evidence_${itemId}_${f.index}`; document.body.appendChild(a); a.click(); document.body.removeChild(a)
}
async function removeEvidenceItem(itemId, f, inEditModal=false){
  try{
    await deleteEPortfolioFile(itemId, f.index ?? 0, f.source)
    if(inEditModal){
      try{
        const response = await listEPortfolioFiles(itemId)
        // Backend returns { items: [{source: 'bytea', index: 0}, {source: 'url', url: '...'}, ...] }
        const items = response?.items || []
        let urlCounter = 0
        editEvidence.value = items.map((item) => {
          if (item.source === 'bytea') {
            return { source: 'bytea', index: item.index, label: `File ${item.index + 1}` }
          } else {
            const label = `Link ${++urlCounter}`
            return { source: 'url', url: item.url, index: items.filter(i => i.source === 'url').indexOf(item), label }
          }
        })
      }catch(e){ 
        console.error('Failed to refresh files:', e)
        editEvidence.value = [] 
      }
      await refresh()
    } else {
      await refresh()
    }
  }catch(e){
    alert(e?.message || 'Remove failed')
  }
}

// Upload occurs as part of Save in add/edit flows

function insertBulletOnEnter(event){
  if(event.key === 'Enter'){
    if(event.shiftKey){
      // Allow Shift+Enter to insert a plain newline without bullet
      return
    }
    event.preventDefault()
    const textarea = event.target
    const start = textarea.selectionStart
    const val = textarea.value
    const before = val.slice(0, start)
    const after = val.slice(start)
    const lines = before.split('\n')
    const currentLine = lines[lines.length - 1]
    const bullet = (before.trim() === '' || currentLine.trim() === '') ? '• ' : '\n• '
    textarea.value = before + bullet + after
    const newPos = start + bullet.length
    textarea.selectionStart = textarea.selectionEnd = newPos
    textarea.dispatchEvent(new Event('input', { bubbles: true }))
  }
}
</script>
