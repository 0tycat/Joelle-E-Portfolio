import { createRouter, createWebHistory } from 'vue-router'
import Skills from '../pages/Skills.vue'
import Work from '../pages/Work.vue'
import Education from '../pages/Education.vue'
import Projects from '../pages/Projects.vue'
import EPortfolio from '../pages/EPortfolio.vue'
import Community from '../pages/Community.vue'
import Login from '../pages/Login.vue'

const routes = [
  { path: '/', redirect: '/portfolio' },
  { path: '/portfolio', component: EPortfolio },
  { path: '/education', component: Education },
  { path: '/skills', component: Skills },
  { path: '/experience', component: Work },
  { path: '/community', component: Community },
  { path: '/interests', component: Projects },
  { path: '/login', component: Login },
  { path: '/:pathMatch(.*)*', redirect: '/portfolio' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
