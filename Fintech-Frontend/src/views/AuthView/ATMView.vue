<script setup>
import { onMounted, ref } from 'vue'
import { authFetch } from '@/utils/api'
import { useMessageStore } from '@/stores/message'
import CurrencyInput from '@/components/CurrencyInput.vue';
import { useCurrencyFormatter } from '@/composables/useCurrencyFormatter';
import { computed } from 'vue';
import { useAuthStore } from '@/stores/auth';


const authStore = useAuthStore()
const { formatCurrency } = useCurrencyFormatter();
const operazione = ref('deposito')
const importoFormat = ref('');
const importoNumerico = ref('');
const messageStore = useMessageStore()
const jsonOperazione = ref(null)
const conti = ref(null)
const error = ref(null)
const id_conto = ref(null)
const page = ref(0);
const responseATM = ref(null)
const saldoFormattato = computed(() => {
const conto = conti.value?.find(conto => conto.id === id_conto.value);
  return conto ? formatCurrency(conto.saldo) : "Caricamento...";
});
const apiPathUser = ref("conti/")



async function fetchConti() {
  try {

    conti.value = null
    error.value = null

    const response = await authFetch(apiPathUser.value, { method: "GET" });

    conti.value = await response.json()
    id_conto.value = conti.value[0].id

  } catch (err) {
    error.value = err.message
    console.error('Fetch error:', err)
  }
}


async function fetchConto() {
  try {

    let conto = null
    error.value = null

    const response = await authFetch(`conto/${id_conto.value}/`, { method: "GET" });

    conto = await response.json()
    conti.value[conti.value.findIndex(conto => conto.id === id_conto.value)] = conto

  } catch (err) {
    error.value = err.message
    console.error('Fetch error:', err)
  }
}

async function callOperazione() {
  try {

    error.value = null

    const response = await authFetch(`${operazione.value}/`, {
      method: "PATCH", body: {
        id_conto: id_conto.value,
        importo: importoNumerico.value,
      }
    });

    jsonOperazione.value = await response.json()
    responseATM.value = response.status
    page.value++

  } catch (err) {
    page.value++
    jsonOperazione.value = err
    responseATM.value = err.status
    console.error('Fetch error:', err)
  }
  await fetchConto()
}

async function checkForm() {
  let importoMaggiore = importoNumerico.value > conti.value.find(conto => conto.id === id_conto.value).saldo
  if (importoMaggiore && operazione.value === "prelievo") {
    fetchConto()
    importoMaggiore = importoNumerico.value > conti.value.find(conto => conto.id === id_conto.value).saldo
  }

  if (!id_conto.value || !importoNumerico.value) {
    messageStore.setMessage("⚠️ Tutti i cambi sono obbligatori", 3000)
    return
  } else if (importoNumerico.value < 0 || isNaN(importoNumerico.value)) {
    messageStore.setMessage("⚠️ L'importo inserito non è valido")
  } else if (importoMaggiore && operazione.value === "prelievo") {
    messageStore.setMessage("⚠️ L'importo inserito per il prelievo è maggiore del saldo disponibile")
  } else {
    page.value++
  }
}

function ritorno(pulisci) {
  if (pulisci) {
    pulisciForm()
  } else {
    page.value--
  }
  fetchConto()
}

function pulisciForm() {
  page.value = 0
  importoFormat.value = ""
  importoNumerico.value = ""
}

onMounted(() => {
  if(authStore.selectedUserId){
    apiPathUser.value = `conti/${authStore.selectedUserId}`
  }
  fetchConti()
})
</script>

<template>
  <div class="bonifico">
    <form v-if="page === 0" @submit.prevent="checkForm" class="form-ATM">
      <span>
        <label style="margin-right: 10px;" for="conto-mittente">Segli conto:</label>
        <select name="conto-mittente" id="conto-mittente" v-model="id_conto">
          <option v-for="conto in conti" :key="conto.id" :value="conto.id">
            {{ conto.nome }}
          </option>
        </select>
      </span>

      <p class="saldo">Saldo conto selezionato: <span>{{ saldoFormattato }}</span></p>

      <div class="radio-group">
        <input type="radio" name="operazione" id="deposito" class="radio-button" value="deposito" v-model="operazione" checked>
        <label for="deposito" class="label-button">Deposito</label>

        <input type="radio" name="operazione" id="prelievo" class="radio-button" value="prelievo" v-model="operazione">
        <label for="prelievo" class="label-button">Prelievo</label>
      </div>



      <label for="importo">Inserisci l'importo da
        <span v-if="operazione === 'deposito'">depositare</span>
        <span v-if="operazione === 'prelievo'">prelevare</span>
        :</label>
      <CurrencyInput v-model="importoFormat" @update:numericValue="importoNumerico = $event" id="importo" :value="importoFormat" />

      <span>
        <input type="submit" :value="operazione === 'deposito' ? 'Deposita' : 'Preleva'">
      </span>
    </form>
    <div v-else-if=" page===1" class="form-ATM">
      <h2 class="contoText">Conto utilizzato:
        <span v-if="conti">{{conti.find(conto => conto.id === id_conto).nome}}</span>
      </h2>
      <p>Importo da
        <span v-if="operazione === 'deposito'">depositare</span>
        <span v-if="operazione === 'prelievo'">prelevare</span>:
      {{ importoFormat }}</p>
      <div>
        <button class="modifica" @click="page--">Modifica</button>
        <button @click="callOperazione">Conferma</button>
      </div>
    </div>
    <div v-else-if="page === 2" class="form-ATM">
      <div v-if="responseATM === 201" class="success">
        <img src="@/assets/spunta-verde.svg" alt="Avvenuto" width="100px" height="100px">
        <h1 style="color: green;">{{ jsonOperazione.message }}</h1>
        <p>Saldo conto aggiornato: <span>{{ saldoFormattato }}</span></p>
      </div>
      <div v-else>
        <img src="@/assets/spunta-rossa.svg" alt="Errore" width="100px" height="100px">
        <h1 style="color: darkred;">Errore</h1>
        <p>{{ jsonOperazione.message }}</p>
      </div>
      <button @click="ritorno(true)" id="ritorna">Effettua un'altra operazione</button>
    </div>


  </div>
</template>

<style scoped>


.radio-group {
  display: flex;
  gap: 10px;
}

.radio-button {
  display: none;
  /* nasconde l'input */
}

.label-button {
  padding: 10px 20px;
  border: 2px solid #006bdd;
  border-radius: 8px;
  background-color: white;
  color: #0064cf;
  cursor: pointer;
  transition: 0.3s ease;
  user-select: none;
}

/* Quando il radio è selezionato, lo stile cambia */
.radio-button:checked+.label-button {
  background-color: #006fe6;
  color: white;
  box-shadow: 0px 0px 10px 0px #002147;
}

/* Hover effetto */
.label-button:hover {
  background-color: #e0eaff;
}























.bonifico {
  display: flex;
  justify-content: center;
  align-self: center;
  text-align: center;
  width: 100%;
  margin-top: 10px;
}

.form-ATM {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 400px;
  width: 500px;
  max-width: 600px;
  padding: 50px;
  background-color: rgb(218, 216, 216);
  padding: 20px;
  border-radius: 20px;
  box-shadow: 0px 10px 50px -10px #002147be;
  transition: all 0.2s linear;
}

.form-ATM:hover {
  box-shadow: 0px 10px 50px -10px #002147;
}

.form-ATM img {
  margin: 20px 0;
}

#ritorna {
  margin: 20px 0;
}

.saldo {
  margin: 4px 0 -5px 0 !important;
}

select,
option {
  text-align: center;
  border: 1px solid #001630;
  background-color: #002147;
  padding: 5px;
  font-size: large;
  color: white;
  max-width: fit-content;
  box-shadow: 0 0 5px 1px #002147;
  font-weight: 600;
}

input {
  border: 1px solid #d4d3ce;
  background-color: #eeece7;
  padding: 10px;
  font-size: larger;
  color: rgb(0, 0, 0);
  border-radius: 10px;
  box-shadow: 0px 0px 10px 0px #002147;
  min-width: 300px;
}

input:focus {
  outline: none;
  box-shadow: 0px 0px 10px 2px #002147;
}

input[type="text"] {
  text-align: center;
  border: 1px solid #004292;
  background-color: #c9c9c9;
  padding: 10px;
  font-size: large;
  max-width: fit-content;
  box-shadow: 0 0 5px 1px #002147;
  font-weight: 600;
}

input[type="text"]:focus {
  outline: none;
  box-shadow: 0px 0px 10px 2px #002147;
}

input[type="submit"] {
  margin-top: 20px;
  background-color: #002147;
  color: white;
  box-shadow: 0 0 5px 2px #002147;
  border: 0;
  min-width: 100px;
  cursor: pointer;
  transition: all 0.2s linear;
  padding: 9px;
}

input[type="submit"]:hover {
  background-color: #002958;
  box-shadow: 0 0 6px 3px #002147;
  padding: 10px;
}

label {
  margin: 10px 0;
}

.contoText {
  margin: 20px 0;
}

.contoText span {
  color: darkred;
  font-weight: 600;
}

.form-ATM p {
  margin: 20px 0;
  font-size: large;
  font-weight: 600;
  max-width: 100%;
  text-wrap: no-wrap;
  overflow-wrap: break-word;
}

.form-ATM p span {
  margin: 20px 0;
  font-size: larger;
  font-weight: 600;
  color: #002147;
  max-width: 100%;
  text-wrap: wrap;
}

.form-ATM button {
  background-color: #047e00;
  color: white;
  box-shadow: 0 0 5px 2px #024700;
  border: 1px solid #034d00;
  padding: 10px;
  min-width: 100px;
  cursor: pointer;
  border-radius: 10px;
  transition: all 0.2s linear;
}

.form-ATM button:hover {
  background-color: #029600;
  box-shadow: 0 0 6px 3px #024700;
  padding: 11px;
}

.form-ATM .modifica {
  background-color: #ff7b00;
  color: white;
  box-shadow: 0 0 5px 2px #ff7b00;
  border: 0;
  min-width: 100px;
  cursor: pointer;
  border: 1px solid #ce6300;
  border-radius: 10px;
  transition: all 0.2s linear;
  margin-right: 20px;
}

.form-ATM .modifica:hover {
  background-color: #ff8c00;
  box-shadow: 0 0 6px 3px #ff7b00;
}
</style>
