<template>
  <div v-if="open" class="modal-backdrop" @click.self="emitClose">
    <div class="modal-card">
      <header class="modal-header">
        <h3 class="modal-title">{{ title }}</h3>
        <button class="modal-close" @click="emitClose" aria-label="Close">×</button>
      </header>
      <div class="modal-body">
        <slot />
      </div>
    </div>
  </div>
  
</template>

<script setup>
const props = defineProps({
  open: { type: Boolean, default: false },
  title: { type: String, default: '' }
})
const emit = defineEmits(['close'])
function emitClose(){ emit('close') }
</script>

<style scoped>
.modal-backdrop{
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-card{
  width: min(720px, 92vw);
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
  color: var(--text-primary);
}
.modal-header{
  display:flex; align-items:center; justify-content:space-between;
  padding: 12px 16px; border-bottom: 1px solid var(--border-color);
}
.modal-title{ margin:0; font-size: 18px; }
.modal-close{ background: transparent; border: none; color: var(--text-primary); font-size: 22px; cursor: pointer; }
.modal-body{ padding: 16px; }
</style>
