import { ref, watch } from 'vue'

const stored = localStorage.getItem('theme')
const prefersDark = typeof window !== 'undefined' && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
const isDark = ref(stored ? stored === 'dark' : prefersDark)

export function useTheme() {
  watch(isDark, (newVal) => {
    localStorage.setItem('theme', newVal ? 'dark' : 'light')
    applyTheme(newVal)
  }, { immediate: true })

  const toggleTheme = () => {
    isDark.value = !isDark.value
  }

  return { isDark, toggleTheme }
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
    root.style.setProperty('--hex-pattern-color', 'rgba(180, 150, 40, 0.35)')
    root.style.setProperty('--bg-gradient-start', '#0f172a')
    root.style.setProperty('--bg-gradient-end', '#0a2540')
    // Header card colors - Dark mode
    root.style.setProperty('--header-card-bg', 'linear-gradient(135deg, #0d4a4a 0%, #1a6b6b 100%)')
    root.style.setProperty('--header-card-text', '#e2e8f0')
    root.style.setProperty('--motto-text', '#d4af37')
    root.style.setProperty('--value-item-heading', '#e2e8f0')
    root.style.setProperty('--value-item-text', 'rgba(226, 232, 240, 0.9)')
    root.style.setProperty('--read-more-btn-color', '#4dd9d5')
    // Card colors - Dark mode
    root.style.setProperty('--card-bg', '#1a2332')
    root.style.setProperty('--card-text', '#e2e8f0')
    root.style.setProperty('--card-text-secondary', '#cbd5e1')
    root.style.setProperty('--card-border', '#2d3e52')
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
    root.style.setProperty('--hex-pattern-color', 'rgba(180, 150, 40, 0.25)')
    root.style.setProperty('--bg-gradient-start', '#ffffff')
    root.style.setProperty('--bg-gradient-end', '#69c0fa')
    // Header card colors - Light mode
    root.style.setProperty('--header-card-bg', 'linear-gradient(135deg, #20b2aa 0%, #48d1cc 100%)')
    root.style.setProperty('--header-card-text', '#ffffff')
    root.style.setProperty('--motto-text', '#d4af37')
    root.style.setProperty('--value-item-heading', '#000000')
    root.style.setProperty('--value-item-text', 'rgba(0, 0, 0, 0.85)')
    root.style.setProperty('--read-more-btn-color', '#2d5a47')
    // Card colors - Light mode
    root.style.setProperty('--card-bg', '#ffffff')
    root.style.setProperty('--card-text', '#0f172a')
    root.style.setProperty('--card-text-secondary', '#475569')
    root.style.setProperty('--card-border', '#e2e8f0')
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
