import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import ContiView from '@/views/AuthView/ContiView.vue'
import LogoutView from '@/views/AuthView/LogoutView.vue'
import BonificoView from '@/views/AuthView/BonificoView.vue'
import ContoView from '@/views/AuthView/ContoView.vue'
import RegistratiView from '@/views/RegistratiView.vue'
import ATMView from '@/views/AuthView/ATMView.vue'
import DashboardView from '@/views/AuthView/DashboardView.vue'
import SettingsView from '@/views/AuthView/SettingsView.vue'
import AboutView from '../views/AboutView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: false }
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView,
      meta: { requiresAuth: false }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true }
    },
    {
      path: '/conti',
      name: 'conti',
      component: ContiView,
      meta: { requiresAuth: true }
    },
    {
      path: '/bonifico',
      name: 'bonifico',
      component: BonificoView,
      meta: { requiresAuth: true }
    },
    {
      path: '/conto/:id',
      name: 'VisualizzaConto',
      component: ContoView,
      meta: { requiresAuth: true },
    },
    {
      path: '/ATM',
      name: 'ATM',
      component: ATMView,
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresAuth: false }
    },
    {
      path: '/apri-conto',
      name: 'apriConto',
      component: RegistratiView,
    },
    {
      path: '/logout',
      name: 'logout',
      component: LogoutView,
      meta: { requiresAuth: true }
    },
    {
      path: '/settings',
      name: 'settings',
      component: SettingsView,
      meta: { requiresAuth: true }
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Verifica se la route richiede autenticazione
  if (to.matched.some(record => record.meta.requiresAuth)) {
    authStore.checkAuth()
  }

  // Se già loggato e prova ad accedere al login
  if ((to.name === 'login' || to.name === 'home' || to.name === 'about') && authStore.token && !authStore.isTokenExpired) {
    next({ name: 'dashboard' })
    return
  }

  next()
})

export default router
