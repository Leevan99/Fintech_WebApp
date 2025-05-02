🏛️ Fintech Web-App

Sistema di gestione conti online per una banca sviluppato in Flask, Vue.js e SQLAlchemy.

Requisiti
- Python 3.12.6 o superiore
- npm 10.9.0 o superiore
- Accesso Internet per scaricare le dipendenze

Funzionalità Principali
- Gestione fino a 5 conti utente
- Bonifici e operazioni ATM (depositi e prelievi)
- Dashboard amministratore per gestione profili e conti utente (creazione, modifica, eliminazione)
- Autenticazione e autorizzazione utenti
- API REST per tutte le operazioni

Configurazione Backend
1. Apri un terminale nella root del progetto
2. Porta nella cartella del backend:
   cd Fintech-Backend
3. Crea e attiva l'ambiente virtuale:
   py -m venv venv

   # Linux/macOS:
   source venv/bin/activate
   # Windows:
   venv\Scripts\activate
4. Installa le dipendenze:
   pip install -r requirements.txt
5. Avvia il server:
   py run.py

Il server sarà disponibile su: http://127.0.0.1:5000/api/v1/

Configurazione Frontend
1. Apri un altro terminale nella root del progetto
2. Porta nella cartella del frontend:
   cd Fintech-Frontend
3. (Opzionale) Crea un file .env con:
   VITE_API_URL=http://192.168.0.123:5000/
4. Installa le dipendenze:
   npm install
5. Avvia il server di sviluppo:
   npm run dev

Accedi all'applicazione su: http://127.0.0.1:5173

Credenziali Admin
- Email: admin@admin.com
- Password: Admin1234

Test Funzionali Backend
1. Apri un terminale nella root del progetto
2. Porta nella cartella del backend:
   cd Fintech-Backend
3. Esegui i test:
   py test.py

Reset Database
Per ricreare da zero il database:
py reset-db.py

Build Frontend per Produzione
1. Apri un terminale nella root del progetto
2. Porta nella cartella del frontend:
   cd Fintech-Frontend
3. Esegui il build:
   npm run build

Il pacchetto compilato sarà disponibile in Fintech-Frontend/dist

Nota
Se riscontri problemi, elimina la cartella venv e ripeti l'installazione.
