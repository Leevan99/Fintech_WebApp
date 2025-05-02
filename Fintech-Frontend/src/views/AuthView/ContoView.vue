<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { authFetch } from '@/utils/api'
import { useCurrencyFormatter } from '@/composables/useCurrencyFormatter';
import Movimenti from '@/components/MovimentiConto.vue'
import { useMessageStore } from '@/stores/message';
import { useAuthStore } from '@/stores/auth';
import ConfermaPopup from '@/components/ConfermaPopup.vue'


const authStore = useAuthStore()
const messageStore = useMessageStore()
const route = useRoute()
const id_conto = ref(route.params.id)
const conto = ref(null)
const error = ref(null)
const movimenti = ref(null)
const responseMovimenti = ref(null)
const modNome = ref(false)
const newName = ref('')
const router = useRouter()
const mostra = ref(false)

const { formatCurrency } = useCurrencyFormatter()
const formattedSaldo = computed(() => formatCurrency(conto.value.saldo));

const formattedDate = computed(() => {
  const date = new Date(conto.value.data_creazione);
  return new Intl.DateTimeFormat('it-IT', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  }).format(date);
});

async function fetchMovimenti() {
  try {
    error.value = null
    const response = await authFetch(`conto/movimenti/${id_conto.value}/`, {
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
    movimenti.value = movimenti.value.reverse()
  } catch (err) {
    error.value = err.message
    console.error('Fetch error:', err)
  }
}

async function fetchConto() {
  try {
    modNome.value = false
    error.value = null
    const response = await authFetch(`conto/${id_conto.value}/`, {
      method: 'GET',
    })

    if (!response.ok) {
      throw new Error(`Errore HTTP: ${response.status}`)
    }

    conto.value = await response.json()
    newName.value = conto.value.nome
  } catch (err) {
    error.value = err.message
    console.error('Fetch error:', err)
  }
}

async function modificaNome() {
  try {
    const response = await authFetch(`conto/${id_conto.value}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        Accept: '*/*',
      },
      body: JSON.stringify({
        nome: newName.value,
      }),
    })

    if (!response.ok) {
      throw new Error(`Errore HTTP: ${response.status}`)
    }

    conto.value.nome = newName.value
    modNome.value = false
  } catch (err) {
    if (err.message.includes('409')) {
      messageStore.setMessage('⚠️ Nome già in uso su un\'altro conto a te intestato, scegli un altro nome')
    } else {
      messageStore.setMessage('❌ Errore durante la modifica del nome del conto')
    }
  }
}

async function eliminaConto() {
  try {
    const response = await authFetch(`conto/${id_conto.value}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        Accept: '*/*',
      }
    })

    if (response.ok){
      mostra.value = false
      messageStore.setMessage('✅ Conto eliminato con successo')
      router.push("/conti")
    }

  } catch (err) {
    console.error(err)
    if (err.message.includes('non esiste')) {
      messageStore.setMessage('⚠️ Il conto che stai cercando di eliminare non esiste')
    } else if (err.message.includes('saldo diverso da zero')) {
      messageStore.setMessage('❌ Non puoi eliminare un conto con saldo diverso da ZERO!')
    } else {
      messageStore.setMessage('❌ Non puoi eliminare il conto principale!')
    }
  }
}


onMounted(() => {
  fetchConto()
  fetchMovimenti()
})
</script>

<template>
  <section class="pagina-conto">
    <div v-if="conto" class="conto-container">
      <div class="riga">
        <div v-if="modNome === false" class="nome-conto">
          <h1>Nome: {{ conto.nome }}</h1><button @click="modNome = true" v-if="conto.nome !== 'Conto Principale'">Modifica</button>
        </div>
        <div v-else-if="modNome" class="nome-conto">
          <h1>Nome: </h1>
          <input v-model="newName" @keyup.enter="modificaNome()" type=" text" placeholder="Nome conto" class="input-nome" maxlength="16" />
          <button @click="modificaNome()">Salva</button>
          <button @click="modNome = false">Annulla</button>
        </div>
        <h1 class="saldo">Saldo: {{ formattedSaldo }}</h1>
      </div>
      <div class="riga">
        <h3>N° conto: {{ conto.numero_conto }}</h3>
        <h3>IBAN: {{ conto.iban }}</h3>
      </div>
      <p>Conto creato in data: {{ formattedDate }}</p>
      <button v-if="authStore.isAdmin && conto.nome != 'Conto Principale'" @click="mostra = true">Elimina Conto</button>
    </div>

    <div v-else>Caricamento...</div>

    <div class="movimenti-container">
      <h2>Movimenti del conto:</h2>
      <div v-if="responseMovimenti === 204">
        <h3 style="color: #005f99;">Non hai ancora effettuato movimenti per questo conto!</h3>
      </div>
      <div v-else-if="!movimenti">
        <h2>Caricamento movimenti...</h2>
      </div>
      <div v-else>
        <Movimenti v-for="movimento in movimenti" :key="movimento.id" :id="movimento.id" :dataMovimento="movimento.data" :importo="movimento.importo" :tipo="movimento.tipo" :iban-destinatario="movimento.iban_destinatario" :iban-mittente="movimento.iban_mittente" :causale="movimento.causale" />
      </div>
    </div>
    <ConfermaPopup :visibile="mostra" @chiudi="mostra = false" @elimina="eliminaConto" />
  </section>
</template>


<style scoped>
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

