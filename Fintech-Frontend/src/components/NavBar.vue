<script setup>
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()


</script>

<template>
  <nav>
    <span>
      <span v-if="authStore.token && !authStore.isTokenExpired">
        <span v-if="authStore.isAdmin">
          <RouterLink to="/dashboard">Dashboard</RouterLink>
          <span v-if="authStore.selectedUserId">
            <RouterLink to="/conti">Conti utente</RouterLink>
            <RouterLink to="/bonifico">Bonifico</RouterLink>
            <RouterLink to="/ATM">ATM</RouterLink>
            <button @click="authStore.clearSelectedUserId" id="deseleziona">Deseleziona Utente</button>
          </span>
        </span>
        <span v-else>
          <RouterLink to="/dashboard">Dashboard</RouterLink>
          <RouterLink to="/conti">I miei conti</RouterLink>
          <RouterLink to="/bonifico">Bonifico</RouterLink>
          <RouterLink to="/ATM">ATM</RouterLink>
        </span>
      </span>

      <span v-else>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </span>
    </span>

    <span v-if="!authStore.token && authStore.isTokenExpired">
      <RouterLink to="/login">Login</RouterLink>
      <RouterLink class="apri-conto" to="/apri-conto">Apri il conto</RouterLink>
    </span>
    <span v-else>
      <RouterLink class="logout" to="/logout">Logout</RouterLink>
    </span>
  </nav>
  <div class="select-user-name">
    <p v-if="authStore.selectedUserId && authStore.isAdmin" class="select-user">Utente selezionato: {{ authStore.selectedUserName }}</p>
  </div>


</template>

<style scoped>
.select-user-name {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 5px;
  max-width: 93%;
}

.select-user {
  margin: 10px;
  color: white;
  box-shadow: 0px 0px 10px 10px #00bd65;
  background-color: #00b862;
  width: fit-content;
}

.logout {
  background-color: rgb(207, 0, 0);
}

.logout:hover {
  background-color: rgb(231, 1, 1);
}

.apri-conto {
  background-color: #00a759;
  border: 1px var(--nav-background) solid;
}

.apri-conto.router-link-exact-active,
.apri-conto:hover {
  background-color: #00bd65;

}

#deseleziona {
  padding: 10px;
  background-color: rgb(207, 0, 0);
  border-radius: 10px;
  color: white;
  border: 1px outset rgb(134, 0, 0);
  font-weight: bolder;
  box-shadow: 0.2px 0.2px 5px 1px red;
  cursor: pointer;
  margin-left: 5px;
}

#deseleziona:hover {
  background-color: rgb(240, 2, 2);
  box-shadow: 0.2px 0.2px 10px 2px red;
}

#deseleziona:active {
  background-color: rgb(165, 0, 0);
}
</style>
