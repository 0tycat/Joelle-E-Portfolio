import { ref, computed } from 'vue'

const AUTH_URL = import.meta.env.VITE_AUTH_URL || 'http://127.0.0.1:5005'

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
