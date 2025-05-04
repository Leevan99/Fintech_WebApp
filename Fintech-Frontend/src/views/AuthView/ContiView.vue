<script setup>
import { onMounted, ref } from 'vue'
import { authFetch } from '@/utils/api'
import CardConto from '@/components/CardConto.vue'
import { useMessageStore } from '@/stores/message'
import ContoPopup from '@/components/ContoPopup.vue'
import { useAuthStore } from '@/stores/auth'

const conti = ref([])
const error = ref(null)
const mostra = ref(false)
const messageStore = useMessageStore()
const authStore = useAuthStore()
const apiPathUser = ref("conti/")

async function fetchConti() {
  try {
    conti.value = []
    error.value = null

    const response = await authFetch(apiPathUser.value, { method: "GET" })

    if (response.status === 204) {
      createConto()
      return
    }

    conti.value = await response.json()

  } catch (err) {
    if (err.message.includes("Non sei autorizzato a fare quest'operazione")){
      fetchConti("")
    }
    error.value = err.message
    console.error('Fetch error:', err)
  }
}

async function createConto(customName) {
  try {
    const newNome = customName?.trim() || "Conto Principale";

    const response = await authFetch(apiPathUser.value, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        nome: newNome,
      }),
    });
    mostra.value = false
    fetchConti()
    return response;

  } catch (error) {
    if (error.message.includes('409')){
      messageStore.setMessage("❌ Campo vuoto o nome conto già utilizzato", 3000)
    } else if (error.message.includes('403')){
      messageStore.setMessage("❌ Hai già raggiunto il numero massimo di conti", 3000)
    } else {
      messageStore.setMessage("❌ Non sei autorizzato a fare quest'operazione", 3000)
    }
    console.error("Failed to create conto:", error);
    throw error;
  }
}

onMounted(() => {
  if (authStore.selectedUserId) {
    apiPathUser.value = `conti/${authStore.selectedUserId}/`
  }
  fetchConti()
})
</script>

<template>
  <div class="conti-container">
    <div class="sub-container">
      <CardConto class="conto" v-for="conto in conti" :key="conto.id" :id="conto.id" :nome-conto="conto.nome" :numero-conto="conto.numero_conto" :saldo="conto.saldo" :iban="conto.iban" :dataCreazione="conto.data_creazione" />
      <div v-if="conti.length < 5 && conti.length > 0" class="addConto">
        <h2>Apri un altro conto<span v-if="authStore.isAdmin"> all'utente</span></h2>
        <button class="apri-conto-btn" @click="mostra = true">Apri conto</button>
      </div>
      <div v-else>

      </div>
      <ContoPopup :visibile="mostra" @chiudi="mostra = false" @crea="createConto" />
    </div>
  </div>

</template>

<style scoped>

.sub-container{
  display: flex;
  max-width: 80%;
}

.error {
  color: red;
  font-weight: bold;
}

.addConto {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.apri-conto-btn {
  color: aliceblue !important;
  background-color: #126b00 !important;
  border: #0b4200 solid 1px !important;
  box-shadow: 0 0 10px 1px #126b00 !important;
  transition: all 0.2s ease;
}

.apri-conto-btn:hover{
  box-shadow: 0 0 30px 5px #126b00 !important;
  padding: 13px !important;
}

.conti-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 2rem;
  min-height: 50vh;
}

.conti-container button {
  padding: 10px;
  background-color: var(--nav-background);
  border-radius: 10px;
  color: #d6a70a;
  font-size: larger;
  font-weight: 600;
  margin-top: 1rem;
  cursor: pointer;
  border: 2px outset #000f20
}

.conti-container button:hover {
  box-shadow: 0 0 20px 2px;
  opacity: 0.9;
}

.conti-container>div {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.conti-exists {
  text-align: center;
}
</style>
