import { ref, computed } from 'vue'

// Prefer explicit VITE_AUTH_URL; otherwise fall back to the composite API base.
const AUTH_URL =
  import.meta.env.VITE_AUTH_URL ||
  import.meta.env.VITE_API_URL ||
  'http://127.0.0.1:8000'

// Reactive auth token state shared across app
export const authToken = ref(localStorage.getItem('access_token'))
export const isAuthed = computed(() => !!authToken.value)

function setAccessToken(token){
  authToken.value = token || null
  if(token){
    localStorage.setItem('access_token', token)
  } else {
    localStorage.removeItem('access_token')
  }
  // Broadcast a lightweight event for any non-Vue listeners
  window.dispatchEvent(new CustomEvent('auth:changed', { detail: { authed: !!token } }))
}

export function clearAuth(){
  setAccessToken(null)
  localStorage.removeItem('refresh_token')
}

// Validate token with auth server
export async function validateToken(token){
  if(!token) return false
  try{
    const res = await fetch(`${AUTH_URL}/auth/validate`,{
      method:'POST',
      headers:{ 'Content-Type':'application/json', 'Authorization': `Bearer ${token}` }
    })
    return res.ok
  }catch(err){
    console.warn('Token validation error:', err)
    return false
  }
}

// Try to refresh token if available
export async function tryRefreshToken(){
  const refreshToken = localStorage.getItem('refresh_token')
  if(!refreshToken) return false
  try{
    const res = await fetch(`${AUTH_URL}/auth/refresh`,{
      method:'POST',
      headers:{ 'Content-Type':'application/json' },
      body: JSON.stringify({ refresh_token: refreshToken })
    })
    if(!res.ok) return false
    const data = await res.json()
    if(data.access_token){
      setAccessToken(data.access_token)
      if(data.refresh_token){
        localStorage.setItem('refresh_token', data.refresh_token)
      }
      return true
    }
    return false
  }catch(err){
    console.warn('Token refresh error:', err)
    return false
  }
}

// Initialize auth on app startup - checks token validity
export async function initializeAuth(){
  const token = authToken.value
  if(!token){
    return false
  }
  
  // Try to validate the current token
  const isValid = await validateToken(token)
  if(isValid){
    return true
  }
  
  // If invalid, try to refresh it
  const refreshed = await tryRefreshToken()
  if(refreshed){
    return true
  }
  
  // If all else fails, clear auth
  clearAuth()
  return false
}

export async function logout(){
  const token = authToken.value
  try{
    await fetch(`${AUTH_URL}/auth/logout`,{
      method:'POST', headers:{ ...(token?{ Authorization: `Bearer ${token}` }:{} ) }
    })
  }catch(err){
    console.warn('logout error', err)
  }finally{
    clearAuth()
  }
}

export async function login(email, password){
  try{
    const res = await fetch(`${AUTH_URL}/auth/login`,{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ email, password })
    })
    if(!res.ok) return false
    const data = await res.json()
    if(data.access_token){
      setAccessToken(data.access_token)
      if(data.refresh_token){
        localStorage.setItem('refresh_token', data.refresh_token)
      }
      return true
    }
    return false
  }catch(err){
    console.error('login error', err)
    return false
  }
}

// Back-compat function; prefer using `isAuthed` directly
export function isAuthenticated(){
  return isAuthed.value
}
