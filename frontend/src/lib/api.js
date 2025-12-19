const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

function authHeader(){
  const token = localStorage.getItem('access_token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export async function apiGet(path){
  const res = await fetch(`${API_URL}${path}`,{ headers: { ...authHeader() } })
  if(!res.ok) throw new Error('Request failed')
  return await res.json()
}

export async function apiPost(path, body){
  const res = await fetch(`${API_URL}${path}`,{
    method:'POST',
    headers:{ 'Content-Type':'application/json', ...authHeader() },
    body: JSON.stringify(body)
  })
  if(!res.ok) throw new Error('Request failed')
  return await res.json()
}

export async function apiPut(path, body){
  const res = await fetch(`${API_URL}${path}`,{
    method:'PUT',
    headers:{ 'Content-Type':'application/json', ...authHeader() },
    body: JSON.stringify(body)
  })
  if(!res.ok) throw new Error('Request failed')
  return await res.json()
}

export async function apiDelete(path){
  const res = await fetch(`${API_URL}${path}`,{
    method:'DELETE',
    headers:{ ...authHeader() }
  })
  if(!res.ok) throw new Error('Request failed')
  return await res.json()
}
