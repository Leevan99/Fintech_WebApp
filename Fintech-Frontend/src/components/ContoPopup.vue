<template>
  <div class="container-box-name" v-show="visibile">
    <div class="popup-content">
      <div class="chiudi">
        <button @click="chiudiPopup">&nbsp;x&nbsp;</button>
      </div>
      <div class="box-name">
        <h1>Dai un nome al nuovo conto</h1>
        <input type="text" maxlength="16" v-model="nome" @keyup.enter="conferma" placeholder="Nome conto" />
        <button class="apri-conto-btn" @click="conferma">Apri conto</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
const props = defineProps({
  visibile: Boolean
})
const emit = defineEmits(['chiudi', 'crea'])

const nome = ref("")

function chiudiPopup() {
  emit('chiudi')
  nome.value = ""
}

function conferma() {
  emit('crea', nome.value)
  nome.value = ""
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

.box-name .apri-conto-btn:hover {
  margin: 13px 0 -3px 0;
}

.box-name input {
  border-radius: 10px;
  background-color: rgb(199, 199, 199);
  font-size: 20px;
  text-align: center;
  padding: 5px;
  font-weight: 600;
}

.apri-conto-btn {
  color: aliceblue;
  background-color: #126b00;
  border: #0b4200 solid 1px;
  box-shadow: 0 0 10px 1px #126b00;
  transition: all 0.2s ease;
}

.apri-conto-btn:hover {
  box-shadow: 0 0 30px 5px #126b00;
  padding: 13px;
}

button {
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

button:hover {
  box-shadow: 0 0 20px 2px;
  opacity: 0.9;
}
</style>
