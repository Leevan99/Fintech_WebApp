<script setup>
import { onMounted, ref, computed } from 'vue'
import { authFetch } from '@/utils/api'
import { useCurrencyFormatter } from '@/composables/useCurrencyFormatter';
import Movimenti from '@/components/MovimentiConto.vue'
import { useAuthStore } from '@/stores/auth';
import { useMessageStore } from '@/stores/message';
import { useRouter } from 'vue-router';


const messageStore = useMessageStore()
const authStore = useAuthStore()
const utente = ref(null)
const error = ref(null)
const movimenti = ref(null)
const responseMovimenti = ref(null)
const user_id = ref(authStore.selectedUserId)
const nomeCompleto = ref(authStore.selectedUserName)
const codiceFiscale = ref("")
const apiPathMov = ref("movimenti/")
const apiPathUser = ref("user/")
const inesistente = ref(false)
const router = useRouter()

const { formatCurrency } = useCurrencyFormatter()
const formattedSaldo = computed(() => formatCurrency(utente.value.saldo));


async function fetchMovimenti() {
  try {
    error.value = null
    movimenti.value = null
    responseMovimenti.value = null
    const response = await authFetch(apiPathMov.value, {
      method: 'GET',
    })

    if (!response.ok) {
      throw new Error(`Errore HTTP: ${response.status}`)
    }

    if (response.status === 204) {
      responseMovimenti.value = response.status
      return
    }

    movimenti.value = await response.json()
    movimenti.value = await movimenti.value.reverse()
  } catch (err) {
    error.value = err.message
    console.error('Fetch error:', err)
  }
}

async function fetchUtente() {
  try {
    error.value = null
    utente.value = null
    const response = await authFetch(apiPathUser.value, {
      method: 'GET',
    })

    if (!response.ok) {
      throw new Error(`Errore HTTP: ${response.status}`)
    }

    utente.value = await response.json()
  } catch (err) {
    error.value = err.message
    console.error('Fetch error:', err)
  }
}

async function selezionaUtente() {
  if(user_id.value != null){
    authStore.setSelectedUserId(user_id.value, nomeCompleto.value)
  }
  if (authStore.selectedUserId){
    apiPathUser.value = `admin/user/${authStore.selectedUserId}/`
    apiPathMov.value = `admin/movimenti/${authStore.selectedUserId}/`
    fetchUtente()
    fetchMovimenti()
  }
}

async function fetchID() {
  try {
    error.value = null
    user_id.value = null
    const response = await authFetch("IDbyCF/", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: '*/*',
      },
      body: JSON.stringify({
        CF: codiceFiscale.value
      })
    })
    const data = await response.json()
    user_id.value = await data.ID
    nomeCompleto.value = await data.NomeCompleto
    selezionaUtente()
  } catch (err) {
    inesistente.value = true
    messageStore.setMessage("❌ L'utente ricercato non esiste, prova di nuovo")
    error.value = err.message
    console.error('Fetch error:', err)
  }

}


onMounted(() => {
  if (user_id.value && authStore.isAdmin){
    selezionaUtente()
  }else{
    fetchUtente()
    fetchMovimenti()
  }

})
</script>

<template>
  <section class="pagina-conto">
    <div v-if="(authStore.isAdmin && authStore.selectedUserId) || !authStore.isAdmin" class="container-conto-dashboard">
      <div v-if="utente" class="conto-container">
        <button v-if="authStore.isAdmin" class="setting" @click="router.push('/settings')">⚙️</button>
        <div class="riga">
          <div class="nome-conto">
            <h1>Nome: {{ utente.nome }} {{ utente.cognome }}</h1>
          </div>
          <h1 class="saldo">Saldo totale: {{ formattedSaldo }}</h1>
        </div>
      </div>
      <div v-else-if="inesistente" class="conto-container">
        <h1>❌ Utente inesistente</h1>
        <p>riprova cercandone un'altro</p>
      </div>
      <div v-else class="conto-container">Caricamento...</div>

      <div class="movimenti-container">
        <h2>Movimenti del conto:</h2>
        <div v-if="responseMovimenti === 204">
          <h3 style="color: #005f99;">Non hai ancora effettuato nessun movimento!</h3>
        </div>
        <div v-else-if="!movimenti">
          <h2>Caricamento movimenti...</h2>
        </div>
        <div v-else>
          <Movimenti v-for="movimento in movimenti" :key="movimento.id" :id="movimento.id" :dataMovimento="movimento.data" :importo="movimento.importo" :tipo="movimento.tipo" :iban-destinatario="movimento.iban_destinatario" :iban-mittente="movimento.iban_mittente" :causale="movimento.causale" />
        </div>
      </div>
    </div>
    <div v-else class="conto-container seleziona-conto">
      <h1 class="select-content">Non hai ancora selezionato nessun utente!</h1>
      <form @submit.prevent="fetchID">
        <h3 class="select-content">Inserisci il codice fiscale dell'utente da selezionare:</h3>
        <div>
          <input class="codice-fiscale" type="text" v-model="codiceFiscale" minlength="16" maxlength="16">
        </div>
        <input class="select-content" type="submit" value="Cerca">
      </form>
    </div>
  </section>
</template>


<style scoped>
.codice-fiscale{
  text-transform: uppercase;
}

.setting{
  position: absolute;
  top: 20%;
  right: 5%;
}

.container-conto-dashboard{
  width: 100%;
}

.seleziona-conto{
  margin-top: 25px !important;
  padding: 50px !important;
}

.select-content{
  padding: 10px;
}

input[type="text"]{
  font-size: larger;
  padding: 10px;
  border-radius: 20px;
  border: 3px solid #004d7c;
  outline: none;
  transition: all 0.2s linear;
  text-align: center;
}

input[type="text"]:focus-visible{
  box-shadow: 0px 0px 10px 1px #004d7c;
}

input[type="submit"]{
  margin-top: 10px;
  background-color: #004d7c;
  color: #fcfcfc;
  border: 2px solid #00385a;
  padding: 10px;
  border-radius: 20px;
  font-size: larger;
  cursor: pointer;
  box-shadow: 0px 0px 10px 1px #004d7c;
  transition: all 0.2s linear;
}

input[type="submit"]:hover{
  background-color: #004570;
  box-shadow: 0px 0px 20px 2px #004d7c;
}

input[type="submit"]:active{
  background-color: #001e31;
}

button {
  background-color: var(--nav-background);
  color: #fff;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  max-width: 200px;
  text-align: center;
  transition: background-color 0.3s;
  box-shadow: 1px 1px 10px 1px var(--nav-background);
}

button:hover {
  background-color: #005f99;
}

.nome-conto {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 10px;
}

.input-nome {
  padding: 5px;
  border-radius: 5px;
  border: 2px solid #005f99;
  width: 200px;
  font-size: larger;
  font-weight: bold;
  color: #004d7c;
  background-color: #fcfcfc;
  transition: border-color 0.3s;
}

.input-nome:focus {
  outline: none;
  border-color: #005f99;
  box-shadow: 0 0 5px #005f99;
}

.conto-container {
  display: flex;
  position: relative;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding: 20px 15%;
  margin: 10px 0 auto;
  border-radius: 20px;
  text-align: center;
  box-shadow: 1px 1px 50px -10px #9e8122;
  background-color: #c9a3277e;
}

.conto-container .riga {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 10px;
}

.conto-container h1 {
  color: rgb(0, 0, 75);
}

.conto-container .saldo {
  color: #117a65;
}

p {
  color: #005f99;
}

.movimenti-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 20px;
  width: 100%;
}

.movimenti-container h3,
.movimenti-container h2 {
  text-align: center;
  margin-bottom: 20px;
}

.pagina-conto {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 0 10%;
}
</style>
