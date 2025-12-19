import { createRouter, createWebHistory } from 'vue-router'
import Skills from '../pages/Skills.vue'
import Work from '../pages/Work.vue'
import Education from '../pages/Education.vue'
import Projects from '../pages/Projects.vue'
import Login from '../pages/Login.vue'

const routes = [
  { path: '/', redirect: '/skills' },
  { path: '/skills', component: Skills },
  { path: '/experience', component: Work },
  { path: '/education', component: Education },
  { path: '/other-information', component: Projects },
  { path: '/login', component: Login }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
