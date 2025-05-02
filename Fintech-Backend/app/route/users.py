from datetime import datetime
import random
import re
from flask_restful import Resource, reqparse, fields, marshal_with, abort
from flask_jwt_extended import get_jwt, jwt_required, create_access_token, get_jwt_identity
from app.models import ContiModel, RevokedTokenModel, UserModel, db

# Parser per la registrazione di un utente
register_args = reqparse.RequestParser()
register_args.add_argument("nome", type=str, required=True, help="Il campo Nome non può essere vuoto")
register_args.add_argument("cognome", type=str, required=True, help="Il campo Cognome non può essere vuoto")
register_args.add_argument("CF", type=str, required=True, help="Il campo CF non può essere vuoto")
register_args.add_argument("email", type=str, required=True, help="Il campo Email non può essere vuoto")
register_args.add_argument("password", type=str, required=True, help="Il campo Password non può essere vuoto")

# Parser per la modifica dei dati di un utente
update_args = reqparse.RequestParser()
update_args.add_argument("nome", type=str, required=True, help="Il campo Nome non può essere vuoto")
update_args.add_argument("cognome", type=str, required=True, help="Il campo Cognome non può essere vuoto")
update_args.add_argument("email", type=str, required=True, help="Il campo Email non può essere vuoto")

# Parser per il login di un utente
login_args = reqparse.RequestParser()
login_args.add_argument("email", type=str, required=True, help="Il campo Email non può essere vuoto")
login_args.add_argument("password", type=str, required=True, help="Il campo Password non può essere vuoto")

#Parser IDbyCF
IdUtente_args = reqparse.RequestParser()
IdUtente_args.add_argument("CF", type=str, required=True, help="Il campo CF non può essere vuoto")

# Campi da restituire per l'utente
userFields = {
    "CF": fields.String,
    "nome": fields.String,
    "cognome": fields.String,
    "email": fields.String,
    "saldo": fields.Float,
}

# Campi da restituire per l'admin
userFieldsAdmin = {
    "id": fields.Integer,
    "CF": fields.String,
    "nome": fields.String,
    "cognome": fields.String,
    "email": fields.String,
    "is_admin": fields.Boolean,
    "password": fields.String,
    "saldo": fields.Float,
}

password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$')

# Verifica se il codice fiscale è valido
def verifica_codice_fiscale(cf):
    if len(cf) != 16:
        return False

    cf = cf.upper()
    if not cf.isalnum():
        return False

    # Tabelle per il calcolo del carattere di controllo
    pari = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
        '6': 6, '7': 7, '8': 8, '9': 9,
        'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5,
        'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11,
        'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16,
        'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21,
        'W': 22, 'X': 23, 'Y': 24, 'Z': 25
    }

    dispari = {
        '0': 1, '1': 0, '2': 5, '3': 7, '4': 9, '5': 13,
        '6': 15, '7': 17, '8': 19, '9': 21,
        'A': 1, 'B': 0, 'C': 5, 'D': 7, 'E': 9, 'F': 13,
        'G': 15, 'H': 17, 'I': 19, 'J': 21, 'K': 2, 'L': 4,
        'M': 18, 'N': 20, 'O': 11, 'P': 3, 'Q': 6,
        'R': 8, 'S': 12, 'T': 14, 'U': 16, 'V': 10,
        'W': 22, 'X': 25, 'Y': 24, 'Z': 23
    }

    check_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Somma dei valori secondo pari/dispari
    total = 0
    for i in range(15):
        c = cf[i]
        if i % 2 == 0:
            total += dispari[c]
        else:
            total += pari[c]

    expected_check_char = check_chars[total % 26]

    return cf[-1] == expected_check_char

# Api di registrazione di un utente
class Register(Resource):
    # Creazione di un nuovo utente se non esiste già
    @marshal_with(userFields)
    def post(self):
        args = register_args.parse_args()
        # Controllo che l'email non sia già presente nel database
        user = UserModel.query.filter_by(email=args["email"]).first()
        if user:
            abort(409, message="Email già in uso")
        else:
            if not verifica_codice_fiscale(args["CF"].upper()):
                abort(400, message="Codice fiscale non valido")
            # Controllo che il codice fiscale non sia già presente nel database
            user = UserModel.query.filter_by(CF=args["CF"].upper()).first()
            if user:
                abort(409, message="Codice fiscale già in uso")
            if not password_regex.match(args["password"]):
                abort(400, message="La password deve contenere almeno 8 caratteri, una maiuscola, una minuscola, un numero e un carattere speciale")
            # Inserimento dell'utente nel database
            user = UserModel(nome=args["nome"], cognome=args["cognome"], CF=args["CF"], email=args["email"])
            user.set_password(args["password"])
            db.session.add(user)
            db.session.commit()
            conto = ContiModel(nome="Conto Principale", saldo=0, data_creazione=datetime.now(), user_id=user.id)
            # Creazione del conto principale per l'utente
            conto.generate_N_Conto_iban()
            db.session.add(conto)
            db.session.commit()
        return user, 201

# Api di login
class Login(Resource):
    def post(self):
        args = login_args.parse_args()
        user = UserModel.query.filter_by(email=args["email"]).first()
        if user and user.check_password(args["password"]):
            access_token = create_access_token(identity=str(user.id))
            return {"access_token": access_token, "is_admin":user.is_admin}, 200
        return {"message": "Credenziali errate"}, 401

# Api di logout
class Logout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        token = RevokedTokenModel(jti=jti)
        db.session.add(token)
        db.session.commit()
        return {"message": "Logout effettuato correttamente"}, 200

# Api per la gestione degli utenti da parte dell'amministratore
class AdminUser(Resource):
    @jwt_required()
    @marshal_with(userFieldsAdmin)
    # Restituisce un utente specifico
    def get(self, id):
        current_user_id = get_jwt_identity()  # Recupera l'ID dal token
        user = UserModel.query.filter_by(id=current_user_id).first()
        if user.is_admin == False:  # Se l'utente non è un amministratore
            abort(403, message="Utente non autorizzato")
        else:  # Se l'utente è un amministratore
            user = UserModel.query.filter_by(id=id).first()
            if not user:
                abort(404, message="Utente non trovato")
            conti = ContiModel.query.filter_by(user_id=id).all()
            saldo = 0.0
            for conto in conti:
                saldo = saldo + conto.saldo
            user.saldo = saldo
        return user

    # Modifica i dati di un utente specifico
    @jwt_required()
    def patch(self, id):
        current_user_id = get_jwt_identity()
        user = UserModel.query.filter_by(id=current_user_id).first()
        args = register_args.parse_args()
        if user.is_admin == False:  # Se l'utente non è un amministratore
            abort(403, message="Utente non autorizzato")
        else:  # Se l'utente è un amministratore
            user = UserModel.query.filter_by(id=id).first()
            if not user:
                abort(404, message="Utente non trovato")
            elif user.email != args["email"] and UserModel.query.filter_by(email=args["email"]).first():
                abort(409, message="Email già in uso")
            elif user.CF != args["CF"].upper() and UserModel.query.filter_by(CF=args["CF"].upper()).first():
                abort(409, message="Codice fiscale già in uso")
            elif not verifica_codice_fiscale(args["CF"].upper()):
                abort(400, message="Codice fiscale non valido")
            elif not password_regex.match(args["password"]):
                abort(400, message="La password deve contenere almeno 8 caratteri, una maiuscola, una minuscola, un numero e un carattere speciale")
            user.nome = args["nome"]
            user.cognome = args["cognome"]
            user.CF = args["CF"].upper()
            user.email = args["email"]
            user.set_password(args["password"])
            db.session.commit()
        return {"message": "Dati profilo modificati correttamente"}, 200

# Restituisce l'ID di un utente specifico in base al codice fiscale se l'utente è un amministratore
class IdUtente(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        admin = UserModel.query.filter_by(id=current_user_id, is_admin=True).first()
        if admin:
            args = IdUtente_args.parse_args()
            user = UserModel.query.filter_by(CF=args["CF"].upper()).first()
            if not user:
                abort(404, message="Utente non trovato")
            nomecompleto = user.nome + " " + user.cognome
            return {"ID":user.id, "NomeCompleto":nomecompleto}, 200
        else:
            abort(403, message="Utente non autorizzato")

# Api per la gestione del profilo dell'utente
class User(Resource):
    @jwt_required()
    @marshal_with(userFields)
    def get(self):
        current_user_id = get_jwt_identity()
        user = UserModel.query.filter_by(id=current_user_id).first()
        if not user:
            abort(404, message="Utente non trovato")
        conti = ContiModel.query.filter_by(user_id=current_user_id).all()
        saldo = 0.0
        for conto in conti:
            saldo = saldo + conto.saldo
        user.saldo = saldo
        return user