# 🏛️ Fintech Web-App

Sistema di gestione conti online per una banca sviluppato in Flask, Vue.js e SQLAlchemy.

![Python](https://img.shields.io/badge/python-3.12.6+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.1.0-green.svg)
![npm](https://img.shields.io/badge/npm-10.9.0-green.svg)

## 📋 Requisiti

- Python 3.12.6 o superiore
- npm 10.9.0 o superiore
- Accesso Internet per scaricare le dipendenze

## ✨ Funzionalità Principali

- 💼 Gestione fino a 5 conti utente
- 💶 Bonifici e operazioni ATM (depositi e prelievi)
- 👥 Dashboard amministratore per gestione profili e conti utente (creazione, modifica, eliminazione)
- 🔐 Autenticazione e autorizzazione utenti
- 🔄 API REST per tutte le operazioni

## ⚙️ Configurazione Backend

1. Apri un terminale nella root del progetto
2. Porta nella cartella del backend:
   ```bash
   cd Fintech-Backend
   ```
3. Crea e attiva l'ambiente virtuale:
   ```bash
   py -m venv venv

   # Linux/macOS:
   source venv/bin/activate
   # Windows:
   venv\Scripts\activate
   ```
4. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```
5. Avvia il server:
   ```bash
   py run.py
   ```

Il server sarà disponibile su: <http://127.0.0.1:5000/api/v1/>

## ⚙️ Configurazione Frontend

1. Apri un altro terminale nella root del progetto
2. Porta nella cartella del frontend:
   ```bash
   cd Fintech-Frontend
   ```
3. **(Opzionale)** Crea un file `.env` nella cartella `Fintech-Frontend` con la variabile di ambiente:
   ```env
   VITE_API_URL=http://192.168.0.123:5000/
   ```
   oppure l'indirizzo dell'eventuale server backend.
4. Installa le dipendenze:
   ```bash
   npm install
   ```
5. Avvia il server di sviluppo:
   ```bash
   npm run dev
   ```

Accedi all'applicazione su: <http://127.0.0.1:5173>

### Credenziali Admin

- Email: `admin@admin.com`
- Password: `Admin1234`

## 🧪 Test Funzionali Backend

1. Apri un terminale nella root del progetto
2. Porta nella cartella del backend:
   ```bash
   cd Fintech-Backend
   ```
3. Esegui i test:
   ```bash
   py test.py
   ```

I test coprono:
- Registrazione e login utenti
- Gestione conti (CRUD, limiti, modifica, eliminazione)
- Depositi e prelievi con controllo saldo
- Bonifici tra utenti e tracciamento movimenti
- Endpoint amministratore

## 🔄 Reset Database

Per ricreare da zero il database:

```bash
py reset-db.py
```

Questo script:
- Rimuove il database esistente (se presente)
- Crea un nuovo database con schema aggiornato

## 🛠️ Build Frontend per Produzione

1. Apri un terminale nella root del progetto
2. Porta nella cartella del frontend:
   ```bash
   cd Fintech-Frontend
   ```
3. Esegui il build:
   ```bash
   npm run build
   ```

Il pacchetto compilato sarà disponibile in `Fintech-Frontend/dist`.

## 📝 Nota

Se riscontri problemi, elimina la cartella `venv` (se presente) e ripeti l'installazione.