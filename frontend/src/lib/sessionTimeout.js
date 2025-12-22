import { onMounted, onBeforeUnmount } from 'vue'
import { logout, isAuthed } from './auth.js'

// Session timeout configuration (in milliseconds)
const SESSION_TIMEOUT = 30 * 60 * 1000 // 30 minutes
const WARNING_TIME = 5 * 60 * 1000 // Show warning 5 minutes before timeout
let timeoutId = null
let warningId = null
let inactivityTimer = null

export function useSessionTimeout() {
  const resetInactivityTimer = () => {
    // Clear existing timers
    if (inactivityTimer) clearTimeout(inactivityTimer)
    if (timeoutId) clearTimeout(timeoutId)
    if (warningId) clearTimeout(warningId)

    // Only set timers if user is authenticated
    if (!isAuthed.value) return

    // Set warning timer
    warningId = setTimeout(() => {
      if (isAuthed.value) {
        // Show warning modal/toast - you can customize this
        const event = new CustomEvent('session:warning', {
          detail: { message: 'Your session will expire in 5 minutes due to inactivity.' }
        })
        window.dispatchEvent(event)
      }
    }, SESSION_TIMEOUT - WARNING_TIME)

    // Set logout timer
    timeoutId = setTimeout(() => {
      if (isAuthed.value) {
        // Auto logout
        logout()
        const event = new CustomEvent('session:expired', {
          detail: { message: 'Your session has expired. Please log in again.' }
        })
        window.dispatchEvent(event)
      }
    }, SESSION_TIMEOUT)
  }

  // Track user activity
  const trackActivity = () => {
    resetInactivityTimer()
  }

  // Setup activity listeners on mount
  const setupListeners = () => {
    // Reset timer on user interaction
    window.addEventListener('mousemove', trackActivity)
    window.addEventListener('keydown', trackActivity)
    window.addEventListener('click', trackActivity)
    window.addEventListener('scroll', trackActivity)
    window.addEventListener('touchstart', trackActivity)

    // Initialize timer if already logged in
    if (isAuthed.value) {
      resetInactivityTimer()
    }
  }

  // Cleanup listeners on unmount
  const cleanupListeners = () => {
    window.removeEventListener('mousemove', trackActivity)
    window.removeEventListener('keydown', trackActivity)
    window.removeEventListener('click', trackActivity)
    window.removeEventListener('scroll', trackActivity)
    window.removeEventListener('touchstart', trackActivity)

    if (inactivityTimer) clearTimeout(inactivityTimer)
    if (timeoutId) clearTimeout(timeoutId)
    if (warningId) clearTimeout(warningId)
  }

  onMounted(() => {
    setupListeners()
  })

  onBeforeUnmount(() => {
    cleanupListeners()
  })

  return {
    resetInactivityTimer,
    trackActivity,
    setupListeners,
    cleanupListeners
  }
}
