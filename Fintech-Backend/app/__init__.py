from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from app.config import Config
from app.models import UserModel, db, RevokedTokenModel
from app.route.movimenti import Bonifico, Movimenti, MovimentiAdmin, MovimentiConto, Prelievo, Deposito
from app.route.users import IdUtente , User, Login, Register, AdminUser, Logout
from app.route.conti import Conti, ContiAdmin, Conto
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # Configurazione dell'applicazione
    app.config.from_object(Config)

    # CORS per le richieste cross-origin
    CORS(app, origins=app.config["CORS_ALLOW_ORIGINS"], allow_headers=app.config["CORS_ALLOW_HEADERS"], supports_credentials=app.config["CORS_ALLOW_CREDENTIALS"])

    # Inizializza estensioni
    db.init_app(app)
    jwt = JWTManager(app)

    # Controllo se il token è stato revocato
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return db.session.query(RevokedTokenModel.id).filter_by(jti=jti).scalar() is not None

    # Inizializza API
    api = Api(app, prefix="/api/v1")
    # API users
    api.add_resource(IdUtente, "/IDbyCF/")
    api.add_resource(AdminUser, "/admin/user/<int:id>/")
    api.add_resource(User, "/user/")
    api.add_resource(Login, "/login/")
    api.add_resource(Register, "/register/")
    api.add_resource(Logout, "/logout/")

    # API conti
    api.add_resource(Conti, "/conti/")
    api.add_resource(Conto, "/conto/<int:id>/")
    api.add_resource(ContiAdmin, "/conti/<int:id>/")

    # API movimenti
    api.add_resource(Bonifico, "/bonifico/")
    api.add_resource(MovimentiConto, "/conto/movimenti/<int:id>/")
    api.add_resource(Movimenti, "/movimenti/")
    api.add_resource(MovimentiAdmin, "/admin/movimenti/<int:id>/")
    api.add_resource(Prelievo, "/prelievo/")
    api.add_resource(Deposito, "/deposito/")
    

    # Creazione di un amministratore di default se non esiste
    def create_default_admin():
        # Controlla se esiste già un admin
        admin = UserModel.query.filter_by(email="admin@admin.com").first()
        if not admin:
            admin = UserModel(
                CF="ADMINCF000000000",
                nome="First",
                cognome="Admin",
                email="admin@admin.com",
                is_admin=True
            )
            admin.set_password("Admin1234")
            db.session.add(admin)
            db.session.commit()

    # Crea il database se non esiste
    with app.app_context():
        db.create_all()
        create_default_admin()

    return app