import { defineStore } from 'pinia'
import { ref, computed} from 'vue'
import { useRouter } from 'vue-router'
import { useMessageStore } from './message'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(null)
  const router = useRouter()
  let expirationTimer = null
  const isAdmin = ref(false)
  const messageStore = useMessageStore()

  const selectedUserId = ref(null)
  const selectedUserName = ref(null)

  const setSelectedUserId = (id, nome) => {
    if (id) {
      selectedUserId.value = id
      document.cookie = `selectedUserId=${id}; path=/; max-age=86400` // 1 giorno
      selectedUserName.value = nome
      document.cookie = `selectedUserName=${nome}; path=/; max-age=86400` // 1 giorno
    } else {
      clearSelectedUserId()
      messageStore.setMessage("❌ Hai inserito un valore non valido")
    }
  }

  const clearSelectedUserId = () => {
    selectedUserId.value = null
    document.cookie = 'selectedUserId=; Max-Age=0; path=/'
    document.cookie = 'selectedUserName=; Max-Age=0; path=/'
    router.push('/dashboard')
  }


  // Recupera token e stato isAdmin dai cookie
  const getCookie = (name) => {
    const value = `; ${document.cookie}`
    const parts = value.split(`; ${name}=`)
    if (parts.length === 2) return parts.pop().split(';').shift()
  }

  // Aggiungi un getter per verificare se il token è scaduto
  const isTokenExpired = computed(() => {
    if (!token.value) return true
    const payload = JSON.parse(atob(token.value.split('.')[1]))
    return payload.exp * 1000 < Date.now()
  })

  // Inizializza lo store recuperando i valori dai cookie
  const initialize = () => {
    const cookieToken = getCookie('access_token')
    const cookieIsAdmin = getCookie('isAdmin') === 'true'
    const cookieUserId = getCookie('selectedUserId')
    const cookieUserNome = getCookie('selectedUserName')

    if (cookieToken && !isTokenExpired.value) {
      token.value = cookieToken
      isAdmin.value = cookieIsAdmin
    }

    if (cookieUserId, cookieUserNome) {
      selectedUserId.value = cookieUserId
      selectedUserName.value = cookieUserNome
    }
  }


  const setToken = (newToken, is_admin) => {
    token.value = newToken;

    // Se is_admin è undefined, prova a leggerlo dal cookie
    if (typeof is_admin === 'undefined') {
      const cookieIsAdmin = getCookie("isAdmin");
      isAdmin.value = cookieIsAdmin === 'true';
    } else {
      isAdmin.value = is_admin;
    }

    try {
      const payload = JSON.parse(atob(newToken.split('.')[1]));
      const expiresAt = payload.exp * 1000;
      const maxAge = Math.floor((expiresAt - Date.now()) / 1000);
      // Imposta il cookie dell'access token
      document.cookie = `access_token=${newToken}; max-age=${maxAge}; path=/`;
      // Imposta anche il cookie per isAdmin
      document.cookie = `isAdmin=${is_admin !== undefined ? (is_admin ? 'true' : 'false') : (isAdmin.value ? 'true' : 'false')}; max-age=${maxAge}; path=/`;
      if (expirationTimer) clearTimeout(expirationTimer);
      expirationTimer = setTimeout(clearToken, expiresAt - Date.now());
    } catch (err) {
      console.error("Errore nel parsing del nuovo token", err);
    }
  }


  const clearToken = () => {
    token.value = null
    isAdmin.value = false
    selectedUserId.value = null
    document.cookie = 'access_token=; Max-Age=0; path=/'
    document.cookie = 'isAdmin=; Max-Age=0; path=/'
    document.cookie = 'selectedUserId=; Max-Age=0; path=/'
    document.cookie = 'selectedUserName=; Max-Age=0; path=/'
    router.push('/login')
  }

  // Aggiungi un metodo per verificare il token
  const checkAuth = async () => {
    if (isTokenExpired.value) {
      clearToken()
      return false
    }
    return true
  }

  // Inizializza lo store al crearlo
  initialize()

  return {
    token,
    isAdmin,
    setToken,
    clearToken,
    checkAuth,
    isTokenExpired,
    selectedUserId,
    selectedUserName,
    setSelectedUserId,
    clearSelectedUserId,
    initialize,
    getCookie
  }
})
