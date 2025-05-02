<template>
  <div class="container-box-name" v-show="visibile">
    <div class="popup-content">
      <div class="box-name">
        <h1>Vuoi davvero eliminare questo conto?</h1>
        <div>
          <button class="conferma" @click="conferma">Si</button>
          <button class="declina" @click="chiudiPopup">No</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { watch } from 'vue'
const props = defineProps({
  visibile: Boolean
})
const emit = defineEmits(['chiudi', 'crea'])


function chiudiPopup() {
  emit('chiudi')
}

function conferma() {
  emit('elimina')
}
</script>

<style scoped>
.container-box-name {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  background-color: rgba(0, 0, 0, 0.274);
  width: 100vw;
  height: 100vh;
  z-index: 999;
}

.popup-content {
  display: flexbox;
  text-align: right;
}

.box-name {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: rgb(136, 136, 136);
  border: 3px solid rgb(53, 53, 53);
  padding: 30px;
  border-radius: 20px;
  box-shadow: 3px 3px 10px 5px rgba(0, 0, 0, 0.274);
}


.conferma {
  background-color: #126b00;
  border-color: #0b4200;
  box-shadow: 0 0 10px 1px #126b00;
  transition: all 0.2s ease;
  margin-right: 20px;
  padding: 10px 13px;
}

.conferma:hover {
  box-shadow: 0 0 30px 5px #126b00;
  background-color: #147900;
}

.declina {
  background-color: #8b0000;
  border-color: #420000;
  box-shadow: 0 0 10px 1px #b00000;
  transition: all 0.2s ease;
  margin-right: 5px;
}

.declina:hover {
  box-shadow: 0 0 30px 5px #b00000;
  background-color: #b70000;
}

button {
  padding: 10px;
  border-radius: 10px;
  color: aliceblue;
  font-size: larger;
  font-weight: 600;
  margin-top: 1rem;
  cursor: pointer;
  border: 2px outset #000f20
}
</style>
