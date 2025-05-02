<script setup>
import { onMounted, ref } from 'vue';
import { useMessageStore } from '@/stores/message';
import { authFetch } from '@/utils/api'
import { useAuthStore } from '@/stores/auth';
import router from '@/router';

const authStore = useAuthStore();
const messageStore = useMessageStore();
const formData = ref({
  nome: '',
  cognome: '',
  CF: '',
  email: '',
  password: ''
});
const responseMessage = ref('');
const page = ref(0);
const responseStatus = ref(0);
const showPassword = ref(false);

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const passwordStrengthMessage = ref('Password:');
const passwordStrengthColor = ref('black'); // colore iniziale
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;
const cfRegex = /^[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]$/;


const checkPasswordStrength = () => {
  const password = formData.value.password;

  if (!password) {
    passwordStrengthMessage.value = 'Password:';
    passwordStrengthColor.value = 'black';
  } else if (passwordRegex.test(password)) {
    passwordStrengthMessage.value = 'Password sicura!';
    passwordStrengthColor.value = 'green';
  } else {
    passwordStrengthMessage.value = 'Password troppo debole!';
    passwordStrengthColor.value = 'darkred';
  }
};


async function fetchUtente() {
  try {
    const response = await authFetch(`admin/user/${authStore.selectedUserId}/`, { method: "GET" })

    const utente = await response.json()

    formData.value.nome = utente.nome
    formData.value.cognome = utente.cognome
    formData.value.CF = utente.CF
    formData.value.email = utente.email
    formData.value.password = utente.password

  } catch (err) {
    err.value = err.message
    console.error('Fetch error:', err)
  }
}

const submitForm = async () => {
  try {
    // Reset messaggio
    messageStore.setMessage(null);

    // Controllo campi vuoti
    if (!formData.value.nome || !formData.value.cognome || !formData.value.email || !formData.value.password) {
      messageStore.setMessage('⚠️ Compila tutti i campi!', 3000);
      return;
    }

    // Controllo password sicura
    if (!passwordRegex.test(formData.value.password)) {
      messageStore.setMessage('⚠️ La password deve contenere almeno 8 caratteri, una maiuscola, una minuscola, un numero e un simbolo!', 5000);
      return;
    }
    // Controllo CF valido
    if (!cfRegex.test(formData.value.CF)) {
      messageStore.setMessage('⚠️ Il codice fiscale non è valido!', 5000);
      return;
    }
    // Controllo email valida
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.value.email)) {
      messageStore.setMessage('⚠️ L\'email non è valida!', 5000);
      return;
    }

    // Chiamata POST diretta senza token
    const response = await authFetch(`admin/user/${authStore.selectedUserId}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        Accept: '*/*',
      },
      body: JSON.stringify({
        nome: formData.value.nome,
        cognome: formData.value.cognome,
        CF: formData.value.CF,
        email: formData.value.email,
        password: formData.value.password,
      }),
    });

    const data = await response.json();
    responseMessage.value = data.message || 'Operazione completata con successo';
    responseStatus.value = response.status;
  } catch (err) {
    console.error('Errore durante l\'apertura del conto:', err);
    responseMessage.value = err.message;
  }

  page.value = 1;
};


onMounted(() => {
  fetchUtente()
})
</script>

<template>
  <div class="open-account">
    <div v-if="page === 0" class="open-account">
      <h2 class="title">Modifica profilo utente</h2>
      <form @submit.prevent="submitForm" class="open-account">

        <label for="nome">Nome:</label>
        <input type="text" id="nome" v-model="formData.nome" placeholder="Es. Mario" required />

        <label for="cognome">Cognome:</label>
        <input type="text" id="cognome" v-model="formData.cognome" placeholder="Es. Rossi" required />

        <label for="CF">Codice Fiscale:</label>
        <input class="codice-fiscale" type="text" id="CF" v-model="formData.CF" placeholder="Es. COGNOM25A01Z999J" minlength="16" maxlength="16" required />

        <label for="email">Email:</label>
        <input type="email" id="email" v-model="formData.email" placeholder="email@example.it" required />

        <label for="password" :style="{ color: passwordStrengthColor, fontWeight: 'bold' }">
          {{ passwordStrengthMessage }}
        </label>
        <div class="password-container">
          <input :type="showPassword ? 'text' : 'password'" id="password" v-model="formData.password" @input="checkPasswordStrength" placeholder="••••••••••" required />
          <button type="button" class="toggle-password" @click="togglePasswordVisibility">
            <img :src="showPassword ? '/eye-off.svg' : '/eye.svg'" alt="Toggle Password" />
          </button>
        </div>

        <input type="submit" value="Aggiorna dati" />
      </form>

    </div>
    <div v-else-if="page === 1" class="thank-you">
      <div v-if="responseStatus === 200" class="success open-account">
        <img src="@/assets/spunta-verde.svg" alt="Conto creato con successo" width="100px" height="100px">
        <h1 style="color: green;">Profilo aggiornato</h1>
        <p>{{responseMessage}}</p>
        <button id="ritorna" @click="router.push({ name: 'dashboard' })">Torna alla Dashboard</button>
      </div>
      <div v-else class="open-account">
        <img src="@/assets/spunta-rossa.svg" alt="Errore" width="100px" height="100px">
        <h1 style="color: darkred;">Errore</h1>
        <p>{{ responseMessage }}</p>
        <button class="riprova" @click="page--">Riprova</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.password-container {
  position: relative;
  display: flex;
  align-items: center;
}

.toggle-password {
  position: absolute;
  right: 7px;
  background: transparent;
  border: 0;
  cursor: pointer;
  width: 24px;
  height: 24px;
  padding: 0;
}

.toggle-password img {
  width: 24px;
  height: 24px;
  margin: 0 !important;
}

.title {
  margin-top: 5%;
}
.open-account {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.thank-you {
  margin-top: 5%;
}

.open-account img {
  margin: 20px 0;
}


input {
  border: 1px solid #d4d3ce;
  background-color: #eeece7;
  padding: 8px;
  font-size: larger;
  color: rgb(0, 0, 0);
  border-radius: 10px;
  box-shadow: 0px 0px 10px 0px #002147;
  min-width: 300px;
  text-align: center;
}

input:focus {
  outline: none;
  box-shadow: 0px 0px 10px 2px #002147;
}


input[type="submit"],
button.riprova,
button#ritorna {
  text-decoration: none;
  background-color: #047e00;
  color: white;
  box-shadow: 0 0 5px 2px #024700;
  border: 1px solid #034d00;
  padding: 10px;
  min-width: 100px;
  cursor: pointer;
  border-radius: 10px;
  transition: all 0.2s linear;
  margin-top: 20px;
}

input[type="submit"]:hover,
button.riprova:hover {
  background-color: #029600;
  box-shadow: 0 0 6px 3px #024700;
  padding: 11px;
}

label {
  margin: 10px 0;
}

.open-account p {
  margin: 5px 0;
  font-size: large;
  font-weight: 600;
  max-width: 100%;
}

.codice-fiscale {
  text-transform: uppercase;
}
</style>
