<template>
  <section>
    <h2>Education</h2>
    <div v-if="isAuthed" style="margin-bottom:12px">
      <button class="btn" @click="showAdd=true">Add Education</button>
    </div>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-for="e in education" :key="e.id" class="card">
        <strong>{{ e.institute_name }}</strong>
        <div>{{ e.certification }}</div>
        <div>{{ e.start_date }} - {{ e.finish_date }}</div>
        <div v-if="isAuthed" style="margin-top:8px; display:flex; gap:8px">
          <button class="btn secondary" @click="startEdit(e)">Edit</button>
          <button class="btn danger" @click="askRemoveEducation(e)">Delete</button>
        </div>
      </div>
    </div>

    <!-- Add Modal -->
    <Modal :open="showAdd" title="Add Education" @close="closeAdd">
      <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap">
        <input class="input" v-model="newItem.institute_name" placeholder="Institute" />
        <input class="input" v-model="newItem.certification" placeholder="Certification" />
        <input class="input" v-model="newItem.start_date" placeholder="Start (YYYY-MM-DD)" />
        <input class="input" v-model="newItem.finish_date" placeholder="Finish (YYYY-MM-DD)" />
        <button class="btn" @click="addEducation">Save</button>
        <button class="btn secondary" @click="closeAdd">Cancel</button>
      </div>
      <p v-if="error" style="color:#fca5a5">{{ error }}</p>
    </Modal>

    <!-- Edit Modal -->
    <Modal :open="showEdit" title="Edit Education" @close="closeEdit">
      <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap">
        <input class="input" v-model="editItem.institute_name" placeholder="Institute" />
        <input class="input" v-model="editItem.certification" placeholder="Certification" />
        <input class="input" v-model="editItem.start_date" placeholder="Start (YYYY-MM-DD)" />
        <input class="input" v-model="editItem.finish_date" placeholder="Finish (YYYY-MM-DD)" />
        <button class="btn" @click="performEdit">Save</button>
        <button class="btn secondary" @click="closeEdit">Cancel</button>
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
import { apiGet, postEducation, deleteEducation, putEducation } from '../lib/api.js'
import { isAuthed as authIsAuthed } from '../lib/auth.js'
import Modal from '../components/Modal.vue'
import ConfirmModal from '../components/ConfirmModal.vue'

const education = ref([])
const loading = ref(true)
const error = ref('')
const isAuthed = authIsAuthed
const newItem = ref({ institute_name:'', certification:'', start_date:'', finish_date:'' })
const editItem = ref({ institute_name:'', certification:'', start_date:'', finish_date:'' })
const showAdd = ref(false)
const showEdit = ref(false)
let editTargetId = null
const showConfirm = ref(false)
let deleteTargetId = null
const deleteItemLabel = ref('')
const confirmMessage = computed(() => `Delete "${deleteItemLabel.value}"? This cannot be undone.`)

async function refresh(){
  try{
    education.value = await apiGet('/api/education')
  } finally {
    loading.value = false
  }
}
onMounted(refresh)

async function addEducation(){
  error.value = ''
  try{
    await postEducation(newItem.value)
    newItem.value = { institute_name:'', certification:'', start_date:'', finish_date:'' }
    await refresh()
    showAdd.value = false
  }catch(e){ error.value = 'Add failed' }
}

function startEdit(e){
  editItem.value = { institute_name:e.institute_name, certification:e.certification, start_date:e.start_date, finish_date:e.finish_date }
  editTargetId = e.id
  showEdit.value = true
}
function closeAdd(){ showAdd.value = false }
function closeEdit(){ showEdit.value = false; editTargetId = null }
async function performEdit(){
  error.value = ''
  try{
    await putEducation(editTargetId, editItem.value)
    closeEdit()
    await refresh()
  }catch(err){ error.value = 'Update failed' }
}

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
