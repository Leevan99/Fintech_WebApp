# Banking System - Entity Definitions

## UserModel
- `id` (PK, Integer)
- `CF` (String(16), Unique, Not Null)
- `nome` (String(80), Not Null)
- `cognome` (String(80), Not Null)
- `email` (String(80), Unique, Not Null)
- `password_hash` (String(80), Not Null)
- `is_admin` (Boolean, Default: False)

## ContiModel
- `id` (PK, Integer)
- `numero_conto` (String(12), Unique, Not Null)
- `nome` (String(80), Not Null)
- `saldo` (Float, Not Null)
- `data_creazione` (DateTime, Not Null)
- `iban` (String(80), Unique, Not Null)
- `user_id` (FK → UserModel.id, Integer, Not Null)

## MovimentiModel
- `id` (PK, Integer)
- `data` (DateTime, Default: now, Not Null)
- `importo` (Float, Not Null)
- `tipo` (String(80), Not Null)
- `causale` (String(80), Nullable)
- `id_conto_mittente` (FK → ContiModel.id, Integer, Nullable)
- `iban_mittente` (String(80), Nullable)
- `beneficiario` (String(80), Nullable)
- `id_conto_destinatario` (FK → ContiModel.id, Integer, Nullable)
- `iban_destinatario` (String(80), Nullable)

## RevokedTokenModel
- `id` (PK, Integer)
- `jti` (String(120), Unique, Not Null)
- `created_at` (DateTime, Default: now, Not Null)

## Relationships
- UserModel → ContiModel (One-to-Many)
  - Un utente può avere più conti
  - ContiModel fa riferimento a UserModel tramite la foreign key `user_id`
- ContiModel → MovimentiModel (One-to-Many, come mittente e destinatario)
  - Un conto può essere mittente o destinatario di più movimenti
  - MovimentiModel fa riferimento a ContiModel tramite le foreign key `id_conto_mittente` e `id_conto_destinatario`

