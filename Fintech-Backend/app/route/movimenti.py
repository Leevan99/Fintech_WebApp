from datetime import datetime
from sqlalchemy import or_
from flask_restful import Resource, reqparse, fields, marshal_with, abort, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import UserModel, db, ContiModel, MovimentiModel

# Parser per i bonifici
bonifico_args = reqparse.RequestParser()
bonifico_args.add_argument("beneficiario", type=str, required=True, help="Il campo Beneficiario non può essere vuoto")
bonifico_args.add_argument("id_conto_mittente", type=int, required=True, help="Il campo ID Conto Mittente non può essere vuoto")
bonifico_args.add_argument("importo", type=float, required=True, help="Il campo Importo non può essere vuoto")
bonifico_args.add_argument("causale", type=str, required=True, help="Il campo Causale non può essere vuoto")
bonifico_args.add_argument("iban_destinatario", type=str, required=True, help="Il campo IBAN Destinatario non può essere vuoto")

# Parser per i movimenti
movimento_args = reqparse.RequestParser()
movimento_args.add_argument("id_conto", type=int, required=True, help="Il campo ID Conto non può essere vuoto")
movimento_args.add_argument('importo', type=float, required=True, help="Il campo Importo non può essere vuoto")

# Campi restituiti per i movimenti 
movimentiFields = {
        "id": fields.Integer,
        "iban_mittente": fields.String,
        "iban_destinatario": fields.String,
        "data": fields.DateTime,
        "importo": fields.Float,
        "tipo": fields.String,
        "causale": fields.String,
}

# Api per i bonifici
class Bonifico(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        args = bonifico_args.parse_args()
        user = UserModel.query.filter_by(id=current_user_id, is_admin=True).first()
        if user:
            conto_mittente = ContiModel.query.filter_by(id=args["id_conto_mittente"]).first()
        else:
            conto_mittente = ContiModel.query.filter_by(user_id=current_user_id, id=args["id_conto_mittente"]).first()
        conto_destinatario = ContiModel.query.filter_by(iban=args["iban_destinatario"]).first()
        if not conto_mittente:
            abort(404, message="Il conto mittente non esiste o non ti appartiene")
        user = UserModel.query.filter_by(id=conto_destinatario.user_id).first()
        if conto_destinatario and (user.nome + " " + user.cognome) != args["beneficiario"]:
            abort(403, message="Il beneficiario non corrisponde all'IBAN del destinatario")
        elif conto_destinatario.iban == conto_mittente.iban:
            abort(403, message="Impossibile effettuare un bonifico verso lo stesso conto")
        elif conto_mittente.saldo < args["importo"]:
            abort(403, message="Saldo insufficiente")
        elif args["importo"] <= 0:
            abort(403, message="Importo non valido")
        else:
            conto_mittente.saldo -= args["importo"]
            conto_destinatario.saldo += args["importo"]
            db.session.commit()
            movimento = MovimentiModel(importo=args["importo"], data=datetime.now(), causale=args["causale"], tipo="Bonifico", id_conto_mittente=conto_mittente.id, id_conto_destinatario=conto_destinatario.id, iban_mittente=conto_mittente.iban, iban_destinatario=conto_destinatario.iban)
            db.session.add(movimento)
            db.session.commit()
        return {"message":"Bonifico effettuato con successo"}, 201

# Api per i movimenti dell'utente selezionato se l'utente è un amministratore
class MovimentiAdmin(Resource):
    @jwt_required()
    @marshal_with(movimentiFields)
    def get(self, id):
        current_user_id = get_jwt_identity()

        # Ottieni tutti gli ID dei conti dell'utente
        id_utenti = {c.id for c in ContiModel.query.filter_by(user_id=id).all()}

        # Query dei movimenti che coinvolgono uno dei conti dell’utente
        movimenti = MovimentiModel.query.join(
            ContiModel, or_(
                MovimentiModel.id_conto_mittente == ContiModel.id,
                MovimentiModel.id_conto_destinatario == ContiModel.id
            )
        ).filter(ContiModel.user_id == id).all()

        if not movimenti:
            return {"message": "Nessun movimento trovato"}, 204

        result = []

        for movimento in movimenti:
            mittente = movimento.id_conto_mittente
            destinatario = movimento.id_conto_destinatario
            importo = movimento.importo

            if mittente in id_utenti and destinatario in id_utenti:
                # Entrambi i conti sono dell’utente → duplichiamo
                movimento_uscita = MovimentiModel(
                    id=movimento.id,
                    iban_mittente=movimento.iban_mittente,
                    iban_destinatario=movimento.iban_destinatario,
                    importo=-abs(importo),
                    tipo=movimento.tipo,
                    causale=movimento.causale,
                    data=movimento.data
                )
                movimento_entrata = MovimentiModel(
                    id=movimento.id,
                    iban_mittente=movimento.iban_mittente,
                    iban_destinatario=movimento.iban_destinatario,
                    importo=abs(importo),
                    tipo=movimento.tipo,
                    causale=movimento.causale,
                    data=movimento.data
                )
                result.append(movimento_uscita)
                result.append(movimento_entrata)
            elif mittente in id_utenti:
                movimento.importo = -abs(importo)
                result.append(movimento)
            elif destinatario in id_utenti:
                movimento.importo = abs(importo)
                result.append(movimento)
        return result

# Api per i movimenti dell'utente autenticato
class Movimenti(Resource):
    @jwt_required()
    @marshal_with(movimentiFields)
    def get(self):
        current_user_id = get_jwt_identity()

        # Recupera tutti gli ID dei conti dell'utente
        id_utenti = {c.id for c in ContiModel.query.filter_by(user_id=current_user_id).all()}

        # Query dei movimenti che coinvolgono i conti dell’utente
        movimenti = MovimentiModel.query.join(
            ContiModel, or_(
                MovimentiModel.id_conto_mittente == ContiModel.id,
                MovimentiModel.id_conto_destinatario == ContiModel.id
            )
        ).filter(ContiModel.user_id == current_user_id).all()

        if not movimenti:
            return {"message": "Nessun movimento trovato"}, 204

        result = []

        for movimento in movimenti:
            mittente = movimento.id_conto_mittente
            destinatario = movimento.id_conto_destinatario
            importo = movimento.importo

            if mittente in id_utenti and destinatario in id_utenti:
                # Entrambi i conti sono dell’utente → duplichiamo
                movimento_uscita = MovimentiModel(
                    id=movimento.id,
                    iban_mittente=movimento.iban_mittente,
                    iban_destinatario=movimento.iban_destinatario,
                    importo=-abs(importo),
                    tipo=movimento.tipo,
                    causale=movimento.causale,
                    data=movimento.data
                )
                movimento_entrata = MovimentiModel(
                    id=movimento.id,
                    iban_mittente=movimento.iban_mittente,
                    iban_destinatario=movimento.iban_destinatario,
                    importo=abs(importo),
                    tipo=movimento.tipo,
                    causale=movimento.causale,
                    data=movimento.data
                )
                result.append(movimento_uscita)
                result.append(movimento_entrata)
            elif mittente in id_utenti:
                movimento.importo = -abs(importo)
                result.append(movimento)
            elif destinatario in id_utenti:
                movimento.importo = abs(importo)
                result.append(movimento)
        return result

# Api per i movimenti di un conto specifico dell'utente autenticato o seleziionato(se l'utente è un amministratore)
class MovimentiConto(Resource):
    @jwt_required()
    @marshal_with(movimentiFields)
    def get(self, id):
        current_user_id = get_jwt_identity()
        user = UserModel.query.filter_by(id=current_user_id, is_admin=True).first()
        if user:
            conto = ContiModel.query.filter_by(id=id).first()
            if not conto:
                abort(404, message="Il conto non esiste")
        else:
            conto = ContiModel.query.filter_by(user_id=current_user_id, id=id).first()
        if not conto:
            abort(404, message="Il conto non esiste o non ti appartiene")
        movimenti = MovimentiModel.query.filter((MovimentiModel.id_conto_mittente == id) | (MovimentiModel.id_conto_destinatario == id)).all()
        if not movimenti:
            return {"message": "Nessun movimento trovato"}, 204
        # Itera sui movimenti e modifica l'importo
        for movimento in movimenti:
            if movimento.id_conto_destinatario == id:
                movimento.importo = movimento.importo  # Lascia invariato
            else:
                movimento.importo = -movimento.importo  # Rende negativo
        return movimenti

# Api per i prelievi su un conto specifico dell'utente autenticato o selezionato(se l'utente è un amministratore)
class Prelievo(Resource):
    @jwt_required()
    def patch(self):
        current_user_id = get_jwt_identity()
        args = movimento_args.parse_args()
        user = UserModel.query.filter_by(id=current_user_id, is_admin=True).first()
        if user:
            conto_mittente = ContiModel.query.filter_by(id=args["id_conto"]).first()
        else:
            conto_mittente = ContiModel.query.filter_by(user_id=current_user_id, id=args["id_conto"]).first()
        if not conto_mittente:
            abort(404, message="Il conto selezionato per il prelievo non esiste o non ti appartiene")
        elif conto_mittente.saldo < args["importo"]:
            abort(403, message="Saldo insufficiente")
        else:
            if args["importo"] < 0:
                abort(403, message="Importo non valido")
            conto_mittente.saldo -= args["importo"]
            db.session.commit()
            movimento = MovimentiModel(importo=args["importo"], tipo="Prelievo", id_conto_mittente=conto_mittente.id, iban_mittente=conto_mittente.iban)
            db.session.add(movimento)
            db.session.commit()
        return {"message":"Prelievo effettuato con successo"}, 201

# Api per i depositi su un conto specifico dell'utente autenticato o selezionato(se l'utente è un amministratore)
class Deposito(Resource):
    @jwt_required()
    def patch(self):
        current_user_id = get_jwt_identity()
        args = movimento_args.parse_args()
        user = UserModel.query.filter_by(id=current_user_id, is_admin=True).first()
        if user:
            conto_destinatario = ContiModel.query.filter_by(id=args["id_conto"]).first()
        else:
            conto_destinatario = ContiModel.query.filter_by(user_id=current_user_id, id=args["id_conto"]).first()
        if not conto_destinatario:
            abort(404, message="Il conto selezionato per il deposito non esiste o non ti appartiene")
        else:
            conto_destinatario.saldo += args["importo"]
            db.session.commit()
            movimento = MovimentiModel(importo=args["importo"], tipo="Deposito", id_conto_mittente="", id_conto_destinatario=conto_destinatario.id)
            db.session.add(movimento)
            db.session.commit()
        return {"message":"Deposito effettuato con successo"}, 201