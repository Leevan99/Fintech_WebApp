<script setup>
import { ref, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { useMessageStore } from '@/stores/message'
import { authFetch } from '@/utils/api'


const messageStore = useMessageStore()
const email = ref()
const password = ref()
const authStore = useAuthStore()
const router = useRouter()
let messageTimeout = null
const showPassword = ref(false);

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

// Pulizia timeout quando il componente viene smontato
onUnmounted(() => {
  if (messageTimeout) clearTimeout(messageTimeout)
})

async function login() {
  try {
    // Reset messaggio
    messageStore.setMessage(null)

    // Controllo campi vuoti
    if (!email.value || !password.value) {
      messageStore.setMessage('⚠️ Inserisci email e password!', 3000)
      return
    }

    // Effettua la chiamata POST al login
    const response = await authFetch("login/", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        Accept: '*/*',
      },
      body: JSON.stringify({
        email: email.value,
        password: password.value,
      }),
    })

    // Controlla risposta
    if (!response.ok) {
      throw new Error(`Errore HTTP! Status: ${response.status}`)
    }

    // Estrai token e aggiorna lo store
    const data = await response.json()
    authStore.setToken(data.access_token, data.is_admin)
    router.push('/dashboard')
    messageStore.setMessage('✅ Login effettuato con successo!', 3000)

  } catch (err) {
    console.error('Login error:', err)
    messageStore.setMessage('❌ Errore durante il login!', 3000)
  }
}

</script>

<template>
  <div class="open-account">
    <h1>Login</h1>
    <form @submit.prevent="login" class="open-account">
      <label for="email">Email:</label>
      <input type="email" v-model="email" placeholder="email@example.it" id="email" name="email" />
      <label for="password">Password:</label>
      <div class="password-container">
        <input :type="showPassword ? 'text' : 'password'" v-model="password" placeholder="••••••••••" id="password" name="password" />
        <button type="button" class="toggle-password" @click="togglePasswordVisibility">
          <img :src="showPassword ? '/eye-off.svg' : '/eye.svg'" alt="Toggle Password" />
        </button>
      </div>
      <input type="submit" value="Login" />
    </form>
  </div>
</template>


<style scoped>
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
  padding: 10px;
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
a#login {
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

input[type="submit"]:hover{
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
</style>
