<template>
  <section>
    <h2>Admin Login</h2>
    <div class="card">
      <label>Email</label>
      <input class="input" v-model="email" type="email" placeholder="you@example.com" />
      <label style="margin-top:8px">Password</label>
      <div class="password-row">
        <input
          class="input"
          v-model="password"
          :type="showPassword ? 'text' : 'password'"
          placeholder="••••••••"
        />
        <button type="button" class="toggle" @click="showPassword = !showPassword">
          {{ showPassword ? 'Hide' : 'Show' }}
        </button>
      </div>
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
const showPassword = ref(false)

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

<style scoped>
.password-row {
  display: flex;
  gap: 8px;
  align-items: center;
}

.password-row .input {
  flex: 1;
}

.toggle {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: #f9fafb;
  cursor: pointer;
  font-weight: 600;
}
</style>
