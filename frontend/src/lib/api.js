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

// Skills write API
export async function postSkill(payload){
  return apiPost('/api/skills', payload)
}
export async function putSkill(id, payload){
  return apiPut(`/api/skills/${id}`, payload)
}
export async function deleteSkill(id){
  return apiDelete(`/api/skills/${id}`)
}

// Education write API
export async function postEducation(payload){
  return apiPost('/api/education', payload)
}
export async function putEducation(id, payload){
  return apiPut(`/api/education/${id}`, payload)
}
export async function deleteEducation(id){
  return apiDelete(`/api/education/${id}`)
}

// Work write API
export async function postWork(payload){
  return apiPost('/api/work', payload)
}
export async function putWork(id, payload){
  return apiPut(`/api/work/${id}`, payload)
}
export async function deleteWork(id){
  return apiDelete(`/api/work/${id}`)
}

// Projects write API
export async function postProject(payload){
  return apiPost('/api/projects', payload)
}
export async function putProject(id, payload){
  return apiPut(`/api/projects/${id}`, payload)
}
export async function deleteProject(id){
  return apiDelete(`/api/projects/${id}`)
}

// Community write API
export async function postCommunity(payload){
  return apiPost('/api/community', payload)
}
export async function putCommunity(id, payload){
  return apiPut(`/api/community/${id}`, payload)
}
export async function deleteCommunity(id){
  return apiDelete(`/api/community/${id}`)
}

// Proficiency Levels (read via composite service)
export async function getProfLevels(){
  return apiGet('/api/prof-levels')
}

// E-Portfolio write API
export async function postEPortfolio(payload){
  return apiPost('/api/e-portfolio', payload)
}
export async function putEPortfolio(id, payload){
  return apiPut(`/api/e-portfolio/${id}`, payload)
}
export async function deleteEPortfolio(id){
  return apiDelete(`/api/e-portfolio/${id}`)
}

// E-Portfolio file upload (artefacts_evidence_files as hex)
export async function uploadEPortfolioFile(id, file){
  const form = new FormData()
  form.append('file', file)
  const res = await fetch(`${API_URL}/api/e-portfolio/${id}/upload`,{
    method:'POST',
    headers:{ ...authHeader() },
    body: form
  })
  if(!res.ok) throw new Error('Request failed')
  return await res.json()
}

// Clear uploaded file
export async function clearEPortfolioFile(id){
  const form = new FormData()
  form.append('clear','true')
  const res = await fetch(`${API_URL}/api/e-portfolio/${id}/upload`,{
    method:'POST',
    headers:{ ...authHeader() },
    body: form
  })
  if(!res.ok) throw new Error('Request failed')
  return await res.json()
}
