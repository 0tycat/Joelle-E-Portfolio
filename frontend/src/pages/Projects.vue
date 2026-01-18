<template>
  <section>
    <!-- Academic Projects Section -->
    <h2 style="margin-top:0">Academic Projects:</h2>
    <div v-if="isAuthed" style="margin-bottom:16px">
      <button class="btn" @click="showAddModule=true"><i class="fas fa-plus"></i> Add Academic Project</button>
    </div>
    <div v-if="loadingModule" style="padding:20px; text-align:center">Loading...</div>
    <div v-else style="display:flex; flex-direction:column; gap:16px; margin-bottom:32px">
      <div v-for="p in filteredAndSortedModule" :key="p.id" class="project-card" style="position:relative">
        <div v-if="isAuthed" class="card-actions">
          <button class="btn-icon secondary" @click="startEditModule(p)" title="Edit"><i class="fas fa-edit"></i></button>
          <button class="btn-icon danger" @click="askRemoveModule(p)" title="Delete"><i class="fas fa-trash"></i></button>
        </div>
        <div class="project-media">
          <div class="media-placeholder">
            {{ p.video_demo ? 'video of demo' : 'project demo' }}
          </div>
        </div>
        <div class="project-content">
          <div style="flex:1">
            <h3 style="margin:0 0 8px 0">{{ p.project_name }}</h3>
            <div v-if="p.start_date || p.end_date" style="margin-bottom:12px; font-size:0.9em; color:var(--text-secondary)">
              Start-end dates: {{ formatDate(p.start_date) }}{{ p.end_date ? ` - ${formatDate(p.end_date)}` : '' }}
            </div>
            <div v-if="p.description" style="margin-bottom:12px">
              <strong>Description:</strong>
              <p style="white-space:pre-wrap; margin:4px 0 0 0">{{ p.description }}</p>
            </div>
            <div v-if="p.takeaways" style="margin-bottom:12px">
              <strong>Takeaways:</strong>
              <p style="white-space:pre-wrap; margin:4px 0 0 0">{{ p.takeaways }}</p>
            </div>
            <div v-if="p.skills_applied" style="margin-bottom:12px">
              <strong>Skills applied:</strong>
              <p style="white-space:pre-wrap; margin:4px 0 0 0">{{ p.skills_applied }}</p>
            </div>
            <!-- Project Files -->
            <div v-if="hasFiles(p)" style="margin-bottom:12px">
              <strong>Attached Files:</strong>
              <div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:8px">
                <a v-for="(file, idx) in getProjectFiles(p)" :key="idx" 
                   :href="getFileDownloadUrl('projects', p.id, idx)" 
                   target="_blank"
                   class="file-badge"
                   :title="`Download file ${idx + 1}`">
                  <i class="fas fa-file"></i> File {{ idx + 1 }}
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="filteredAndSortedModule.length === 0" style="text-align:center; color:var(--text-secondary); padding:20px">
        No academic projects yet
      </div>
    </div>

    <!-- Community Projects Section -->
    <h2>Community Projects:</h2>
    <div v-if="isAuthed" style="margin-bottom:16px">
      <button class="btn" @click="showAddCommunity=true"><i class="fas fa-plus"></i> Add Community Project</button>
    </div>
    <div v-if="loadingCommunity" style="padding:20px; text-align:center">Loading...</div>
    <div v-else style="display:flex; flex-direction:column; gap:16px">
      <div v-for="c in filteredAndSortedCommunity" :key="c.id" class="project-card" style="position:relative">
        <div v-if="isAuthed" class="card-actions">
          <button class="btn-icon secondary" @click="startEditCommunity(c)" title="Edit"><i class="fas fa-edit"></i></button>
          <button class="btn-icon danger" @click="askRemoveCommunity(c)" title="Delete"><i class="fas fa-trash"></i></button>
        </div>
        <div class="project-media">
          <div class="media-placeholder">
            Image of Institute Badge
          </div>
        </div>
        <div class="project-content">
          <div style="flex:1">
            <h3 style="margin:0 0 8px 0">{{ c.programme_name }}</h3>
            <div v-if="c.start_date || c.end_date" style="margin-bottom:12px; font-size:0.9em; color:var(--text-secondary)">
              Start-end dates: {{ formatDate(c.start_date) }}{{ c.end_date ? ` - ${formatDate(c.end_date)}` : '' }}
            </div>
            <div v-if="c.role" style="margin-bottom:12px">
              <strong>Role:</strong> {{ c.role }}
            </div>
            <div v-if="c.description" style="margin-bottom:12px">
              <strong>Description:</strong>
              <p style="white-space:pre-wrap; margin:4px 0 0 0">{{ c.description }}</p>
            </div>
            <!-- Community Files -->
            <div v-if="hasFiles(c)" style="margin-bottom:12px">
              <strong>Attached Files:</strong>
              <div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:8px">
                <a v-for="(file, idx) in getProjectFiles(c)" :key="idx" 
                   :href="getFileDownloadUrl('community', c.id, idx)" 
                   target="_blank"
                   class="file-badge"
                   :title="`Download file ${idx + 1}`">
                  <i class="fas fa-file"></i> File {{ idx + 1 }}
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="filteredAndSortedCommunity.length === 0" style="text-align:center; color:var(--text-secondary); padding:20px">
        No community projects yet
      </div>
    </div>

    <!-- Add Academic Modal -->
    <Modal :open="showAddModule" title="Add Academic Project" @close="closeAddModule">
      <div style="display:flex; gap:8px; flex-direction:column">
        <input class="input" v-model="newModule.project_name" placeholder="Project name" />
        <div style="display:flex; gap:8px">
          <DatePicker v-model="newModule.start_date" placeholder="Start (YYYY-MM-DD)" />
          <DatePicker v-model="newModule.end_date" placeholder="End (YYYY-MM-DD)" />
        </div>
        <textarea class="input" v-model="newModule.description" @keydown="handleDescriptionKeydown($event, newModule)" placeholder="Description" rows="3" style="resize:vertical"></textarea>
        <textarea class="input" v-model="newModule.takeaways" placeholder="Takeaways" rows="3" style="resize:vertical"></textarea>
        <textarea class="input" v-model="newModule.skills_applied" placeholder="Skills Applied" rows="3" style="resize:vertical"></textarea>
        
        <label style="font-weight:600; margin-top:8px">Project Files (optional)</label>
        <FileDropzone
          accept="*"
          multiple
          @selected="onNewModuleFilesSelected"
          @cleared="onNewModuleFilesCleared"
        >
          <template #label>
            <span>Drop files here or click to upload</span>
          </template>
        </FileDropzone>
        <div v-if="newModuleFiles.length > 0" style="margin-top:8px">
          <div v-for="(file, idx) in newModuleFiles" :key="idx" style="display:flex; align-items:center; gap:8px; padding:4px 0">
            <i class="fas fa-file"></i>
            <span style="flex:1">{{ file.name }}</span>
            <button class="btn-icon danger" @click="removeNewModuleFile(idx)" title="Remove"><i class="fas fa-times"></i></button>
          </div>
        </div>
        
        <div style="display:flex; gap:8px">
          <button class="btn" @click="addModule"><i class="fas fa-save"></i> Save</button>
          <button class="btn secondary" @click="closeAddModule"><i class="fas fa-times"></i> Cancel</button>
        </div>
      </div>
      <p v-if="errorModule" style="color:#fca5a5">{{ errorModule }}</p>
    </Modal>

    <!-- Edit Academic Modal -->
    <Modal :open="showEditModule" title="Edit Academic Project" @close="closeEditModule">
      <div style="display:flex; gap:8px; flex-direction:column">
        <input class="input" v-model="editModule.project_name" placeholder="Project name" />
        <div style="display:flex; gap:8px">
          <DatePicker v-model="editModule.start_date" placeholder="Start (YYYY-MM-DD)" />
          <DatePicker v-model="editModule.end_date" placeholder="End (YYYY-MM-DD)" />
        </div>
        <textarea class="input" v-model="editModule.description" @keydown="handleDescriptionKeydown($event, editModule)" placeholder="Description" rows="3" style="resize:vertical"></textarea>
        <textarea class="input" v-model="editModule.takeaways" placeholder="Takeaways" rows="3" style="resize:vertical"></textarea>
        <textarea class="input" v-model="editModule.skills_applied" placeholder="Skills Applied" rows="3" style="resize:vertical"></textarea>
        
        <!-- Existing Files -->
        <div v-if="editModuleExistingFiles.length > 0" style="margin-top:8px">
          <label style="font-weight:600">Existing Files:</label>
          <div v-for="(file, idx) in editModuleExistingFiles" :key="idx" style="display:flex; align-items:center; gap:8px; padding:4px 0">
            <i class="fas fa-file"></i>
            <span style="flex:1">File {{ idx + 1 }}</span>
            <button class="btn-icon danger" @click="removeExistingModuleFile(idx)" title="Remove"><i class="fas fa-trash"></i></button>
          </div>
        </div>
        
        <label style="font-weight:600; margin-top:8px">Add New Files (optional)</label>
        <FileDropzone
          accept="*"
          multiple
          @selected="onEditModuleFilesSelected"
          @cleared="onEditModuleFilesCleared"
        >
          <template #label>
            <span>Drop files here or click to upload</span>
          </template>
        </FileDropzone>
        <div v-if="editModuleFiles.length > 0" style="margin-top:8px">
          <div v-for="(file, idx) in editModuleFiles" :key="idx" style="display:flex; align-items:center; gap:8px; padding:4px 0">
            <i class="fas fa-file"></i>
            <span style="flex:1">{{ file.name }}</span>
            <button class="btn-icon danger" @click="removeEditModuleFile(idx)" title="Remove"><i class="fas fa-times"></i></button>
          </div>
        </div>
        
        <div style="display:flex; gap:8px">
          <button class="btn" @click="performEditModule"><i class="fas fa-save"></i> Save</button>
          <button class="btn secondary" @click="closeEditModule"><i class="fas fa-times"></i> Cancel</button>
        </div>
      </div>
      <p v-if="errorModule" style="color:#fca5a5">{{ errorModule }}</p>
    </Modal>

    <!-- Add Community Modal -->
    <Modal :open="showAddCommunity" title="Add Community Project" @close="closeAddCommunity">
      <div style="display:flex; gap:8px; flex-direction:column">
        <input class="input" v-model="newCommunity.programme_name" placeholder="Programme Name" />
        <input class="input" v-model="newCommunity.role" placeholder="Role" />
        <div style="display:flex; gap:8px">
          <DatePicker v-model="newCommunity.start_date" placeholder="Start (YYYY-MM-DD)" />
          <DatePicker v-model="newCommunity.end_date" placeholder="End (YYYY-MM-DD)" />
        </div>
        <textarea class="input" v-model="newCommunity.description" @keydown="handleDescriptionKeydown($event, newCommunity)" placeholder="Description" rows="5" style="resize:vertical"></textarea>
        
        <label style="font-weight:600; margin-top:8px">Project Files (optional)</label>
        <FileDropzone
          accept="*"
          multiple
          @selected="onNewCommunityFilesSelected"
          @cleared="onNewCommunityFilesCleared"
        >
          <template #label>
            <span>Drop files here or click to upload</span>
          </template>
        </FileDropzone>
        <div v-if="newCommunityFiles.length > 0" style="margin-top:8px">
          <div v-for="(file, idx) in newCommunityFiles" :key="idx" style="display:flex; align-items:center; gap:8px; padding:4px 0">
            <i class="fas fa-file"></i>
            <span style="flex:1">{{ file.name }}</span>
            <button class="btn-icon danger" @click="removeNewCommunityFile(idx)" title="Remove"><i class="fas fa-times"></i></button>
          </div>
        </div>
        
        <div style="display:flex; gap:8px">
          <button class="btn" @click="addCommunity"><i class="fas fa-save"></i> Save</button>
          <button class="btn secondary" @click="closeAddCommunity"><i class="fas fa-times"></i> Cancel</button>
        </div>
      </div>
      <p v-if="errorCommunity" style="color:#fca5a5">{{ errorCommunity }}</p>
    </Modal>

    <!-- Edit Community Modal -->
    <Modal :open="showEditCommunity" title="Edit Community Project" @close="closeEditCommunity">
      <div style="display:flex; gap:8px; flex-direction:column">
        <input class="input" v-model="editCommunity.programme_name" placeholder="Programme Name" />
        <input class="input" v-model="editCommunity.role" placeholder="Role" />
        <div style="display:flex; gap:8px">
          <DatePicker v-model="editCommunity.start_date" placeholder="Start (YYYY-MM-DD)" />
          <DatePicker v-model="editCommunity.end_date" placeholder="End (YYYY-MM-DD)" />
        </div>
        <textarea class="input" v-model="editCommunity.description" @keydown="handleDescriptionKeydown($event, editCommunity)" placeholder="Description" rows="5" style="resize:vertical"></textarea>
        
        <!-- Existing Files -->
        <div v-if="editCommunityExistingFiles.length > 0" style="margin-top:8px">
          <label style="font-weight:600">Existing Files:</label>
          <div v-for="(file, idx) in editCommunityExistingFiles" :key="idx" style="display:flex; align-items:center; gap:8px; padding:4px 0">
            <i class="fas fa-file"></i>
            <span style="flex:1">File {{ idx + 1 }}</span>
            <button class="btn-icon danger" @click="removeExistingCommunityFile(idx)" title="Remove"><i class="fas fa-trash"></i></button>
          </div>
        </div>
        
        <label style="font-weight:600; margin-top:8px">Add New Files (optional)</label>
        <FileDropzone
          accept="*"
          multiple
          @selected="onEditCommunityFilesSelected"
          @cleared="onEditCommunityFilesCleared"
        >
          <template #label>
            <span>Drop files here or click to upload</span>
          </template>
        </FileDropzone>
        <div v-if="editCommunityFiles.length > 0" style="margin-top:8px">
          <div v-for="(file, idx) in editCommunityFiles" :key="idx" style="display:flex; align-items:center; gap:8px; padding:4px 0">
            <i class="fas fa-file"></i>
            <span style="flex:1">{{ file.name }}</span>
            <button class="btn-icon danger" @click="removeEditCommunityFile(idx)" title="Remove"><i class="fas fa-times"></i></button>
          </div>
        </div>
        
        <div style="display:flex; gap:8px">
          <button class="btn" @click="performEditCommunity"><i class="fas fa-save"></i> Save</button>
          <button class="btn secondary" @click="closeEditCommunity"><i class="fas fa-times"></i> Cancel</button>
        </div>
      </div>
      <p v-if="errorCommunity" style="color:#fca5a5">{{ errorCommunity }}</p>
    </Modal>

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

<style scoped>
.project-card {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 8px;
}

.project-media {
  flex-shrink: 0;
  width: 180px;
  height: 140px;
}

.media-placeholder {
  width: 100%;
  height: 100%;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 8px;
  color: var(--text-secondary);
  background: var(--bg-color);
  font-size: 0.9em;
}

.project-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-width: 0;
}

.project-content h3 {
  color: var(--text-primary);
}

.project-content strong {
  color: var(--text-primary);
}

@media (max-width: 768px) {
  .project-card {
    flex-direction: column;
  }
  
  .project-media {
    width: 100%;
    height: 160px;
  }
}

.file-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: var(--primary-color);
  color: white;
  border-radius: 4px;
  text-decoration: none;
  font-size: 0.9em;
  transition: background 0.2s;
}

.file-badge:hover {
  background: var(--primary-hover);
}
</style>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { apiGet, postProject, deleteProject, putProject, postCommunity, putCommunity, deleteCommunity } from '../lib/api.js'
import { isAuthed as authIsAuthed } from '../lib/auth.js'
import Modal from '../components/Modal.vue'
import ConfirmModal from '../components/ConfirmModal.vue'
import DatePicker from '../components/DatePicker.vue'
import FileDropzone from '../components/FileDropzone.vue'
import { formatDate } from '../lib/date.js'

const isAuthed = authIsAuthed
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

// Community Service State
const community = ref([])
const loadingCommunity = ref(true)
const errorCommunity = ref('')
const newCommunity = ref({ programme_name:'', role:'', start_date:'', end_date:'', description:'' })
const editCommunity = ref({ programme_name:'', role:'', start_date:'', end_date:'', description:'' })
const showAddCommunity = ref(false)
const showEditCommunity = ref(false)
let editTargetCommunityId = null
const newCommunityFiles = ref([])
const editCommunityFiles = ref([])
const editCommunityExistingFiles = ref([])
const editCommunityFilesToRemove = ref([])

// Module Projects State
const modules = ref([])
const loadingModule = ref(true)
const errorModule = ref('')
const newModule = ref({ project_name:'', description:'', takeaways:'', skills_applied:'', start_date:'', end_date:'', video_demo:'' })
const editModule = ref({ project_name:'', description:'', takeaways:'', skills_applied:'', start_date:'', end_date:'', video_demo:'' })
const showAddModule = ref(false)
const showEditModule = ref(false)
let editTargetModuleId = null
const newModuleFiles = ref([])
const editModuleFiles = ref([])
const editModuleExistingFiles = ref([])
const editModuleFilesToRemove = ref([])

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
const filteredAndSortedCommunity = computed(() => {
  return community.value
})

// Module Computed
const filteredAndSortedModule = computed(() => {
  return modules.value
})

// Community Functions
async function addCommunity(){
  errorCommunity.value = ''
  try{
    const result = await postCommunity(newCommunity.value)
    const communityId = result.data?.[0]?.id
    
    // Upload files if any
    if (communityId && newCommunityFiles.value.length > 0) {
      const formData = new FormData()
      newCommunityFiles.value.forEach(file => {
        formData.append('files', file)
      })
      await fetch(`${API_URL}/api/community/${communityId}/files`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
        body: formData
      })
    }
    
    newCommunity.value = { programme_name:'', role:'', start_date:'', end_date:'', description:'' }
    newCommunityFiles.value = []
    await loadAll()
    showAddCommunity.value = false
  }catch(e){ errorCommunity.value = 'Add failed' }
}

function startEditCommunity(c){
  editCommunity.value = { programme_name:c.programme_name, role:c.role, start_date:c.start_date || '', end_date:c.end_date || '', description:c.description }
  editTargetCommunityId = c.id
  editCommunityFiles.value = []
  editCommunityExistingFiles.value = getProjectFiles(c)
  editCommunityFilesToRemove.value = []
  showEditCommunity.value = true
}

function closeAddCommunity(){ 
  showAddCommunity.value = false
  newCommunityFiles.value = []
}
function closeEditCommunity(){ 
  showEditCommunity.value = false
  editTargetCommunityId = null
  editCommunityFiles.value = []
  editCommunityExistingFiles.value = []
  editCommunityFilesToRemove.value = []
}

async function performEditCommunity(){
  errorCommunity.value = ''
  try{
    await putCommunity(editTargetCommunityId, editCommunity.value)
    
    // Remove files marked for deletion
    for (const index of editCommunityFilesToRemove.value) {
      await fetch(`${API_URL}/api/community/${editTargetCommunityId}/files/${index}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
      })
    }
    
    // Upload new files if any
    if (editCommunityFiles.value.length > 0) {
      const formData = new FormData()
      editCommunityFiles.value.forEach(file => {
        formData.append('files', file)
      })
      await fetch(`${API_URL}/api/community/${editTargetCommunityId}/files`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
        body: formData
      })
    }
    
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

// Module Functions
async function addModule(){
  errorModule.value = ''
  try{
    const result = await postProject(newModule.value)
    const projectId = result.data?.[0]?.id
    
    // Upload files if any
    if (projectId && newModuleFiles.value.length > 0) {
      const formData = new FormData()
      newModuleFiles.value.forEach(file => {
        formData.append('files', file)
      })
      await fetch(`${API_URL}/api/projects/${projectId}/files`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
        body: formData
      })
    }
    
    newModule.value = { project_name:'', description:'', takeaways:'', skills_applied:'', start_date:'', end_date:'', video_demo:'' }
    newModuleFiles.value = []
    await loadAll()
    showAddModule.value = false
  }catch(e){ errorModule.value = 'Add failed' }
}

function startEditModule(p){
  editModule.value = { 
    project_name:p.project_name, 
    description:p.description, 
    takeaways:p.takeaways || '',
    skills_applied:p.skills_applied || '',
    start_date:p.start_date || '',
    end_date:p.end_date || '',
    video_demo:p.video_demo || ''
  }
  editTargetModuleId = p.id
  editModuleFiles.value = []
  editModuleExistingFiles.value = getProjectFiles(p)
  editModuleFilesToRemove.value = []
  showEditModule.value = true
}

function closeAddModule(){ 
  showAddModule.value = false
  newModuleFiles.value = []
}
function closeEditModule(){ 
  showEditModule.value = false
  editTargetModuleId = null
  editModuleFiles.value = []
  editModuleExistingFiles.value = []
  editModuleFilesToRemove.value = []
}

async function performEditModule(){
  errorModule.value = ''
  try{
    await putProject(editTargetModuleId, editModule.value)
    
    // Remove files marked for deletion
    for (const index of editModuleFilesToRemove.value) {
      await fetch(`${API_URL}/api/projects/${editTargetModuleId}/files/${index}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
      })
    }
    
    // Upload new files if any
    if (editModuleFiles.value.length > 0) {
      const formData = new FormData()
      editModuleFiles.value.forEach(file => {
        formData.append('files', file)
      })
      await fetch(`${API_URL}/api/projects/${editTargetModuleId}/files`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
        body: formData
      })
    }
    
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

// File Helper Functions
function hasFiles(item) {
  const files = item?.project_files
  return (typeof files === 'string' && files) || (Array.isArray(files) && files.length > 0)
}

function getProjectFiles(item) {
  const files = item?.project_files
  if (!files) return []
  if (typeof files === 'string') return [files]
  if (Array.isArray(files)) return files
  return []
}

function getFileDownloadUrl(type, id, index) {
  return `${API_URL}/api/${type}/${id}/files/${index}`
}

// Module File Handlers
function onNewModuleFilesSelected(files) {
  newModuleFiles.value = [...newModuleFiles.value, ...files]
}

function onNewModuleFilesCleared() {
  newModuleFiles.value = []
}

function removeNewModuleFile(index) {
  newModuleFiles.value.splice(index, 1)
}

function onEditModuleFilesSelected(files) {
  editModuleFiles.value = [...editModuleFiles.value, ...files]
}

function onEditModuleFilesCleared() {
  editModuleFiles.value = []
}

function removeEditModuleFile(index) {
  editModuleFiles.value.splice(index, 1)
}

function removeExistingModuleFile(index) {
  editModuleFilesToRemove.value.push(index)
  editModuleExistingFiles.value.splice(index, 1)
}

// Community File Handlers
function onNewCommunityFilesSelected(files) {
  newCommunityFiles.value = [...newCommunityFiles.value, ...files]
}

function onNewCommunityFilesCleared() {
  newCommunityFiles.value = []
}

function removeNewCommunityFile(index) {
  newCommunityFiles.value.splice(index, 1)
}

function onEditCommunityFilesSelected(files) {
  editCommunityFiles.value = [...editCommunityFiles.value, ...files]
}

function onEditCommunityFilesCleared() {
  editCommunityFiles.value = []
}

function removeEditCommunityFile(index) {
  editCommunityFiles.value.splice(index, 1)
}

function removeExistingCommunityFile(index) {
  editCommunityFilesToRemove.value.push(index)
  editCommunityExistingFiles.value.splice(index, 1)
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
