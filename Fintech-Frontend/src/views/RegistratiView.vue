<script setup>
import { ref } from 'vue';
import { useMessageStore } from '@/stores/message';

const messageStore = useMessageStore();
const formData = ref({
  nome: '',
  cognome: '',
  CF: '',
  email: '',
  password: ''
});
const responseMessage = ref('');
const responseStatus = ref(0);
const page = ref(0);

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


    const BASE_URL = (import.meta.env.VITE_API_URL || 'http://localhost:5000/') + 'api/v1/'

    // Chiamata POST diretta senza token
    const response = await fetch(`${BASE_URL}register/`, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
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

    responseStatus.value = response.status;
    responseMessage.value = data.message;
  } catch (err) {
    console.error('Errore durante l\'apertura del conto:', err.message);
    responseMessage.value = err.message;
  }

  page.value = 1;
};


</script>

<template>
  <div class="open-account">
    <div v-if="page === 0" class="open-account">
      <h1>Apri un conto</h1>
      <form @submit.prevent="submitForm" class="open-account">

        <label for="nome">Nome:</label>
        <input type="text" id="nome" v-model="formData.nome" placeholder="Es. Mario" required />

        <label for="cognome">Cognome:</label>
        <input type="text" id="cognome" v-model="formData.cognome" placeholder="Es. Rossi" required />

        <label for="CF">Codice Fiscale:</label>
        <input class="codice-fiscale" type="text" id="CF" v-model="formData.CF" placeholder="COGNOM25A01Z999J" minlength="16" maxlength="16" required />

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


        <input type="submit" value="Apri conto" />
      </form>

    </div>
    <div v-else-if="page === 1" class="thank-you">
      <div v-if="responseStatus === 201" class="success open-account">
        <img src="@/assets/spunta-verde.svg" alt="Conto creato con successo" width="100px" height="100px">
        <h1 style="color: green;">Conto creato con successo!</h1>
        <p>Il conto è stato correttamente creato.</p>
        <a id="login" href="/login">Effettua il Login</a>
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


input[type="submit"], button.riprova, a#login {
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
