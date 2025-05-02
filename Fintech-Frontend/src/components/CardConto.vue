<template>
  <div class="cardConto">
    <h1>{{ nomeConto }}</h1>
    <p>N° conto: {{ numeroConto }}</p>

    <h1>{{ formattedSaldo }}</h1>
    <button class="conto-button" @click="visualizzaConto">Visualizza conto</button>
    <p class="small-font">IBAN: {{ iban }}<br>Conto creato in data: {{ formattedDate }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useCurrencyFormatter } from '@/composables/useCurrencyFormatter';
import { useRouter } from 'vue-router'

const props = defineProps({
  id: Number,
  nomeConto: String,
  numeroConto: String,
  saldo: Number,
  iban: String,
  isFavorite: Boolean,
  dataCreazione: String
})

const router = useRouter()
const { formatCurrency } = useCurrencyFormatter();

const formattedSaldo = computed(() => formatCurrency(props.saldo));

function visualizzaConto() {
  router.push(`/conto/${props.id}`)
}

const formattedDate = computed(() => {
  const date = new Date(props.dataCreazione);
  return new Intl.DateTimeFormat('it-IT', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  }).format(date);
});

</script>

<style>
.cardConto {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
  height: 300px;
  width: 300px;
  border: 0;
  border-radius: 20px;
  padding: 10px;
  text-align: center;
  background-color: #c9a3277e;
  box-shadow: 1px 1px 50px -10px #9e8122;
  transition: all 0.2s linear;
}

.cardConto:hover {
  box-shadow: 1px 1px 50px 10px #9e8122;
}

.small-font {
  font-size: small;
  margin: 0;
}

.conto-button {
  border-radius: 30px;
  color: white;
  background-color: var(--nav-background);
  padding: 13px;
  box-shadow: 1px 1px 10px 1px var(--nav-background);
  cursor: pointer;
  transition: all linear 0.2s;
  font-size: larger;
}

.conto-button:hover {
  background-color: #00244d;
  box-shadow: 1px 1px 50px 5px #002d61;
  border-radius: 40px;
  padding: 15px;
}
</style>
