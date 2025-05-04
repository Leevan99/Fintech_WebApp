"""
tests/test_api_monkeypatched_config.py
Test unitari per le API principali usando un DB SQLite in memoria,
monkeypatchando Config prima di importare create_app().
"""
import unittest
import os
import tempfile
from datetime import date, timedelta
from unittest.mock import patch

# --- Monkey‐patch globale del Config di SQLAlchemy ---------------------------------
from app.config import Config
# DB in-memory per test
Config.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
Config.TESTING = True
Config.JWT_ACCESS_TOKEN_EXPIRES = 1

# Ora importiamo l’app factory con la Config modificata
from app import create_app, db
from app.models import UserModel, ContiModel, MovimentiModel

class TestAPI_MonkeyConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Bypass validazione CF
        cls.cf_patcher = patch('app.route.users.verifica_codice_fiscale', return_value=True)
        cls.cf_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.cf_patcher.stop()

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            # ricrea l'admin di default
            from app.models import UserModel
            admin = UserModel(CF="ADMINCF000000000", nome="First", cognome="Admin", email="admin@admin.com", password="Admin1234", is_admin=True)
            db.session.add(admin)
            db.session.commit()
        self.tomorrow = (date.today() + timedelta(days=1)).isoformat()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def get_auth_header(self, email, password):
        res = self.client.post("/api/login/", json={"email": email, "password": password})
        self.assertEqual(res.status_code, 200, f"Login fallito per {email}")
        data = res.get_json()
        token = data.get("access_token")
        self.assertIsNotNone(token, f"Nessun token per {email}")
        return {"Authorization": f"Bearer {token}"}

    # ------------------- TESTS -------------------

    def test_register_login_and_duplicate(self):
        # registrazione OK
        r1 = self.client.post("/api/register/", json={
            "nome": "Alice", "cognome": "Rossi", "CF": "RSSALC85T10A562S",
            "email": "alice@example.com", "password": "Password1!"
        })
        self.assertEqual(r1.status_code, 201)
        # email duplicata
        r2 = self.client.post("/api/register/", json={
            "nome": "Bob", "cognome": "Bianchi", "CF": "BNCBNC85T10A562S",
            "email": "alice@example.com", "password": "Password1!"
        })
        self.assertEqual(r2.status_code, 409)
        # login corretto
        self.alice_hdr = self.get_auth_header("alice@example.com", "Password1!")
        # login errato
        bad = self.client.post("/api/login/", json={"email": "alice@example.com", "password": "Wrong1!"})
        self.assertEqual(bad.status_code, 401)

    def test_conto_crud_and_limits(self):
        self.test_register_login_and_duplicate()
        hdr = self.alice_hdr
        # GET conti
        r = self.client.get("/api/conti/", headers=hdr)
        self.assertEqual(r.status_code, 200)
        conti = r.get_json()
        self.assertEqual(len(conti), 1)
        # creo 4 altri conti
        for i in range(1, 5):
            rc = self.client.post("/api/conti/", headers=hdr, json={"nome": f"C{i}"})
            self.assertEqual(rc.status_code, 201)
        # 6° conto -> 403
        r6 = self.client.post("/api/conti/", headers=hdr, json={"nome": "X"})
        self.assertEqual(r6.status_code, 403)
        # GET conti max
        r = self.client.get("/api/conti/", headers=hdr)
        self.assertEqual(r.status_code, 200)
        conti = r.get_json()
        self.assertEqual(len(conti), 5)
        # patch nome conto -> 200
        cid = conti[1]["id"]
        rp = self.client.patch(f"/api/conto/{cid}/", headers=hdr, json={"nome": "Nuovo"})
        self.assertEqual(rp.status_code, 200)
        # patch nome conto principale -> 422
        cid = conti[0]["id"]
        rp = self.client.patch(f"/api/conto/{cid}/", headers=hdr, json={"nome": "Nuovo"})
        self.assertEqual(rp.status_code, 422)
        # delete conto principale con permesso admin -> 422
        admin_hdr = self.get_auth_header("admin@admin.com", "Admin1234")
        rd = self.client.delete(f"/api/conto/{cid}/", headers=admin_hdr)
        self.assertEqual(rd.status_code, 422)
        

    def test_deposit_withdraw(self):
        self.test_register_login_and_duplicate()
        hdr = self.alice_hdr
        cid = self.client.get("/api/conti/", headers=hdr).get_json()[0]["id"]
        # deposito
        d = self.client.patch("/api/deposito/", headers=hdr, json={"id_conto": cid, "importo": 100.0})
        self.assertEqual(d.status_code, 201)
        # prelievo eccesso
        o = self.client.patch("/api/prelievo/", headers=hdr, json={"id_conto": cid, "importo": 200.0})
        self.assertEqual(o.status_code, 403)
        # prelievo valido
        ok = self.client.patch("/api/prelievo/", headers=hdr, json={"id_conto": cid, "importo": 50.0})
        self.assertEqual(ok.status_code, 201)

    def test_bonifico_and_movements(self):
        self.test_register_login_and_duplicate()
        hdr = self.alice_hdr
        # registro destinatario
        self.client.post("/api/register/", json={
            "nome": "Recv", "cognome": "User", "CF": "RCTUSR85T10A562S",
            "email": "recv@ex.com", "password": "Password1!"
        })
        # ottengo header admin e ID destinatario
        admin_hdr = self.get_auth_header("admin@admin.com", "Admin1234")
        idb_res = self.client.post("/api/IDbyCF/", headers=admin_hdr, json={"CF": "RCTUSR85T10A562S"})
        self.assertEqual(idb_res.status_code, 200)
        recv_id = idb_res.get_json()["ID"]
        recv_conto = self.client.get(f"/api/conti/{recv_id}", headers=admin_hdr).get_json()[0]
        # fondo mittente
        alice_conto = self.client.get("/api/conti/", headers=hdr).get_json()[0]
        self.client.patch("/api/deposito/", headers=hdr, json={"id_conto": alice_conto["id"], "importo": 100.0})
        # bonifico
        b = self.client.post("/api/bonifico/", headers=hdr, json={
            "beneficiario": "Recv User",
            "id_conto_mittente": alice_conto["id"],
            "importo": 30.0,
            "causale": "T",
            "iban_destinatario": recv_conto["iban"]
        })
        self.assertEqual(b.status_code, 201)
        # movimenti mittente
        mv = self.client.get("/api/movimenti/", headers=hdr).get_json()
        self.assertTrue(any(m["importo"] < 0 for m in mv))
        # movimenti destinatario
        rh_hdr = self.get_auth_header("recv@ex.com", "Password1!")
        mv2 = self.client.get("/api/movimenti/", headers=rh_hdr).get_json()
        self.assertTrue(any(m["importo"] > 0 for m in mv2))

    def test_admin_endpoints(self):
        admin_hdr = self.get_auth_header("admin@admin.com", "Admin1234")
        # get non esistente
        r404 = self.client.get("/api/admin/user/9999/", headers=admin_hdr)
        self.assertEqual(r404.status_code, 404)
        # register + get esistente
        self.test_register_login_and_duplicate()
        rg = self.client.get("/api/admin/user/2/", headers=admin_hdr)
        self.assertEqual(rg.status_code, 200)
        # patch admin-user
        pg = self.client.patch("/api/admin/user/2/", headers=admin_hdr, json={
            "nome": "X", "cognome": "Y", "CF": "NEWCF85T10A562S",
            "email": "new@example.com", "password": "Password1!"
        })
        self.assertEqual(pg.status_code, 200)
        # IDbyCF
        idb2 = self.client.post("/api/IDbyCF/", headers=admin_hdr, json={"CF": "NEWCF85T10A562S"})
        self.assertEqual(idb2.status_code, 200)

    def test_admin_movimenti_and_conto_movimenti(self):
        # usa bonifico per generare movimenti
        self.test_bonifico_and_movements()
        admin_hdr = self.get_auth_header("admin@admin.com", "Admin1234")
        # movimenti admin
        mva = self.client.get("/api/admin/movimenti/2/", headers=admin_hdr)
        self.assertIn(mva.status_code, (200, 204))
        # movimenti conto specifico
        alice_conto = self.client.get("/api/conti/", headers=self.alice_hdr).get_json()[0]
        mvc = self.client.get(f"/api/conto/movimenti/{alice_conto['id']}/", headers=self.alice_hdr)
        self.assertIn(mvc.status_code, (200, 204))

if __name__ == "__main__":
    unittest.main(verbosity=2)
