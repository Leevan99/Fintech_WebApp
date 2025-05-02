<script setup>
import { useMessageStore } from '@/stores/message'
import { computed } from 'vue';
import { defineProps } from 'vue';

const props = defineProps(['message']);

const messageBox = computed(() => {
  if (props.message.includes('❌')) {
    return 'message-error';
  } else if (props.message.includes('✅')) {
    return 'message-success';
  } else if (props.message.includes('⚠️')) {
    return 'message-warning';
  } else { //ℹ️
    return 'message-info';
  }
});

const messageStore = useMessageStore();
</script>

<template>
  <div v-if="message" class="message-box" :class="messageBox">
    <div class="message-text">
      {{ message }}
    </div>
    <div>
      <button class="chiudi" @click="messageStore.clearMessage()">Chiudi</button>
    </div>
  </div>

</template>

<style scoped>
.message-box {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 50%;
  height: 100px;
  padding: 10px;
  margin: 10px auto;
  border-radius: 20px;
  text-align: center;
  box-shadow: 2px 2px 10px 2px #380000;
  opacity: 0.9;
}
.chiudi {
  margin-bottom: 10px;
  background-color: #000000;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  padding: 10px;
  font-size: larger;
  opacity: 1;
}
.chiudi:hover {
  background-color: #333333;
  box-shadow: 0 0 5px 1px #380000;
  opacity: 1;
}
.message-text{
  margin-top: 10px;
  display: flex;
  align-items: center;
  font-size: larger;
  font-weight: bold;
}
.message-error{
  background-color: rgb(151, 0, 0);
  color: white;
}
.message-success {
  background-color: rgb(0, 211, 0);
}
.message-warning {
  background-color: rgb(255, 208, 0);
}
.message-info {
  background-color: rgb(0, 89, 255);
}

</style>
