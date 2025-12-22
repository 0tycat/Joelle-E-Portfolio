import { ref, watch } from 'vue'

const stored = localStorage.getItem('theme')
const prefersDark = typeof window !== 'undefined' && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
const isDark = ref(stored ? stored === 'dark' : prefersDark)

export function useTheme() {
  watch(isDark, (newVal) => {
    localStorage.setItem('theme', newVal ? 'dark' : 'light')
    applyTheme(newVal)
  }, { immediate: true })

  return { isDark }
}

function applyTheme(dark) {
  const root = document.documentElement
  if (dark) {
    // Dark mode background with vibrant button colors
    root.style.setProperty('--bg-primary', '#0f172a')
    root.style.setProperty('--bg-secondary', '#111827')
    root.style.setProperty('--bg-tertiary', '#0b1220')
    root.style.setProperty('--text-primary', '#e2e8f0')
    root.style.setProperty('--text-secondary', '#cbd5e1')
    root.style.setProperty('--border-color', '#1f2937')
    // Button colors - Dark mode
    root.style.setProperty('--btn-primary', '#00a89d')       // Vibrant teal
    root.style.setProperty('--btn-primary-hover', '#008a84')
    root.style.setProperty('--btn-secondary', '#b8a89f')    // Sand/taupe
    root.style.setProperty('--btn-secondary-hover', '#a89a91')
    root.style.setProperty('--btn-danger', '#ff6b6b')       // Vibrant red
    root.style.setProperty('--btn-danger-hover', '#ff5252')
    root.style.setProperty('--btn-success', '#1e88e5')      // Vibrant navy/blue
    root.style.setProperty('--btn-success-hover', '#1565c0')
  } else {
    // Light mode background with vibrant button colors
    root.style.setProperty('--bg-primary', '#f8fafc')
    root.style.setProperty('--bg-secondary', '#f1f5f9')
    root.style.setProperty('--bg-tertiary', '#ffffff')
    root.style.setProperty('--text-primary', '#0f172a')
    root.style.setProperty('--text-secondary', '#334155')
    root.style.setProperty('--border-color', '#cbd5e1')
    // Button colors - Light mode
    root.style.setProperty('--btn-primary', '#00a89d')       // Vibrant teal
    root.style.setProperty('--btn-primary-hover', '#008a84')
    root.style.setProperty('--btn-secondary', '#9e8b81')    // Sand/taupe
    root.style.setProperty('--btn-secondary-hover', '#8e7b71')
    root.style.setProperty('--btn-danger', '#ff6b6b')       // Vibrant red
    root.style.setProperty('--btn-danger-hover', '#ff5252')
    root.style.setProperty('--btn-success', '#1e88e5')      // Vibrant navy/blue
    root.style.setProperty('--btn-success-hover', '#1565c0')
  }
}
