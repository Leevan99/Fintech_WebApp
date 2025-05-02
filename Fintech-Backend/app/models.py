# Importazione delle librerie necessarie
from datetime import datetime
import random
import string
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Inizializzazione del database
db = SQLAlchemy()

# Definizione delle tabelle del database
# Tabella utenti
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CF = db.Column(db.String(16), unique=True, nullable=False)
    nome = db.Column(db.String(80), unique=False, nullable=False)
    cognome = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(80), unique=False, nullable=False)
    is_admin = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @classmethod
    def check_is_admin(cls, user_id):
        user = cls.query.get(user_id)
        return bool(user and user.is_admin)

# Tabella conti
class ContiModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_conto = db.Column(db.String(12), unique=True, nullable=False)
    nome = db.Column(db.String(80), unique=False, nullable=False)
    saldo = db.Column(db.Float, unique=False, nullable=False)
    data_creazione = db.Column(db.DateTime, nullable=False)
    iban = db.Column(db.String(80), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user_model.id"), nullable=False)

    # Funzione per generare un codice conto e un IBAN
    def generate_N_Conto_iban(self):
        account_number = random.randint(100000000000, 999999999999)
        while ContiModel.query.filter_by(numero_conto=account_number).first():
            account_number = random.randint(100000000000, 999999999999)
        country_code = "IT"  # Codice Paese
        check_digits = str(random.randint(10, 99))  # Due cifre di controllo
        cin = random.choice(string.ascii_uppercase)  # Lettera CIN casuale
        bank_code = "05428"  # Simulazione ABI (5 cifre)
        branch_code = "11101"  # Simulazione CAB (5 cifre)
        iban = f"{country_code}{check_digits}{cin}{bank_code}{branch_code}{account_number}"
        self.numero_conto = str(account_number)
        self.iban = iban

# Tabella movimenti
class MovimentiModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False, default=datetime.now)
    importo = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(80), nullable=False)
    causale = db.Column(db.String(80), nullable=True)
    id_conto_mittente = db.Column(db.Integer, db.ForeignKey("conti_model.id"), nullable=True)
    iban_mittente = db.Column(db.String(80), nullable=True)
    beneficiario = db.Column(db.String(80), nullable=True)
    id_conto_destinatario = db.Column(db.Integer, db.ForeignKey("conti_model.id"), nullable=True)
    iban_destinatario = db.Column(db.String(80), nullable=True)
    
# Tabella per la blacklist dei token JWT
class RevokedTokenModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120), unique=True, nullable=False)  # Identificativo del token
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)  # Data di creazione del token

