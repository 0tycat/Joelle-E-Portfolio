<template>
  <div class="resume-container">
    <!-- Skip to Section Navigation -->
    <div class="skip-navigation">
      <h2 style="font-size: 1.2rem; margin-bottom: 1rem;">Skip to:</h2>
      <div class="skip-buttons">
        <button class="btn btn-outline" @click="scrollTo('work')"><i class="fas fa-briefcase"></i> Work Experience</button>
        <button class="btn btn-outline" @click="scrollTo('education')"><i class="fas fa-graduation-cap"></i> Education</button>
        <button class="btn btn-outline" @click="scrollTo('skills')"><i class="fas fa-star"></i> Skillsets</button>
      </div>
    </div>

    <!-- Work Experience Section -->
    <section id="work" class="resume-section">
      <h2 class="section-title">Work Experience:</h2>
      <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-bottom:12px">
        <div v-if="isAuthed">
          <button class="btn" @click="showAddWork=true"><i class="fas fa-plus"></i> Add Work</button>
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center">
          <div style="position:relative">
            <button class="btn secondary" @click="toggleWorkFilter"><i class="fas fa-filter"></i> Filter</button>
            <div v-if="workFilterOpen" class="card" style="position:absolute; top:110%; left:0; min-width:240px; z-index:10; padding:10px; display:flex; flex-direction:column; gap:8px">
              <strong>Roles</strong>
              <small style="color:#6b7280">Checked roles are hidden</small>
              <label v-for="role in workRoleOptions" :key="role" style="display:flex; align-items:center; gap:6px">
                <input type="checkbox" v-model="activeWorkRoles" :value="role" />
                <span>{{ role }}</span>
              </label>
              <button class="btn secondary" style="padding:6px 10px; align-self:flex-start" @click="clearWorkFilters"><i class="fas fa-undo"></i> Clear</button>
            </div>
          </div>
          <div style="position:relative">
            <button class="btn secondary" @click="toggleWorkSort"><i class="fas fa-sort"></i> Sort: {{ workSortLabel }}</button>
            <div v-if="workSortOpen" class="card" style="position:absolute; top:110%; left:0; min-width:200px; z-index:10; padding:10px; display:flex; flex-direction:column; gap:6px">
              <button class="btn secondary" :class="{active: workSortMode==='alpha-asc'}" @click="setWorkSortAndClose('alpha-asc')">Company A → Z</button>
              <button class="btn secondary" :class="{active: workSortMode==='alpha-desc'}" @click="setWorkSortAndClose('alpha-desc')">Company Z → A</button>
              <button class="btn secondary" :class="{active: workSortMode==='start-new'}" @click="setWorkSortAndClose('start-new')">Start: Newest</button>
              <button class="btn secondary" :class="{active: workSortMode==='start-old'}" @click="setWorkSortAndClose('start-old')">Start: Oldest</button>
              <button class="btn secondary" :class="{active: workSortMode==='end-new'}" @click="setWorkSortAndClose('end-new')">End: Newest</button>
              <button class="btn secondary" :class="{active: workSortMode==='end-old'}" @click="setWorkSortAndClose('end-old')">End: Oldest</button>
            </div>
          </div>
        </div>
      </div>
      <div v-if="workLoading">Loading...</div>
      <div v-else>
        <div v-for="w in workFilteredAndSorted" :key="w.id" class="card">
          <div style="display:flex; gap:12px; align-items:start">
            <img v-if="w.organization_logo" :src="getLogoUrl('work', w.id)" alt="Logo" style="width:48px; height:48px; object-fit:contain; border-radius:4px" />
            <div style="flex:1">
              <strong>{{ w.company_name }}</strong>
              <div>{{ w.role }}</div>
              <div>{{ formatDate(w.start_date) }} - {{ w.end_date ? formatDate(w.end_date) : 'Present' }}</div>
              <p style="white-space:pre-wrap">{{ w.description }}</p>
            </div>
          </div>
          <div v-if="isAuthed" class="card-actions">
            <button class="btn-icon secondary" @click="startEditWork(w)" title="Edit"><i class="fas fa-edit"></i></button>
            <button class="btn-icon danger" @click="askRemoveWork(w)" title="Delete"><i class="fas fa-trash"></i></button>
          </div>
        </div>
      </div>
    </section>

    <!-- Education Section -->
    <section id="education" class="resume-section">
      <h2 class="section-title">Education:</h2>
      <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-bottom:12px">
        <div v-if="isAuthed">
          <button class="btn" @click="showAddEducation=true"><i class="fas fa-plus"></i> Add Education</button>
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center">
          <div style="position:relative">
            <button class="btn secondary" @click="toggleEducationFilter"><i class="fas fa-filter"></i> Filter</button>
            <div v-if="educationFilterOpen" class="card" style="position:absolute; top:110%; left:0; min-width:240px; z-index:10; padding:10px; display:flex; flex-direction:column; gap:8px">
              <strong>Institutes</strong>
              <small style="color:#6b7280">Checked institutes are hidden</small>
              <label v-for="inst in instituteOptions" :key="inst" style="display:flex; align-items:center; gap:6px">
                <input type="checkbox" v-model="activeInstitutes" :value="inst" />
                <span>{{ inst }}</span>
              </label>
              <button class="btn secondary" style="padding:6px 10px; align-self:flex-start" @click="clearEducationFilters"><i class="fas fa-undo"></i> Clear</button>
            </div>
          </div>
          <div style="position:relative">
            <button class="btn secondary" @click="toggleEducationSort"><i class="fas fa-sort"></i> Sort: {{ educationSortLabel }}</button>
            <div v-if="educationSortOpen" class="card" style="position:absolute; top:110%; left:0; min-width:200px; z-index:10; padding:10px; display:flex; flex-direction:column; gap:6px">
              <button class="btn secondary" :class="{active: educationSortMode==='alpha-asc'}" @click="setEducationSortAndClose('alpha-asc')">Institute A → Z</button>
              <button class="btn secondary" :class="{active: educationSortMode==='alpha-desc'}" @click="setEducationSortAndClose('alpha-desc')">Institute Z → A</button>
              <button class="btn secondary" :class="{active: educationSortMode==='start-new'}" @click="setEducationSortAndClose('start-new')">Start: Newest</button>
              <button class="btn secondary" :class="{active: educationSortMode==='start-old'}" @click="setEducationSortAndClose('start-old')">Start: Oldest</button>
              <button class="btn secondary" :class="{active: educationSortMode==='end-new'}" @click="setEducationSortAndClose('end-new')">Finish: Newest</button>
              <button class="btn secondary" :class="{active: educationSortMode==='end-old'}" @click="setEducationSortAndClose('end-old')">Finish: Oldest</button>
            </div>
          </div>
        </div>
      </div>
      <div v-if="educationLoading">Loading...</div>
      <div v-else>
        <div v-for="e in educationFilteredAndSorted" :key="e.id" class="card education-card">
          <div class="education-logo-section">
            <img v-if="e.organisation_logo" :src="base64ToDataUrl(e.organisation_logo)" alt="Logo" class="education-logo" />
            <div v-else class="education-logo-placeholder">
              <i class="fas fa-image"></i>
              <span>No Logo</span>
            </div>
          </div>
          <div class="education-info-section">
            <strong class="education-institute">{{ e.institute_name }}</strong>
            <div class="education-certification">{{ e.certification }}</div>
            <div class="education-dates">{{ formatDate(e.start_date) }} - {{ e.finish_date ? formatDate(e.finish_date) : 'Present' }}</div>
          </div>
          <div v-if="isAuthed" class="card-actions">
            <button class="btn-icon secondary" @click="startEditEducation(e)" title="Edit"><i class="fas fa-edit"></i></button>
            <button class="btn-icon danger" @click="askRemoveEducation(e)" title="Delete"><i class="fas fa-trash"></i></button>
          </div>
        </div>
      </div>
    </section>

    <!-- Skills Section -->
    <section id="skills" class="resume-section">
      <h2 class="section-title">Skillsets:</h2>
      <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-bottom:12px">
        <div v-if="isAuthed">
          <button class="btn" @click="showAddSkill=true"><i class="fas fa-plus"></i> Add Skill</button>
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center">
          <div style="position:relative">
            <button class="btn secondary" @click="toggleSkillsFilter"><i class="fas fa-filter"></i> Filter</button>
            <div v-if="skillsFilterOpen" class="card" style="position:absolute; top:110%; left:0; min-width:240px; z-index:10; padding:10px; display:flex; flex-direction:column; gap:8px">
              <strong>Proficiency</strong>
              <small style="color:#6b7280">Checked levels are hidden</small>
              <label v-for="lvl in profLevels" :key="lvl.id" style="display:flex; align-items:center; gap:6px">
                <input type="checkbox" v-model="activeSkillLevels" :value="String(lvl.id)" />
                <span>{{ lvl.level }}</span>
              </label>
              <button class="btn secondary" style="padding:6px 10px; align-self:flex-start" @click="clearSkillsFilters"><i class="fas fa-undo"></i> Clear</button>
            </div>
          </div>
          <div style="position:relative">
            <button class="btn secondary" @click="toggleSkillsSort"><i class="fas fa-sort"></i> Sort: {{ skillsSortLabel }}</button>
            <div v-if="skillsSortOpen" class="card" style="position:absolute; top:110%; left:0; min-width:200px; z-index:10; padding:10px; display:flex; flex-direction:column; gap:6px">
              <button class="btn secondary" :class="{active: skillsSortMode==='alpha-asc'}" @click="setSkillsSortAndClose('alpha-asc')">A → Z</button>
              <button class="btn secondary" :class="{active: skillsSortMode==='alpha-desc'}" @click="setSkillsSortAndClose('alpha-desc')">Z → A</button>
              <button class="btn secondary" :class="{active: skillsSortMode==='prof-asc'}" @click="setSkillsSortAndClose('prof-asc')">Proficiency ↑</button>
              <button class="btn secondary" :class="{active: skillsSortMode==='prof-desc'}" @click="setSkillsSortAndClose('prof-desc')">Proficiency ↓</button>
            </div>
          </div>
        </div>
      </div>
      <div v-if="skillsLoading">Loading...</div>
      <div v-else>
        <div v-for="s in skillsFilteredAndSorted" :key="s.id" class="card">
          <strong>{{ s.skill_name }}</strong>
          <div>Proficiency: {{ s.proficiency_label ? s.proficiency_label : s.proficiency }}</div>
          <div v-if="isAuthed" class="card-actions">
            <button class="btn-icon secondary" @click="startEditSkill(s)" title="Edit"><i class="fas fa-edit"></i></button>
            <button class="btn-icon danger" @click="askRemoveSkill(s)" title="Delete"><i class="fas fa-trash"></i></button>
          </div>
        </div>
      </div>
    </section>

    <!-- Work Modals -->
    <Modal :open="showAddWork" title="Add Work" @close="closeAddWork">
      <div style="display:flex; gap:8px; flex-direction:column">
        <input class="input" v-model="newWork.company_name" placeholder="Company" />
        <input class="input" v-model="newWork.role" placeholder="Role" />
        <DatePicker v-model="newWork.start_date" placeholder="Start (YYYY-MM-DD)" />
        <DatePicker v-model="newWork.end_date" placeholder="End (YYYY-MM-DD)" />
        <textarea class="input" v-model="newWork.description" @keydown="handleDescriptionKeydown($event, newWork)" placeholder="Description (press Enter for new bullet)" rows="5" style="resize:vertical"></textarea>
        <label style="font-weight:600">Organization Logo (optional)</label>
        <FileDropzone accept="image/*" @selected="onNewWorkLogoSelected" @cleared="onNewWorkLogoCleared">
          <template #label><span>Upload organization logo (PNG, JPG, SVG)</span></template>
        </FileDropzone>
        <div style="display:flex; gap:8px">
          <button class="btn" @click="addWork"><i class="fas fa-save"></i> Save</button>
          <button class="btn secondary" @click="closeAddWork"><i class="fas fa-times"></i> Cancel</button>
        </div>
      </div>
      <p v-if="workError" style="color:#fca5a5">{{ workError }}</p>
    </Modal>

    <Modal :open="showEditWork" title="Edit Work" @close="closeEditWork">
      <div style="display:flex; gap:8px; flex-direction:column">
        <input class="input" v-model="editWork.company_name" placeholder="Company" />
        <input class="input" v-model="editWork.role" placeholder="Role" />
        <DatePicker v-model="editWork.start_date" placeholder="Start (YYYY-MM-DD)" />
        <DatePicker v-model="editWork.end_date" placeholder="End (YYYY-MM-DD)" />
        <textarea class="input" v-model="editWork.description" @keydown="handleDescriptionKeydown($event, editWork)" placeholder="Description (press Enter for new bullet)" rows="5" style="resize:vertical"></textarea>
        <label style="font-weight:600">Organization Logo (optional)</label>
        <FileDropzone accept="image/*" @selected="onEditWorkLogoSelected" @cleared="onEditWorkLogoCleared">
          <template #label><span>Upload new logo to replace existing (leave empty to keep current)</span></template>
        </FileDropzone>
        <div style="display:flex; gap:8px">
          <button class="btn" @click="performEditWork"><i class="fas fa-save"></i> Save</button>
          <button class="btn secondary" @click="closeEditWork"><i class="fas fa-times"></i> Cancel</button>
        </div>
      </div>
      <p v-if="workError" style="color:#fca5a5">{{ workError }}</p>
    </Modal>

    <!-- Education Modals -->
    <Modal :open="showAddEducation" title="Add Education" @close="closeAddEducation">
      <div style="display:flex; gap:8px; flex-direction:column">
        <input class="input" v-model="newEducation.institute_name" placeholder="Institute" />
        <input class="input" v-model="newEducation.certification" placeholder="Certification" />
        <DatePicker v-model="newEducation.start_date" placeholder="Start (YYYY-MM-DD)" />
        <DatePicker v-model="newEducation.finish_date" placeholder="Finish (YYYY-MM-DD)" />
        <label style="font-weight:600">Organization Logo (optional)</label>
        <FileDropzone accept="image/*" @selected="onNewEducationLogoSelected" @cleared="onNewEducationLogoCleared">
          <template #label><span>Upload organization logo (PNG, JPG, SVG)</span></template>
        </FileDropzone>
        <div style="display:flex; gap:8px">
          <button class="btn" @click="addEducation"><i class="fas fa-save"></i> Save</button>
          <button class="btn secondary" @click="closeAddEducation"><i class="fas fa-times"></i> Cancel</button>
        </div>
      </div>
      <p v-if="educationError" style="color:#fca5a5">{{ educationError }}</p>
    </Modal>

    <Modal :open="showEditEducation" title="Edit Education" @close="closeEditEducation">
      <div style="display:flex; gap:8px; flex-direction:column">
        <input class="input" v-model="editEducation.institute_name" placeholder="Institute" />
        <input class="input" v-model="editEducation.certification" placeholder="Certification" />
        <DatePicker v-model="editEducation.start_date" placeholder="Start (YYYY-MM-DD)" />
        <DatePicker v-model="editEducation.finish_date" placeholder="Finish (YYYY-MM-DD)" />
        <label style="font-weight:600">Organization Logo (optional)</label>
        <FileDropzone accept="image/*" @selected="onEditEducationLogoSelected" @cleared="onEditEducationLogoCleared">
          <template #label><span>Upload new logo to replace existing (leave empty to keep current)</span></template>
        </FileDropzone>
        <div style="display:flex; gap:8px">
          <button class="btn" @click="performEditEducation"><i class="fas fa-save"></i> Save</button>
          <button class="btn secondary" @click="closeEditEducation"><i class="fas fa-times"></i> Cancel</button>
        </div>
      </div>
      <p v-if="educationError" style="color:#fca5a5">{{ educationError }}</p>
    </Modal>

    <!-- Skills Modals -->
    <Modal :open="showAddSkill" title="Add Skill" @close="closeAddSkill">
      <div style="display:flex; gap:8px; flex-direction:column">
        <input class="input" v-model="newSkill.skill_name" placeholder="Skill name" />
        <select class="input" v-model="newSkill.proficiency">
          <option disabled value="">Select proficiency level</option>
          <option v-for="lvl in profLevels" :key="lvl.id" :value="String(lvl.id)">{{ lvl.level }}</option>
        </select>
        <div style="display:flex; gap:8px">
          <button class="btn" @click="addSkill"><i class="fas fa-save"></i> Save</button>
          <button class="btn secondary" @click="closeAddSkill"><i class="fas fa-times"></i> Cancel</button>
        </div>
      </div>
      <p v-if="skillsError" style="color:#fca5a5">{{ skillsError }}</p>
    </Modal>

    <Modal :open="showEditSkill" title="Edit Skill" @close="closeEditSkill">
      <div style="display:flex; gap:8px; flex-direction:column">
        <input class="input" v-model="editSkill.skill_name" />
        <select class="input" v-model="editSkill.proficiency">
          <option disabled value="">Select proficiency level</option>
          <option v-for="lvl in profLevels" :key="lvl.id" :value="String(lvl.id)">{{ lvl.level }}</option>
        </select>
        <div style="display:flex; gap:8px">
          <button class="btn" @click="performEditSkill"><i class="fas fa-save"></i> Save</button>
          <button class="btn secondary" @click="closeEditSkill"><i class="fas fa-times"></i> Cancel</button>
        </div>
      </div>
      <p v-if="skillsError" style="color:#fca5a5">{{ skillsError }}</p>
    </Modal>

    <!-- Confirm Delete Modals -->
    <ConfirmModal
      :open="showWorkConfirm"
      title="Delete Work Record"
      :message="workConfirmMessage"
      @confirm="performDeleteWork"
      @close="closeWorkConfirm"
    />

    <ConfirmModal
      :open="showEducationConfirm"
      title="Delete Education Record"
      :message="educationConfirmMessage"
      @confirm="performDeleteEducation"
      @close="closeEducationConfirm"
    />

    <ConfirmModal
      :open="showSkillConfirm"
      title="Delete Skill"
      :message="skillConfirmMessage"
      @confirm="performDeleteSkill"
      @close="closeSkillConfirm"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { 
  apiGet, 
  postWork, deleteWork, putWork, uploadWorkLogo,
  postEducation, deleteEducation, putEducation,
  postSkill, putSkill, deleteSkill, getProfLevels
} from '../lib/api.js'
import { isAuthed as authIsAuthed } from '../lib/auth.js'
import { formatDate } from '../lib/date.js'
import Modal from '../components/Modal.vue'
import ConfirmModal from '../components/ConfirmModal.vue'
import DatePicker from '../components/DatePicker.vue'
import FileDropzone from '../components/FileDropzone.vue'

const isAuthed = authIsAuthed

// ========== WORK EXPERIENCE ==========
const work = ref([])
const workLoading = ref(true)
const workError = ref('')
const activeWorkRoles = ref([])
const workFilterOpen = ref(false)
const workSortOpen = ref(false)
const workSortMode = ref('start-new')
const newWork = ref({ company_name:'', role:'', start_date:'', end_date:'', description:'' })
const editWork = ref({ company_name:'', role:'', start_date:'', end_date:'', description:'' })
const newWorkLogo = ref(null)
const editWorkLogo = ref(null)
const showAddWork = ref(false)
const showEditWork = ref(false)
let editWorkTargetId = null
const showWorkConfirm = ref(false)
let deleteWorkTargetId = null
const deleteWorkLabel = ref('')
const workConfirmMessage = computed(() => `Delete "${deleteWorkLabel.value}"? This cannot be undone.`)

const workRoleOptions = computed(() => {
  const roles = new Set(work.value.map(w => w.role).filter(Boolean))
  return Array.from(roles).sort((a,b) => a.localeCompare(b))
})

const workFilteredAndSorted = computed(() => {
  const filtered = activeWorkRoles.value.length
    ? work.value.filter(w => !activeWorkRoles.value.includes(w.role))
    : work.value
  const toDate = v => v ? new Date(v) : null
  return [...filtered].sort((a,b) => {
    if(workSortMode.value === 'alpha-asc') return a.company_name.localeCompare(b.company_name)
    if(workSortMode.value === 'alpha-desc') return b.company_name.localeCompare(a.company_name)
    if(workSortMode.value === 'start-new') return (toDate(b.start_date) - toDate(a.start_date))
    if(workSortMode.value === 'start-old') return (toDate(a.start_date) - toDate(b.start_date))
    if(workSortMode.value === 'end-new') return (toDate(b.end_date) || 0) - (toDate(a.end_date) || 0)
    if(workSortMode.value === 'end-old') return (toDate(a.end_date) || 0) - (toDate(b.end_date) || 0)
    return 0
  })
})

const workSortLabel = computed(() => {
  if(workSortMode.value === 'alpha-asc') return 'Company A → Z'
  if(workSortMode.value === 'alpha-desc') return 'Company Z → A'
  if(workSortMode.value === 'start-new') return 'Start: Newest'
  if(workSortMode.value === 'start-old') return 'Start: Oldest'
  if(workSortMode.value === 'end-new') return 'End: Newest'
  if(workSortMode.value === 'end-old') return 'End: Oldest'
  return 'Choose'
})

function toggleWorkFilter(){ workFilterOpen.value = !workFilterOpen.value; if(workFilterOpen.value) workSortOpen.value = false }
function toggleWorkSort(){ workSortOpen.value = !workSortOpen.value; if(workSortOpen.value) workFilterOpen.value = false }
function setWorkSortAndClose(mode){ workSortMode.value = mode; workSortOpen.value = false }
function clearWorkFilters(){ activeWorkRoles.value = [] }

async function refreshWork(){
  try{ work.value = await apiGet('/api/work') } 
  finally { workLoading.value = false }
}

async function addWork(){
  workError.value = ''
  try{
    const created = await postWork(newWork.value)
    const createdId = created?.data?.[0]?.id
    if (createdId && newWorkLogo.value) await uploadWorkLogo(createdId, newWorkLogo.value)
    newWork.value = { company_name:'', role:'', start_date:'', end_date:'', description:'' }
    newWorkLogo.value = null
    await refreshWork()
    showAddWork.value = false
  }catch(e){ workError.value = 'Add failed' }
}

function startEditWork(w){
  editWork.value = { company_name:w.company_name, role:w.role, start_date:w.start_date, end_date:w.end_date, description:w.description }
  editWorkTargetId = w.id
  showEditWork.value = true
}

function closeAddWork(){ showAddWork.value = false; newWorkLogo.value = null }
function closeEditWork(){ showEditWork.value = false; editWorkTargetId = null; editWorkLogo.value = null }

async function performEditWork(){
  workError.value = ''
  try{
    await putWork(editWorkTargetId, editWork.value)
    if (editWorkLogo.value) await uploadWorkLogo(editWorkTargetId, editWorkLogo.value)
    editWorkLogo.value = null
    closeEditWork()
    await refreshWork()
  }catch(e){ workError.value = 'Update failed' }
}

function onNewWorkLogoSelected(file){ newWorkLogo.value = file }
function onNewWorkLogoCleared(){ newWorkLogo.value = null }
function onEditWorkLogoSelected(file){ editWorkLogo.value = file }
function onEditWorkLogoCleared(){ editWorkLogo.value = null }

function askRemoveWork(w){ deleteWorkTargetId = w.id; deleteWorkLabel.value = w.company_name; showWorkConfirm.value = true }
function closeWorkConfirm(){ showWorkConfirm.value = false; deleteWorkTargetId = null; deleteWorkLabel.value = '' }
async function performDeleteWork(){
  workError.value = ''
  try{ await deleteWork(deleteWorkTargetId); closeWorkConfirm(); await refreshWork() }
  catch(e){ workError.value = 'Delete failed' }
}

// ========== EDUCATION ==========
const education = ref([])
const educationLoading = ref(true)
const educationError = ref('')
const activeInstitutes = ref([])
const educationFilterOpen = ref(false)
const educationSortOpen = ref(false)
const educationSortMode = ref('start-new')
const newEducation = ref({ institute_name:'', certification:'', start_date:'', finish_date:'' })
const editEducation = ref({ institute_name:'', certification:'', start_date:'', finish_date:'' })
const newEducationLogo = ref(null)
const editEducationLogo = ref(null)
const showAddEducation = ref(false)
const showEditEducation = ref(false)
let editEducationTargetId = null
const showEducationConfirm = ref(false)
let deleteEducationTargetId = null
const deleteEducationLabel = ref('')
const educationConfirmMessage = computed(() => `Delete "${deleteEducationLabel.value}"? This cannot be undone.`)

const instituteOptions = computed(() => {
  const set = new Set(education.value.map(e => e.institute_name).filter(Boolean))
  return Array.from(set).sort((a,b) => a.localeCompare(b))
})

const educationFilteredAndSorted = computed(() => {
  const filtered = activeInstitutes.value.length
    ? education.value.filter(e => !activeInstitutes.value.includes(e.institute_name))
    : education.value
  const toDate = v => v ? new Date(v) : null
  return [...filtered].sort((a,b) => {
    if(educationSortMode.value === 'alpha-asc') return a.institute_name.localeCompare(b.institute_name)
    if(educationSortMode.value === 'alpha-desc') return b.institute_name.localeCompare(a.institute_name)
    if(educationSortMode.value === 'start-new') return (toDate(b.start_date) - toDate(a.start_date))
    if(educationSortMode.value === 'start-old') return (toDate(a.start_date) - toDate(b.start_date))
    if(educationSortMode.value === 'end-new') return (toDate(b.finish_date) || 0) - (toDate(a.finish_date) || 0)
    if(educationSortMode.value === 'end-old') return (toDate(a.finish_date) || 0) - (toDate(b.finish_date) || 0)
    return 0
  })
})

const educationSortLabel = computed(() => {
  if(educationSortMode.value === 'alpha-asc') return 'Institute A → Z'
  if(educationSortMode.value === 'alpha-desc') return 'Institute Z → A'
  if(educationSortMode.value === 'start-new') return 'Start: Newest'
  if(educationSortMode.value === 'start-old') return 'Start: Oldest'
  if(educationSortMode.value === 'end-new') return 'Finish: Newest'
  if(educationSortMode.value === 'end-old') return 'Finish: Oldest'
  return 'Choose'
})

function toggleEducationFilter(){ educationFilterOpen.value = !educationFilterOpen.value; if(educationFilterOpen.value) educationSortOpen.value = false }
function toggleEducationSort(){ educationSortOpen.value = !educationSortOpen.value; if(educationSortOpen.value) educationFilterOpen.value = false }
function setEducationSortAndClose(mode){ educationSortMode.value = mode; educationSortOpen.value = false }
function clearEducationFilters(){ activeInstitutes.value = [] }

async function refreshEducation(){
  try{ education.value = await apiGet('/api/education') } 
  finally { educationLoading.value = false }
}

async function addEducation(){
  educationError.value = ''
  try{
    const created = await postEducation(newEducation.value, newEducationLogo.value)
    newEducation.value = { institute_name:'', certification:'', start_date:'', finish_date:'' }
    newEducationLogo.value = null
    await refreshEducation()
    showAddEducation.value = false
  }catch(e){ educationError.value = 'Add failed' }
}

function startEditEducation(e){
  editEducation.value = { institute_name:e.institute_name, certification:e.certification, start_date:e.start_date, finish_date:e.finish_date }
  editEducationTargetId = e.id
  showEditEducation.value = true
}

function closeAddEducation(){ showAddEducation.value = false; newEducationLogo.value = null }
function closeEditEducation(){ showEditEducation.value = false; editEducationTargetId = null; editEducationLogo.value = null }

async function performEditEducation(){
  educationError.value = ''
  try{
    await putEducation(editEducationTargetId, editEducation.value, editEducationLogo.value)
    editEducationLogo.value = null
    closeEditEducation()
    await refreshEducation()
  }catch(err){ educationError.value = 'Update failed' }
}

function onNewEducationLogoSelected(file){ newEducationLogo.value = file }
function onNewEducationLogoCleared(){ newEducationLogo.value = null }
function onEditEducationLogoSelected(file){ editEducationLogo.value = file }
function onEditEducationLogoCleared(){ editEducationLogo.value = null }

function askRemoveEducation(e){ deleteEducationTargetId = e.id; deleteEducationLabel.value = e.institute_name; showEducationConfirm.value = true }
function closeEducationConfirm(){ showEducationConfirm.value = false; deleteEducationTargetId = null; deleteEducationLabel.value = '' }
async function performDeleteEducation(){
  educationError.value = ''
  try{ await deleteEducation(deleteEducationTargetId); closeEducationConfirm(); await refreshEducation() }
  catch(err){ educationError.value = 'Delete failed' }
}

// ========== SKILLS ==========
const skills = ref([])
const skillsLoading = ref(true)
const skillsError = ref('')
const profLevels = ref([])
const activeSkillLevels = ref([])
const skillsFilterOpen = ref(false)
const skillsSortOpen = ref(false)
const skillsSortMode = ref('alpha-asc')
const newSkill = ref({ skill_name:'', proficiency:'' })
const editSkill = ref({ skill_name:'', proficiency:'' })
const showAddSkill = ref(false)
const showEditSkill = ref(false)
let editSkillTargetId = null
const showSkillConfirm = ref(false)
let deleteSkillTargetId = null
const deleteSkillLabel = ref('')
const skillConfirmMessage = computed(() => `Delete "${deleteSkillLabel.value}"? This cannot be undone.`)

const skillsFilteredAndSorted = computed(() => {
  const byLevel = activeSkillLevels.value.length
    ? skills.value.filter(s => !activeSkillLevels.value.includes(String(s.proficiency)))
    : skills.value
  const labelFor = lvlId => profLevels.value.find(l => String(l.id) === String(lvlId))?.level || ''
  return [...byLevel].sort((a,b) => {
    if(skillsSortMode.value === 'alpha-asc') return a.skill_name.localeCompare(b.skill_name)
    if(skillsSortMode.value === 'alpha-desc') return b.skill_name.localeCompare(a.skill_name)
    const aVal = Number(a.proficiency)
    const bVal = Number(b.proficiency)
    if(skillsSortMode.value === 'prof-asc') return aVal - bVal || labelFor(aVal).localeCompare(labelFor(bVal))
    if(skillsSortMode.value === 'prof-desc') return bVal - aVal || labelFor(bVal).localeCompare(labelFor(aVal))
    return 0
  })
})

const skillsSortLabel = computed(() => {
  if(skillsSortMode.value === 'alpha-asc') return 'A → Z'
  if(skillsSortMode.value === 'alpha-desc') return 'Z → A'
  if(skillsSortMode.value === 'prof-asc') return 'Proficiency ↑'
  if(skillsSortMode.value === 'prof-desc') return 'Proficiency ↓'
  return 'Choose'
})

function toggleSkillsFilter(){ skillsFilterOpen.value = !skillsFilterOpen.value; if(skillsFilterOpen.value) skillsSortOpen.value = false }
function toggleSkillsSort(){ skillsSortOpen.value = !skillsSortOpen.value; if(skillsSortOpen.value) skillsFilterOpen.value = false }
function setSkillsSortAndClose(mode){ skillsSortMode.value = mode; skillsSortOpen.value = false }
function clearSkillsFilters(){ activeSkillLevels.value = [] }

async function refreshSkills(){
  try{
    const [levels, skillsData] = await Promise.all([
      getProfLevels().catch(() => []),
      apiGet('/api/skills')
    ])
    profLevels.value = Array.isArray(levels) ? levels : []
    skills.value = skillsData
  } finally { skillsLoading.value = false }
}

async function addSkill(){
  skillsError.value = ''
  try{
    if(!newSkill.value.skill_name || !newSkill.value.proficiency){
      skillsError.value = 'Provide skill name and proficiency'
      return
    }
    await postSkill({ skill_name: newSkill.value.skill_name, proficiency: Number(newSkill.value.proficiency) })
    newSkill.value = { skill_name:'', proficiency:'' }
    await refreshSkills()
    showAddSkill.value = false
  }catch(e){ skillsError.value = 'Add failed' }
}

function startEditSkill(s){
  editSkill.value = { skill_name: s.skill_name, proficiency: s.proficiency }
  editSkillTargetId = s.id
  showEditSkill.value = true
}

function closeAddSkill(){ showAddSkill.value = false }
function closeEditSkill(){ showEditSkill.value = false; editSkillTargetId = null }

async function performEditSkill(){
  skillsError.value = ''
  try{
    await putSkill(editSkillTargetId, { skill_name: editSkill.value.skill_name, proficiency: Number(editSkill.value.proficiency) })
    closeEditSkill()
    await refreshSkills()
  }catch(e){ skillsError.value = 'Update failed' }
}

function askRemoveSkill(s){ deleteSkillTargetId = s.id; deleteSkillLabel.value = s.skill_name; showSkillConfirm.value = true }
function closeSkillConfirm(){ showSkillConfirm.value = false; deleteSkillTargetId = null; deleteSkillLabel.value = '' }
async function performDeleteSkill(){
  skillsError.value = ''
  try{ await deleteSkill(deleteSkillTargetId); closeSkillConfirm(); await refreshSkills() }
  catch(e){ skillsError.value = 'Delete failed' }
}

// ========== UTILITIES ==========
function getLogoUrl(type, id) {
  const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
  return `${API_URL}/api/${type}/${id}/logo`
}

function handleDescriptionKeydown(event, item){
  if(event.key === 'Enter'){
    if(event.shiftKey) return
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
      setTimeout(() => { textarea.selectionStart = textarea.selectionEnd = cursorPos - currentLine.length }, 0)
      return
    }
    const bullet = currentLine.trim().startsWith('•') || currentLine.trim().startsWith('-') ? '\n• ' : (beforeCursor.trim() === '' ? '• ' : '\n• ')
    item.description = beforeCursor + bullet + afterCursor
    setTimeout(() => { textarea.selectionStart = textarea.selectionEnd = cursorPos + bullet.length }, 0)
  }
}

function scrollTo(sectionId) {
  const element = document.getElementById(sectionId)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

function base64ToDataUrl(base64String) {
  if (!base64String) return null
  // Base64 text can be used directly in a data URL
  return `data:image/jpeg;base64,${base64String}`
}

// ========== INITIALIZE ==========
onMounted(() => {
  refreshWork()
  refreshEducation()
  refreshSkills()
})
</script>

<style scoped>
.resume-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

.skip-navigation {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  text-align: center;
}

.skip-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.resume-section {
  margin-bottom: 3rem;
  padding: 2rem;
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 8px;
}

.section-title {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--card-border);
  color: var(--text-primary);
}

.card {
  margin-bottom: 1rem;
}

.education-card {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
}

.education-logo-section {
  flex-shrink: 0;
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.education-logo {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 8px;
  border: 2px solid var(--card-border);
}

.education-logo-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 2px dashed var(--card-border);
  border-radius: 8px;
  color: var(--text-secondary);
  font-size: 0.9rem;
  gap: 0.5rem;
}

.education-logo-placeholder i {
  font-size: 1.5rem;
  opacity: 0.5;
}

.education-info-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.education-institute {
  font-size: 1.1rem;
  color: var(--text-primary);
}

.education-certification {
  color: var(--text-primary);
  font-weight: 500;
}

.education-dates {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .skip-buttons {
    flex-direction: column;
    align-items: stretch;
  }
  
  .resume-section {
    padding: 1rem;
  }

  .education-card {
    flex-direction: column;
    align-items: center;
  }

  .education-logo-section {
    width: 100px;
    height: 100px;
  }
}

</style>
