// Vue 3 directive: v-bullet-tab
// Inserts a bullet "• " at the caret position on Tab inside a textarea.
// Keeps Tab working normally for non-textareas.
export default {
  mounted(el) {
    if (el.tagName !== 'TEXTAREA') return
    el.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        e.preventDefault()
        const start = el.selectionStart
        const end = el.selectionEnd
        const before = el.value.slice(0, start)
        const after = el.value.slice(end)
        const bullet = '• '
        el.value = before + bullet + after
        const newPos = start + bullet.length
        el.selectionStart = newPos
        el.selectionEnd = newPos
        el.dispatchEvent(new Event('input', { bubbles: true }))
      }
    })
  }
}
