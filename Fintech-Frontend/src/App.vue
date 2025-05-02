<script setup>
import { RouterView } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import MessageBox from '@/components/MessageBox.vue'
import { useMessageStore } from '@/stores/message'

const messageStore = useMessageStore()


import { onMounted } from 'vue'
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()

onMounted(() => {
  // Leggi il token dai cookie all'avvio
  const cookieToken = authStore.getCookie('access_token')

  if (cookieToken) authStore.setToken(cookieToken)
})

</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="100" height="100" />

    <div class="wrapper">
      <h1>FinTech</h1>
      <NavBar/>
    </div>
  </header>
  <MessageBox class="message" :message="messageStore.message" />
  <RouterView class="container-principale" />
</template>

<style scoped>

header {
  display: flex;
  width: 100%;
}

header .wrapper {
  width: 100%;
}

.logo {
  display: block;
  margin: 0 2rem 0 0;
}

.message {
  position: fixed;
  top: 15%;
  left: 0;
  right: 0;
  z-index: 1000;
}
.container-principale {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}


</style>
