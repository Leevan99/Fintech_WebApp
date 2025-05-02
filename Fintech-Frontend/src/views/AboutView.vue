<template>
  <main class="about-container">
    <!-- About Hero -->
    <section class="hero-about">
      <h1>Chi Siamo</h1>
      <p>FinTech è la tua banca digitale di fiducia. La nostra missione è offrire soluzioni bancarie semplici, sicure e trasparenti.</p>
    </section>

    <!-- Mission & Vision -->
    <section class="mission-vision">
      <div class="item" v-for="section in sections" :key="section.title">
        <h2>{{ section.title }}</h2>
        <p>{{ section.content }}</p>
      </div>
    </section>

    <!-- Servizi Offerti -->
    <section class="services">
      <h2>I Nostri Servizi</h2>
      <div class="service" v-for="service in services" :key="service.title">
        <h3>{{ service.title }}</h3>
        <p>{{ service.description }}</p>
      </div>
    </section>
  </main>
</template>

<script>
export default {
  name: 'AboutPage',
  data() {
    return {
      sections: [
        {
          title: 'La Nostra Missione',
          content: 'Offrire prodotti e servizi bancari digitali innovativi, focalizzati sulla semplicità d’uso e sulla sicurezza.'
        },
        {
          title: 'La Nostra Visione',
          content: 'Diventare la banca di riferimento per i clienti digitali, promuovendo trasparenza e inclusione finanziaria.'
        }
      ],
      services: [
        {
          title: 'Gestione Conti Multipli',
          description: 'Gestisci fino a 5 conti: 1 conto principale obbligatorio e fino a 4 conti opzionali con nome personalizzato.'
        },
        {
          title: 'Visualizzazione Conti Dettagliata',
          description: 'Consulta il saldo e i movimenti di ogni singolo conto, ognuno dotato di numero di conto e IBAN univoco.'
        },
        {
          title: 'Transazioni Complete',
          description: 'Esegui bonifici, prelievi e depositi in modo rapido e sicuro direttamente dalla tua dashboard.'
        },
        {
          title: 'Dashboard Interattiva',
          description: 'Visualizza il saldo totale dei conti attivi e una vista aggregata di tutti i movimenti finanziari.'
        }
      ]
    }
  }
}
</script>

<style scoped>
.about-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
  font-family: Arial, sans-serif;
  color: #333;
}

.hero-about {
  text-align: center;
  margin-bottom: 60px;
}

.hero-about h1 {
  font-size: 2.5rem;
  color: #0056b3;
  margin-bottom: 20px;
}

.hero-about p {
  font-size: 1.2rem;
}

.mission-vision {
  display: flex;
  gap: 20px;
  margin-bottom: 60px;
}

.mission-vision .item {
  flex: 1;
  background: #f7f7f7;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.mission-vision h2 {
  margin-bottom: 10px;
  color: #0056b3;
}

.services {
  margin-bottom: 60px;
}

.services h2 {
  font-size: 2rem;
  color: #0056b3;
  text-align: center;
  margin-bottom: 20px;
}

.service {
  background: #f7f7f7;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.service h3 {
  margin-bottom: 10px;
  color: #0056b3;
}

.service p {
  line-height: 1.5;
}
</style>
