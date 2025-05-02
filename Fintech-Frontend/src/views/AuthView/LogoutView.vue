<script setup>
import { onMounted, ref } from 'vue'
import { authFetch } from '@/utils/api'
import { useMessageStore } from '@/stores/message'
import { useRouter } from 'vue-router'

const error = ref(null)
const messageStore = useMessageStore()
const router = useRouter()

async function logout() {
  try {
    const response = await authFetch('logout/', { method: 'POST' })
    if (!response.ok) {
      throw new Error(`Logout fallito: ${response.status}`)
    }
    messageStore.setMessage('ℹ️ Logout effettuato con successo!', 3000)
    await router.push('/')
  } catch (err) {
    error.value = err.message
    console.error('Errore logout:', err)
  }
}

onMounted(() => {
  logout()
})
</script>

<template>
  <div class="logout-view">
    <template v-if="!error">
      <div class="spinner-container">
        <div class="spinner"></div>
        <p>Effettuando logout…</p>
      </div>
    </template>
    <p v-else class="error">{{ error }}</p>
  </div>
</template>

<style scoped>
.logout-view {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 50vh;
  flex-direction: column;
}

.spinner-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-top-color: #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error {
  color: red;
  font-weight: bold;
}
</style>
