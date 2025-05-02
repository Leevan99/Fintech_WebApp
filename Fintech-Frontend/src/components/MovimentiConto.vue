<template>
  <div class="movimenti-container">
    <div class="movimento-container">
      <h3 class="tipologia"><span id="tipo">{{ tipo }}</span> del {{ formattedDate }}</h3>
      <div v-if="tipo==='Bonifico'" class="movimento">
        <p>{{ ibanMittente }}</p>
        <p>--></p>
        <p>{{ ibanDestinatario }}</p>
      </div>
      <div class="movimento">
        <p :class="tipo"><span v-if="importo > 0">+</span>{{ formattedSaldo }}</p>
      </div>
      <div v-if="tipo === 'Bonifico'" class="movimento">
        <p>Causale: {{ causale }}</p>
      </div>
    </div>
  </div>
</template>


<script setup>
import { computed } from 'vue';
import { useCurrencyFormatter } from '@/composables/useCurrencyFormatter';

const props = defineProps({
  id: Number,
  dataMovimento: String,
  importo: Number,
  causale: String,
  ibanDestinatario: String,
  ibanMittente: String,
  tipo: String,
})

const { formatCurrency } = useCurrencyFormatter();

const formattedSaldo = computed(() => formatCurrency(props.importo));

const formattedDate = computed(() => {
  if (!props.dataMovimento) return 'Data non disponibile';
  const date = new Date(props.dataMovimento);
  return new Intl.DateTimeFormat('it-IT', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
    timeZone: 'UTC'
  }).format(date);
});


</script>


<style scoped>
.movimenti-container {
  padding: 20px;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-bottom: 1px solid #ccc;
}

.movimento-container{
  box-shadow: 0px 0px 10px 0px #000000;
  border-radius: 8px;
  padding-bottom: 15px;
}

.Deposito, .Prelievo, .Bonifico{
  font-size: 1.3rem;
}

.movimento-container:nth-child(even) {
  background-color: #f9f9f9;
}

.movimento-container:nth-child(odd) {
  background-color: #fff;
}

.movimento-container:hover {
  background-color: #f1f1f1;
}

.movimento-container:hover p {
  font-weight: bold;
}

.movimenti-container h2 {
  text-align: center;
  margin-bottom: 20px;
}

.movimento {
  display: flex;
  justify-content: space-around;
  width: 100%;
}

.tipologia {
  font-weight: bold;
  color: #117a65;
  text-align: center;
  margin: 10px;
}

#tipo{
  color: #005f99;
  font-size: 23px;
}

</style>
