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
          <p v-if="item.artefacts_evidence_links_texts" style="white-space:pre-wrap; margin-top:8px"><strong>Evidence/Links:</strong><br/>{{ item.artefacts_evidence_links_texts }}</p>
          <p v-if="item.relevance_career" style="white-space:pre-wrap; margin-top:8px"><strong>Relevance to Career:</strong><br/>{{ item.relevance_career }}</p>
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
        <textarea class="input" v-model="newItem.description" placeholder="Description / Purpose & Context" rows="3" style="resize:vertical"></textarea>
        <textarea class="input" v-model="newItem.what_i_did" placeholder="What I Did" rows="3" style="resize:vertical"></textarea>
        <textarea class="input" v-model="newItem.skills_tools_acquired" placeholder="Skills & Tools Applied/Acquired" rows="3" style="resize:vertical"></textarea>
        <textarea class="input" v-model="newItem.takeaways" placeholder="What I Learned / Key Takeaways" rows="3" style="resize:vertical"></textarea>
        <textarea class="input" v-model="newItem.artefacts_evidence_links_texts" placeholder="Evidence / Artefacts / Links" rows="2" style="resize:vertical"></textarea>
        <textarea class="input" v-model="newItem.relevance_career" placeholder="Relevance to Internship / Career" rows="2" style="resize:vertical"></textarea>
        <label style="font-weight:600">Upload evidence (optional)</label>
        <input type="file" @change="handleNewFileChange" />
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
        <textarea class="input" v-model="editItem.description" placeholder="Description / Purpose & Context" rows="3" style="resize:vertical"></textarea>
        <textarea class="input" v-model="editItem.what_i_did" placeholder="What I Did" rows="3" style="resize:vertical"></textarea>
        <textarea class="input" v-model="editItem.skills_tools_acquired" placeholder="Skills & Tools Applied/Acquired" rows="3" style="resize:vertical"></textarea>
        <textarea class="input" v-model="editItem.takeaways" placeholder="What I Learned / Key Takeaways" rows="3" style="resize:vertical"></textarea>
        <textarea class="input" v-model="editItem.artefacts_evidence_links_texts" placeholder="Evidence / Artefacts / Links" rows="2" style="resize:vertical"></textarea>
        <textarea class="input" v-model="editItem.relevance_career" placeholder="Relevance to Internship / Career" rows="2" style="resize:vertical"></textarea>
        <label style="font-weight:600">Upload evidence (optional)</label>
        <input type="file" @change="handleEditFileChange" />
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
import { apiGet, postEPortfolio, deleteEPortfolio, putEPortfolio, uploadEPortfolioFile, clearEPortfolioFile } from '../lib/api.js'
import { isAuthed as authIsAuthed } from '../lib/auth.js'
import Modal from '../components/Modal.vue'
import ConfirmModal from '../components/ConfirmModal.vue'
import DatePicker from '../components/DatePicker.vue'
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
const newFile = ref(null)
const editFile = ref(null)
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
    if(createdId && newFile.value){
      await uploadEPortfolioFile(createdId, newFile.value)
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
    newFile.value = null
    await refresh()
    showAdd.value = false
  }catch(e){ error.value = 'Add failed' }
}

function startEdit(p){
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
}
function closeAdd(){ showAdd.value = false }
function closeEdit(){ showEdit.value = false; editTargetId = null }
async function performEdit(){
  error.value = ''
  try{
    await putEPortfolio(editTargetId, editItem.value)
    if(editFile.value){
      await uploadEPortfolioFile(editTargetId, editFile.value)
    }
    editFile.value = null
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

function handleNewFileChange(event){
  const files = event.target.files
  newFile.value = files && files[0] ? files[0] : null
}

function handleEditFileChange(event){
  const files = event.target.files
  editFile.value = files && files[0] ? files[0] : null
}
</script>
