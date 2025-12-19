const AUTH_URL = import.meta.env.VITE_AUTH_URL || 'http://127.0.0.1:5005'

export function isAuthenticated(){
  return !!localStorage.getItem('access_token')
}

export function clearAuth(){
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
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
      localStorage.setItem('access_token', data.access_token)
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
