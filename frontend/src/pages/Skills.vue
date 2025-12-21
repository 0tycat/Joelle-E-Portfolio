<template>
  <section>
    <h2>Skills</h2>
    <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-bottom:12px">
      <div v-if="isAuthed">
        <button class="btn" @click="showAdd=true"><i class="fas fa-plus"></i> Add Skill</button>
      </div>
      <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center">
        <div style="position:relative">
          <button class="btn secondary" @click="toggleFilter"><i class="fas fa-filter"></i> Filter</button>
          <div v-if="filterOpen" class="card" style="position:absolute; top:110%; left:0; min-width:240px; z-index:10; padding:10px; display:flex; flex-direction:column; gap:8px">
            <strong>Proficiency</strong>
            <small style="color:#6b7280">Checked levels are hidden</small>
            <label v-for="lvl in profLevels" :key="lvl.id" style="display:flex; align-items:center; gap:6px">
              <input type="checkbox" v-model="activeLevels" :value="String(lvl.id)" />
              <span>{{ lvl.level }}</span>
            </label>
            <button class="btn secondary" style="padding:6px 10px; align-self:flex-start" @click="clearFilters"><i class="fas fa-undo"></i> Clear</button>
          </div>
        </div>
        <div style="position:relative">
          <button class="btn secondary" @click="toggleSort"><i class="fas fa-sort"></i> Sort: {{ sortLabel }}</button>
          <div v-if="sortOpen" class="card" style="position:absolute; top:110%; left:0; min-width:200px; z-index:10; padding:10px; display:flex; flex-direction:column; gap:6px">
            <button class="btn secondary" :class="{active: sortMode==='alpha-asc'}" @click="setSortAndClose('alpha-asc')">A → Z</button>
            <button class="btn secondary" :class="{active: sortMode==='alpha-desc'}" @click="setSortAndClose('alpha-desc')">Z → A</button>
            <button class="btn secondary" :class="{active: sortMode==='prof-asc'}" @click="setSortAndClose('prof-asc')">Proficiency ↑</button>
            <button class="btn secondary" :class="{active: sortMode==='prof-desc'}" @click="setSortAndClose('prof-desc')">Proficiency ↓</button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-for="s in filteredAndSorted" :key="s.id" class="card">
        <strong>{{ s.skill_name }}</strong>
        <div>Proficiency: {{ s.proficiency_label ? s.proficiency_label : s.proficiency }}</div>
        <div v-if="isAuthed" style="margin-top:8px; display:flex; gap:8px">
          <button class="btn secondary" @click="startEdit(s)"><i class="fas fa-edit"></i> Edit</button>
          <button class="btn danger" @click="askRemoveSkill(s)"><i class="fas fa-trash"></i> Delete</button>
        </div>
      </div>
    </div>

    <!-- Add Modal -->
    <Modal :open="showAdd" title="Add Skill" @close="closeAdd">
      <div style="display:flex; gap:8px; flex-direction:column">
        <input class="input" v-model="newSkill.skill_name" placeholder="Skill name" />
        <select class="input" v-model="newSkill.proficiency">
          <option disabled value="">Select proficiency level</option>
          <option v-for="lvl in profLevels" :key="lvl.id" :value="String(lvl.id)">{{ lvl.level }}</option>
        </select>
        <div style="display:flex; gap:8px">
          <button class="btn" @click="addSkill"><i class="fas fa-save"></i> Save</button>
          <button class="btn secondary" @click="closeAdd"><i class="fas fa-times"></i> Cancel</button>
        </div>
      </div>
      <p v-if="error" style="color:#fca5a5">{{ error }}</p>
    </Modal>

    <!-- Edit Modal -->
    <Modal :open="showEdit" title="Edit Skill" @close="closeEdit">
      <div style="display:flex; gap:8px; flex-direction:column">
        <input class="input" v-model="editSkill.skill_name" />
        <select class="input" v-model="editSkill.proficiency">
          <option disabled value="">Select proficiency level</option>
          <option v-for="lvl in profLevels" :key="lvl.id" :value="String(lvl.id)">{{ lvl.level }}</option>
        </select>
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
      title="Delete Skill"
      :message="confirmMessage"
      @confirm="performDelete"
      @close="closeConfirm"
    />
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { apiGet, postSkill, putSkill, deleteSkill, getProfLevels } from '../lib/api.js'
import { isAuthed } from '../lib/auth.js'
import Modal from '../components/Modal.vue'
import ConfirmModal from '../components/ConfirmModal.vue'

const skills = ref([])
const loading = ref(true)
const error = ref('')
const profLevels = ref([])
const activeLevels = ref([])
const sortMode = ref('alpha-asc')
const filterOpen = ref(false)
const sortOpen = ref(false)
const newSkill = ref({ skill_name:'', proficiency:'' })
const editingId = ref(null)
const editSkill = ref({ skill_name:'', proficiency:'' })
const showAdd = ref(false)
const showEdit = ref(false)
let editTargetId = null
const showConfirm = ref(false)
let deleteTargetId = null
const deleteItemLabel = ref('')
const confirmMessage = computed(() => `Delete "${deleteItemLabel.value}"? This cannot be undone.`)

async function refresh(){
  try{
    const [levels, skillsData] = await Promise.all([
      getProfLevels().catch(() => []),
      apiGet('/api/skills')
    ])
    profLevels.value = Array.isArray(levels) ? levels : []
    skills.value = skillsData
  } finally {
    loading.value = false
  }
}
onMounted(refresh)

const filteredAndSorted = computed(() => {
  const byLevel = activeLevels.value.length
    ? skills.value.filter(s => !activeLevels.value.includes(String(s.proficiency)))
    : skills.value

  const labelFor = lvlId => profLevels.value.find(l => String(l.id) === String(lvlId))?.level || ''

  return [...byLevel].sort((a,b) => {
    if(sortMode.value === 'alpha-asc') return a.skill_name.localeCompare(b.skill_name)
    if(sortMode.value === 'alpha-desc') return b.skill_name.localeCompare(a.skill_name)
    const aVal = Number(a.proficiency)
    const bVal = Number(b.proficiency)
    if(sortMode.value === 'prof-asc') return aVal - bVal || labelFor(aVal).localeCompare(labelFor(bVal))
    if(sortMode.value === 'prof-desc') return bVal - aVal || labelFor(bVal).localeCompare(labelFor(aVal))
    return 0
  })
})

function setSort(mode){
  sortMode.value = mode
}
function setSortAndClose(mode){
  setSort(mode)
  sortOpen.value = false
}
function clearFilters(){
  activeLevels.value = []
}
function toggleFilter(){
  filterOpen.value = !filterOpen.value
  if(filterOpen.value){
    sortOpen.value = false
  }
}
function toggleSort(){
  sortOpen.value = !sortOpen.value
  if(sortOpen.value){
    filterOpen.value = false
  }
}
const sortLabel = computed(() => {
  if(sortMode.value === 'alpha-asc') return 'A → Z'
  if(sortMode.value === 'alpha-desc') return 'Z → A'
  if(sortMode.value === 'prof-asc') return 'Proficiency ↑'
  if(sortMode.value === 'prof-desc') return 'Proficiency ↓'
  return 'Choose'
})

async function addSkill(){
  error.value = ''
  try{
    if(!newSkill.value.skill_name || !newSkill.value.proficiency){
      error.value = 'Provide skill name and proficiency'
      return
    }
    await postSkill({
      skill_name: newSkill.value.skill_name,
      proficiency: Number(newSkill.value.proficiency)
    })
    newSkill.value = { skill_name:'', proficiency:'' }
    await refresh()
    showAdd.value = false
  }catch(e){ error.value = 'Add failed' }
}

function startEdit(s){
  editSkill.value = { skill_name: s.skill_name, proficiency: s.proficiency }
  editTargetId = s.id
  showEdit.value = true
}
function closeAdd(){ showAdd.value = false }
function closeEdit(){ showEdit.value = false; editTargetId = null }
async function performEdit(){
  error.value = ''
  try{
    await putSkill(editTargetId, {
      skill_name: editSkill.value.skill_name,
      proficiency: Number(editSkill.value.proficiency)
    })
    closeEdit()
    await refresh()
  }catch(e){ error.value = 'Update failed' }
}
async function removeSkill(s){
  // replaced by askRemoveSkill
}

function askRemoveSkill(s){
  deleteTargetId = s.id
  deleteItemLabel.value = s.skill_name
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
    await deleteSkill(deleteTargetId)
    closeConfirm()
    await refresh()
  }catch(e){ error.value = 'Delete failed' }
}
</script>
