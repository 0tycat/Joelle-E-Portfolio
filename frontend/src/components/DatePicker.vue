<template>
  <div class="date-picker" ref="pickerEl">
    <input
      ref="inputEl"
      class="input"
      :placeholder="placeholder"
      :readonly="readonly"
    />
    <button v-if="allowClear && internalValue" class="clear-btn" @click="clear">✕</button>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import flatpickr from 'flatpickr'
import 'flatpickr/dist/flatpickr.min.css'

const props = defineProps({
  modelValue: { type: [String, Date], default: '' },
  placeholder: { type: String, default: 'YYYY-MM-DD' },
  dateFormat: { type: String, default: 'Y-m-d' },
  allowClear: { type: Boolean, default: true },
  readonly: { type: Boolean, default: false },
  minDate: { type: [String, Date], default: null },
  maxDate: { type: [String, Date], default: null },
})
const emit = defineEmits(['update:modelValue'])

const inputEl = ref(null)
const pickerEl = ref(null)
let fp = null

const internalValue = ref(props.modelValue ? formatToOutput(props.modelValue) : '')

function formatToOutput(val){
  if(!val) return ''
  if(val instanceof Date){
    const y = val.getFullYear()
    const m = String(val.getMonth()+1).padStart(2, '0')
    const d = String(val.getDate()).padStart(2, '0')
    return `${y}-${m}-${d}`
  }
  // assume string already in YYYY-MM-DD
  return val
}

onMounted(() => {
  fp = flatpickr(inputEl.value, {
    dateFormat: props.dateFormat,
    defaultDate: internalValue.value || undefined,
    allowInput: false,
    disableMobile: true,
    monthSelectorType: 'dropdown',
    minDate: props.minDate || undefined,
    maxDate: props.maxDate || undefined,
    onChange: (selectedDates) => {
      const val = selectedDates && selectedDates[0] ? formatToOutput(selectedDates[0]) : ''
      internalValue.value = val
      emit('update:modelValue', val)
    },
  })
})

onBeforeUnmount(() => {
  if(fp){ fp.destroy(); fp = null }
})

watch(() => props.modelValue, (nv) => {
  const formatted = formatToOutput(nv)
  internalValue.value = formatted
  if(fp){ fp.setDate(formatted || null, true) }
})

function clear(){
  internalValue.value = ''
  if(fp){ fp.clear() }
  emit('update:modelValue', '')
}
</script>

<style scoped>
.date-picker{
  position: relative;
  display: inline-flex;
  align-items: center;
  width: 100%;
}
.input{
  width: 100%;
}
.clear-btn{
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
}
/* Theme override for flatpickr to match app variables */
:deep(.flatpickr-calendar){
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}
:deep(.flatpickr-months){
  border-bottom: 1px solid var(--border-color);
}
:deep(.flatpickr-day){
  color: var(--text-primary);
}
:deep(.flatpickr-day:hover){
  background: var(--bg-secondary);
}
:deep(.flatpickr-day.selected),
:deep(.flatpickr-day.startRange),
:deep(.flatpickr-day.endRange){
  background: #3b82f6;
  color: #ffffff;
}
:deep(.flatpickr-monthDropdown-months),
:deep(.numInputWrapper input){
  background: var(--bg-secondary);
  color: var(--text-primary);
}
:deep(.flatpickr-weekdays){
  color: var(--text-secondary);
}
:deep(.flatpickr-day.today){
  border-color: var(--border-color);
}
:deep(.flatpickr-day.disabled){
  color: var(--text-secondary);
  opacity: 0.5;
}
:deep(.flatpickr-months .flatpickr-prev-month svg),
:deep(.flatpickr-months .flatpickr-next-month svg){
  fill: var(--text-secondary);
}
:deep(.flatpickr-time .numInputWrapper input){
  background: var(--bg-secondary);
  color: var(--text-primary);
}
</style>
