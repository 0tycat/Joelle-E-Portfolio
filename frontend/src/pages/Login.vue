<template>
  <section>
    <h2>Admin Login</h2>
    <div class="card">
      <label>Email</label>
      <input class="input" v-model="email" type="email" placeholder="you@example.com" />
      <label style="margin-top:8px">Password</label>
      <input class="input" v-model="password" type="password" placeholder="••••••••" />
      <div style="margin-top:12px">
        <button class="btn" @click="login">Login</button>
      </div>
      <p v-if="error" style="color:#fca5a5">{{ error }}</p>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login as loginApi, isAuthenticated } from '../lib/auth.js'

const router = useRouter()
const email = ref('')
const password = ref('')
const error = ref('')

async function login(){
  error.value = ''
  const ok = await loginApi(email.value, password.value)
  if(ok){
    router.push('/skills')
  } else {
    error.value = 'Login failed. Check credentials.'
  }
}

if(isAuthenticated()){
  router.push('/skills')
}
</script>
