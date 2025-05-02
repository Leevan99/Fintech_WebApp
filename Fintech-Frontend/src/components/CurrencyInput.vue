<template>
  <input ref="inputRef" type="text" :value="displayValue" @input="onInput" @blur="onBlur" class="currency-input" />
</template>

<script setup>
import { ref, watch } from 'vue';

// Props e eventi
const props = defineProps({
  modelValue: String
});
const emit = defineEmits(['update:modelValue', 'update:numericValue']);

// Riferimenti
const displayValue = ref('');
const inputRef = ref(null);

// Watch per sincronizzare il valore formattato
watch(() => props.modelValue, (newVal) => {
  if (newVal !== displayValue.value) {
    displayValue.value = newVal;
  }
});

// Utility: formatta i numeri con separatori delle migliaia
function formatNumber(n) {
  return n.replace(/\D/g, '').replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}

// Utility: formatta il valore in formato € con decimali
function formatCurrency(value, isBlur = false) {
  let input_val = value;
  if (!input_val) return '';

  // Rimuove simboli non numerici e tiene la virgola
  input_val = input_val.replace(/[^0-9,]/g, '');

  if (input_val.indexOf(',') >= 0) {
    const decimal_pos = input_val.indexOf(',');
    let left_side = input_val.substring(0, decimal_pos);
    let right_side = input_val.substring(decimal_pos + 1);

    left_side = formatNumber(left_side);
    right_side = formatNumber(right_side);

    if (isBlur) right_side += '00';
    right_side = right_side.substring(0, 2);

    return '€' + left_side + ',' + right_side;
  } else {
    input_val = formatNumber(input_val);
    if (isBlur) input_val += ',00';
    return '€' + input_val;
  }
}

// Utility: estrae il valore numerico (es. 1.234,56 → 1234.56)
function extractNumericValue(formatted) {
  if (!formatted) return '';
  return formatted
    .replace(/[€\s]/g, '')  // rimuove €
    .replace(/\./g, '')     // rimuove punti
    .replace(',', '.');     // converte la virgola in punto
}

// Gestione input
function onInput(e) {
  const raw_val = e.target.value;
  const formatted = formatCurrency(raw_val);
  const numeric = extractNumericValue(formatted);

  displayValue.value = formatted;
  emit('update:modelValue', formatted);
  emit('update:numericValue', numeric);
}

// Gestione blur
function onBlur(e) {
  const formatted = formatCurrency(e.target.value, true);
  const numeric = extractNumericValue(formatted);

  displayValue.value = formatted;
  emit('update:modelValue', formatted);
  emit('update:numericValue', numeric);
}
</script>

<style scoped>
.currency-input {
  padding: 0.5em;
  font-size: 1em;
  width: 200px;
}
</style>