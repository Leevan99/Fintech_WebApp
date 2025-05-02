# Banking System - Class Diagram

## UserModel Class
- **Attributes**:
  - `id`: Integer (Primary Key)
  - `CF`: String(16) (Codice Fiscale, unique)
  - `nome`: String(80)
  - `cognome`: String(80)
  - `email`: String(80) (unique)
  - `password_hash`: String(80)
  - `is_admin`: Boolean (default=False)

- **Methods**:
  - `set_password(password)`: Imposta la password criptata con hash
  - `check_password(password)`: Verifica la password rispetto all'hash salvato
  - `check_is_admin(user_id)`: Verifica se l'utente è amministratore (classmethod)

## ContiModel Class
- **Attributes**:
  - `id`: Integer (Primary Key)
  - `numero_conto`: String(12) (unique)
  - `nome`: String(80)
  - `saldo`: Float
  - `data_creazione`: DateTime
  - `iban`: String(80) (unique)
  - `user_id`: Integer (Foreign Key to UserModel.id)

- **Methods**:
  - `generate_N_Conto_iban()`: Genera numero conto e IBAN validi e univoci

## MovimentiModel Class
- **Attributes**:
  - `id`: Integer (Primary Key)
  - `data`: DateTime (default ora corrente)
  - `importo`: Float
  - `tipo`: String(80)
  - `causale`: String(80) (nullable)
  - `id_conto_mittente`: Integer (Foreign Key to ContiModel.id, nullable)
  - `iban_mittente`: String(80) (nullable)
  - `beneficiario`: String(80) (nullable)
  - `id_conto_destinatario`: Integer (Foreign Key to ContiModel.id, nullable)
  - `iban_destinatario`: String(80) (nullable)


## RevokedTokenModel Class
- **Attributes**:
  - `id`: Integer (Primary Key)
  - `jti`: String(120) (unique, JWT Identifier)
  - `created_at`: DateTime (default ora corrente)


## Relationships
- **UserModel** (1) — (N) **ContiModel**
- **ContiModel** (1) — (N) **MovimentiModel** (sia come mittente che destinatario)