const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
// Atomic services
const SKILLS_URL = import.meta.env.VITE_SKILLS_URL || 'http://127.0.0.1:5000'
const EDUCATION_URL = import.meta.env.VITE_EDU_URL || 'http://127.0.0.1:5001'
const WORK_URL = import.meta.env.VITE_WORK_URL || 'http://127.0.0.1:5002'
const COMMUNITY_URL = import.meta.env.VITE_COMM_URL || 'http://127.0.0.1:5003'
const PROJECTS_URL = import.meta.env.VITE_PROJ_URL || 'http://127.0.0.1:5004'

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

// Skills write API
export async function postSkill(payload){
  const res = await fetch(`${SKILLS_URL}/skills`,{
    method:'POST', headers:{ 'Content-Type':'application/json', ...authHeader() }, body: JSON.stringify(payload)
  })
  if(!res.ok) throw new Error('Request failed')
  return await res.json()
}
export async function putSkill(id, payload){
  const res = await fetch(`${SKILLS_URL}/skills/${id}`,{
    method:'PUT', headers:{ 'Content-Type':'application/json', ...authHeader() }, body: JSON.stringify(payload)
  })
  if(!res.ok) throw new Error('Request failed')
  return await res.json()
}
export async function deleteSkill(id){
  const res = await fetch(`${SKILLS_URL}/skills/${id}`,{ method:'DELETE', headers:{ ...authHeader() } })
  if(!res.ok) throw new Error('Request failed')
  return await res.json()
}

// Education write API
export async function postEducation(payload){
  const res = await fetch(`${EDUCATION_URL}/education`,{
    method:'POST', headers:{ 'Content-Type':'application/json', ...authHeader() }, body: JSON.stringify(payload)
  })
  if(!res.ok) throw new Error('Request failed')
  return await res.json()
}
export async function putEducation(id, payload){
  const res = await fetch(`${EDUCATION_URL}/education/${id}`,{
    method:'PUT', headers:{ 'Content-Type':'application/json', ...authHeader() }, body: JSON.stringify(payload)
  })
  if(!res.ok) throw new Error('Request failed')
  return await res.json()
}
export async function deleteEducation(id){
  const res = await fetch(`${EDUCATION_URL}/education/${id}`,{ method:'DELETE', headers:{ ...authHeader() } })
  if(!res.ok) throw new Error('Request failed')
  return await res.json()
}

// Work write API
export async function postWork(payload){
  const res = await fetch(`${WORK_URL}/work`,{
    method:'POST', headers:{ 'Content-Type':'application/json', ...authHeader() }, body: JSON.stringify(payload)
  })
  if(!res.ok) throw new Error('Request failed')
  return await res.json()
}
export async function putWork(id, payload){
  const res = await fetch(`${WORK_URL}/work/${id}`,{
    method:'PUT', headers:{ 'Content-Type':'application/json', ...authHeader() }, body: JSON.stringify(payload)
  })
  if(!res.ok) throw new Error('Request failed')
  return await res.json()
}
export async function deleteWork(id){
  const res = await fetch(`${WORK_URL}/work/${id}`,{ method:'DELETE', headers:{ ...authHeader() } })
  if(!res.ok) throw new Error('Request failed')
  return await res.json()
}

// Projects write API
export async function postProject(payload){
  const res = await fetch(`${PROJECTS_URL}/projects`,{
    method:'POST', headers:{ 'Content-Type':'application/json', ...authHeader() }, body: JSON.stringify(payload)
  })
  if(!res.ok) throw new Error('Request failed')
  return await res.json()
}
export async function putProject(id, payload){
  const res = await fetch(`${PROJECTS_URL}/projects/${id}`,{
    method:'PUT', headers:{ 'Content-Type':'application/json', ...authHeader() }, body: JSON.stringify(payload)
  })
  if(!res.ok) throw new Error('Request failed')
  return await res.json()
}
export async function deleteProject(id){
  const res = await fetch(`${PROJECTS_URL}/projects/${id}`,{ method:'DELETE', headers:{ ...authHeader() } })
  if(!res.ok) throw new Error('Request failed')
  return await res.json()
}

// Community write API
export async function postCommunity(payload){
  const res = await fetch(`${COMMUNITY_URL}/community`,{
    method:'POST', headers:{ 'Content-Type':'application/json', ...authHeader() }, body: JSON.stringify(payload)
  })
  if(!res.ok) throw new Error('Request failed')
  return await res.json()
}
export async function putCommunity(id, payload){
  const res = await fetch(`${COMMUNITY_URL}/community/${id}`,{
    method:'PUT', headers:{ 'Content-Type':'application/json', ...authHeader() }, body: JSON.stringify(payload)
  })
  if(!res.ok) throw new Error('Request failed')
  return await res.json()
}
export async function deleteCommunity(id){
  const res = await fetch(`${COMMUNITY_URL}/community/${id}`,{ method:'DELETE', headers:{ ...authHeader() } })
  if(!res.ok) throw new Error('Request failed')
  return await res.json()
}
