// stores/message.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useMessageStore = defineStore('message', () => {
  const message = ref(null)
  let timeoutId = null

  const setMessage = (newMessage, duration = 5000) => {
    message.value = newMessage
    if (timeoutId) clearTimeout(timeoutId)
    timeoutId = setTimeout(() => {
      message.value = null
    }, duration)
  }

  const clearMessage = () => {
    message.value = null
    if (timeoutId) clearTimeout(timeoutId)
  }

  return { message, setMessage, clearMessage }
})