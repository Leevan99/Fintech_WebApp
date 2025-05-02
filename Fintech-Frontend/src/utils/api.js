import { useAuthStore } from '@/stores/auth'
import router from '@/router'

export async function authFetch(url, options = {}) {
  const authStore = useAuthStore()
  const BASE_URL = (import.meta.env.VITE_API_URL || 'http://localhost:5000/') + 'api/v1/'
  const fullUrl = `${BASE_URL}${url}`

  // Salta controllo token e redirect per la chiamata di logout
  const isLogoutCall = url.includes('logout')
  if (!isLogoutCall && !authStore.checkAuth()) {
    authStore.clearToken()
    router.push('/logout')
    throw new Error('Token scaduto o non valido')
  }

  // Gestione automatica del body JSON
  if (options.body && typeof options.body === 'object') {
    options.body = JSON.stringify(options.body)
    options.headers = {
      'Content-Type': 'application/json',
      ...options.headers
    }
  }

  const response = await fetch(fullUrl, {
    ...options,
    headers: {
      'Authorization': `Bearer ${authStore.token}`,
      ...options.headers
    }
  })

  // Gestione 401: per logout non lanciare errore, per le altre chiamate reindirizza
  if (response.status === 401) {
    authStore.clearToken()
    if (!isLogoutCall) {
      router.push('/logout')
      throw new Error('Sessione scaduta')
    }
    // per logout, ritorna tranquillamente la response senza throw
    return response
  }

  // Gestione altri errori HTTP
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.message || `Errore HTTP! Status: ${response.status}`)
  }

  return response
}
