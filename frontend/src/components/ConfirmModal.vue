<template>
  <Modal :open="open" :title="title" @close="emit('close')">
    <div style="margin-bottom:12px">{{ message }}</div>
    <div style="display:flex; gap:8px">
      <button class="btn danger" @click="emit('confirm')">Confirm</button>
      <button class="btn secondary" @click="emit('close')">Cancel</button>
    </div>
  </Modal>
</template>

<script setup>
import Modal from './Modal.vue'

const props = defineProps({
  open: { type: Boolean, default: false },
  title: { type: String, default: 'Confirm' },
  message: { type: String, default: 'Are you sure?' }
})
const emit = defineEmits(['confirm','close'])
</script>
