<template>
  <div
    class="dropzone"
    :class="{ 'is-dragging': dragging }"
    @dragover.prevent="onDragOver"
    @dragenter.prevent="onDragEnter"
    @dragleave.prevent="onDragLeave"
    @drop.prevent="onDrop"
    @click="openFilePicker"
  >
    <div class="dz-content">
      <div v-if="selectedFiles.length === 0">
        <slot name="label">
          <strong>Drag & drop</strong> {{ multiple ? 'files' : 'a file' }} here, or <span class="link">click to choose</span>.
        </slot>
      </div>
      <div v-else class="dz-selected">
        <div v-if="!multiple">
          <i class="fas fa-file"></i>
          <span class="name">{{ selectedFiles[0].name }}</span>
        </div>
        <div v-else class="dz-file-list">
          <div v-for="(file, index) in selectedFiles" :key="index" class="dz-file-item">
            <i class="fas fa-file"></i>
            <span class="name">{{ file.name }}</span>
          </div>
        </div>
        <button class="btn-icon danger" title="Clear" @click.stop="clear">
          <i class="fas fa-times"></i>
        </button>
      </div>
    </div>
    <input
      ref="fileInput"
      type="file"
      :accept="accept"
      :multiple="multiple"
      style="display:none"
      @change="onFileChange"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  accept: { type: String, default: '' },
  multiple: { type: Boolean, default: false }
})
const emit = defineEmits(['selected', 'cleared'])

const fileInput = ref(null)
const dragging = ref(false)
const selectedFiles = ref([])

function onDragOver() { dragging.value = true }
function onDragEnter() { dragging.value = true }
function onDragLeave() { dragging.value = false }
function onDrop(e) {
  dragging.value = false
  const files = Array.from(e.dataTransfer?.files || [])
  if (files.length > 0) {
    selectedFiles.value = props.multiple ? files : [files[0]]
    emit('selected', props.multiple ? selectedFiles.value : selectedFiles.value[0])
  }
}
function openFilePicker() { fileInput.value?.click() }
function onFileChange(e) {
  const files = Array.from(e.target.files || [])
  if (files.length > 0) {
    selectedFiles.value = props.multiple ? files : [files[0]]
    emit('selected', props.multiple ? selectedFiles.value : selectedFiles.value[0])
  }
}
function clear() {
  selectedFiles.value = []
  if (fileInput.value) fileInput.value.value = ''
  emit('cleared')
}
</script>

<style scoped>
.dropzone {
  border: 2px dashed #9ca3af;
  border-radius: 8px;
  padding: 14px;
  cursor: pointer;
  transition: border-color 0.15s ease, background 0.15s ease;
  background: #f9fafb;
}
.dropzone.is-dragging {
  border-color: #60a5fa;
  background: #eff6ff;
}
.dz-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.dz-selected {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
}
.dz-file-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.dz-file-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.9em;
}
.dz-selected .name {
  color: #374151;
}
.link { color: #2563eb; text-decoration: underline; }
.btn-icon { border:none; background:transparent; cursor:pointer; }
.btn-icon.danger { color:#ef4444; }
</style>
