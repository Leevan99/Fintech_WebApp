<template>
  <main class="home-container">
    <!-- Hero Section -->
    <section class="hero">
      <h1>Gestisci i tuoi conti in modo semplice e sicuro</h1>
      <p>Controlla saldi, movimenti e trasferimenti con pochi click.</p>
      <button @click="openAccount" class="apri-conto">Apri un conto</button>
    </section>

    <!-- Features Section -->
    <section class="features">
      <div class="feature" v-for="item in features" :key="item.title">
        <h3>{{ item.title }}</h3>
        <p>{{ item.description }}</p>
      </div>
    </section>
  </main>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      features: [
        {
          title: 'Saldo in tempo reale',
          description: 'Visualizza il saldo e i movimenti istantaneamente.'
        },
        {
          title: 'Trasferimenti rapidi',
          description: 'Invia denaro in modo facile e veloce.'
        },
        {
          title: 'Assistenza 24/7',
          description: 'Supporto sempre disponibile per ogni tua esigenza.'
        }
      ]
    }
  },
  methods: {
    openAccount() {
      // Logica per aprire un nuovo conto o navigare alla pagina registrazione
      this.$router.push({ name: 'apriConto' });
    }
  }
}
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  color: #333;
  font-family: Arial, sans-serif;
}

.hero {
  text-align: center;
  margin-bottom: 60px;
}

.hero h1 {
  font-size: 2.5rem;
  margin-bottom: 20px;
  color: #0056b3;
}

.hero p {
  font-size: 1.2rem;
  margin-bottom: 30px;
}

.apri-conto {
  padding: 12px 24px;
  background-color: #0056b3;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.apri-conto:hover {
    background-color: #00a759;
    box-shadow: 0 3px 8px 1px #0056b3;
    transform: translateY(-2px);
}

.features {
  display: flex;
  gap: 20px;
  justify-content: space-between;
}

.feature {
  flex: 1;
  padding: 20px;
  background-color: #f7f7f7;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.feature:hover {
  transform: translateY(-5px);
}

.feature h3 {
  margin-bottom: 10px;
  color: #0056b3;
}
</style>
