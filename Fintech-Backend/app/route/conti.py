from datetime import datetime
from flask_restful import Resource, reqparse, fields, marshal_with, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import UserModel, db, ContiModel


# Parser per i conti
conto_args = reqparse.RequestParser()
conto_args.add_argument("nome", type=str, required=True, help="Il campo Nome non può essere vuoto")

# Campi da restituire per i conti
contoFields = {
    "id": fields.Integer,
    "numero_conto": fields.String,
    "nome": fields.String,
    "saldo": fields.Float,
    "iban": fields.String,
    "data_creazione": fields.DateTime,
}

# Api per i conti dell'utente autenticato
class Conti(Resource):
    # Restituisce tutti i conti dell'utente autenticato
    @jwt_required()
    @marshal_with(contoFields)
    def get(self):
        current_user_id = get_jwt_identity()
        if UserModel.check_is_admin(current_user_id):
            return {"message" : "Non puoi avere un conto, sei un amministratore"}, 403
        conti = ContiModel.query.filter_by(user_id=current_user_id).all()
        if not conti:
            return {"message": "Nessun conto trovato"}, 204
        return conti
    
    # Crea un nuovo conto
    @jwt_required()
    @marshal_with(contoFields)
    def post(self):
        current_user_id = get_jwt_identity()
        if UserModel.check_is_admin(current_user_id):
            return {"message" : "Non puoi creare un conto, sei un amministratore"}, 404
        args = conto_args.parse_args()
        conti = ContiModel.query.filter_by(user_id=current_user_id).all()
        if len(conti) >= 5:
            return {"message":"Hai già raggiunto il numero massimo di conti"}, 403
        # Controllo che il nome del conto non sia già presente
        conto = ContiModel.query.filter_by(user_id=current_user_id, nome=args['nome']).first()
        if conto:
            return {"message":"nome conto già utilizzato"}, 409

        conto = ContiModel(nome=args["nome"], saldo=0, data_creazione=datetime.now(), user_id=current_user_id)
        conto.generate_N_Conto_iban()
        db.session.add(conto)
        db.session.commit()
        return conto, 201

# Api per la gestione dei conti da parte dell'amministratore
class ContiAdmin(Resource):
    # Restituisce tutti i conti dell'utente selezionato
    @jwt_required()
    @marshal_with(contoFields)
    def get(self, id):
        current_user_id = get_jwt_identity()
        if UserModel.check_is_admin(current_user_id):
            conti = ContiModel.query.filter_by(user_id=id).all()
            if not conti:
                return {"message": "Nessun conto trovato"}, 204
            return conti
        abort(403, message="Non sei autorizzato a fare quest'operazione")
    
    # Crea un nuovo conto all'utente selezionato
    @jwt_required()
    @marshal_with(contoFields)
    def post(self, id):
        current_user_id = get_jwt_identity()
        user = UserModel.query.filter_by(id=id, is_admin=False).first()
        if UserModel.check_is_admin(current_user_id) and user:
            args = conto_args.parse_args()
            conti = ContiModel.query.filter_by(user_id=id).all()
            if len(conti) >= 5:
                return {"message":"Hai già raggiunto il numero massimo di conti"}, 403
            # Controllo che il nome del conto non sia già presente tra i conti dell'utente selezionato
            conto = ContiModel.query.filter_by(user_id=id, nome=args['nome']).first()
            if conto:
                return {"message":"nome conto già utilizzato"}, 409

            conto = ContiModel(nome=args["nome"], saldo=0, data_creazione=datetime.now(), user_id=id)
            conto.generate_N_Conto_iban()
            db.session.add(conto)
            db.session.commit()
            return conto, 201
        abort(403, message="Non sei autorizzato a fare quest'operazione")


# Api per la gestione di un conto specifico
class Conto(Resource):
    # Restituisce un conto specifico dell'utente autenticato
    @jwt_required()
    @marshal_with(contoFields)
    def get(self, id):
        current_user_id = get_jwt_identity()
        if UserModel.check_is_admin(current_user_id):
            conto = ContiModel.query.filter_by(id=id).first()
            if not conto:
                abort(404, message="Il conto non esiste per l'utente selezionato")
        else:
            conto = ContiModel.query.filter_by(user_id=current_user_id, id=id).first()
            if not conto:
                abort(404, message="Il conto non esiste o non ti appartiene")
        return conto
    
    # Aggiorna il nome di un conto specifico dell'utente autenticato
    @jwt_required()
    @marshal_with(contoFields)
    def patch(self, id):
        current_user_id = get_jwt_identity()
        args = conto_args.parse_args()
        if args["nome"] == "Conto Principale":
            return {"message": "Non puoi rinominare un conto in Conto Principale"}, 422
        if UserModel.check_is_admin(current_user_id):
            conto = ContiModel.query.filter_by(id=id).first()
            if not conto:
                abort(404, message="Il conto non esiste")
            conti = ContiModel.query.filter_by(user_id=conto.user_id, nome=args['nome']).first()
        else:
            conto = ContiModel.query.filter_by(user_id=current_user_id, id=id).first()
            if not conto:
                abort(404, message="Il conto non esiste o non ti appartiene")
            conti = ContiModel.query.filter_by(user_id=current_user_id, nome=args['nome']).first()
        if conto.nome == "Conto Principale":
            return {"message": "Non puoi rinominare il conto principale"}, 422
        elif conti:
            return {"message": "Nome conto già utilizzato"}, 409
        conto.nome = args["nome"]
        db.session.commit()
        return conto

    # Elimina un conto specifico dell'utente selezionato se l'utente è un amministratore e il conto non ha saldo
    # e non è il conto principale
    @jwt_required()
    def delete(self, id):
        current_user_id = get_jwt_identity()
        if UserModel.check_is_admin(current_user_id):
            conto = ContiModel.query.filter_by(id=id).first()
            if not conto:
                abort(404, message="Il conto non esiste")
            elif conto.saldo != 0:
                abort(403, message="Non puoi eliminare un conto con saldo diverso da zero")
            elif conto.nome == "Conto Principale":
                abort(422, message="Non puoi eliminare il conto principale")
            db.session.delete(conto)
            db.session.commit()
            return {"message": "Conto eliminato correttamente"}