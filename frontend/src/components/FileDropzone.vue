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
      <div v-if="!selectedFile">
        <slot name="label">
          <strong>Drag & drop</strong> a file here, or <span class="link">click to choose</span>.
        </slot>
      </div>
      <div v-else class="dz-selected">
        <i class="fas fa-file"></i>
        <span class="name">{{ selectedFile.name }}</span>
        <button class="btn-icon danger" title="Clear" @click.stop="clear">
          <i class="fas fa-times"></i>
        </button>
      </div>
    </div>
    <input
      ref="fileInput"
      type="file"
      :accept="accept"
      style="display:none"
      @change="onFileChange"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  accept: { type: String, default: '' }
})
const emit = defineEmits(['selected', 'cleared'])

const fileInput = ref(null)
const dragging = ref(false)
const selectedFile = ref(null)

function onDragOver() { dragging.value = true }
function onDragEnter() { dragging.value = true }
function onDragLeave() { dragging.value = false }
function onDrop(e) {
  dragging.value = false
  const f = e.dataTransfer?.files?.[0]
  if (f) {
    selectedFile.value = f
    emit('selected', f)
  }
}
function openFilePicker() { fileInput.value?.click() }
function onFileChange(e) {
  const f = e.target.files?.[0]
  if (f) {
    selectedFile.value = f
    emit('selected', f)
  }
}
function clear() {
  selectedFile.value = null
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
}
.dz-selected .name {
  color: #374151;
}
.link { color: #2563eb; text-decoration: underline; }
.btn-icon { border:none; background:transparent; cursor:pointer; }
.btn-icon.danger { color:#ef4444; }
</style>
