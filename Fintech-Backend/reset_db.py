from app.models import db
from app import create_app

with create_app().app_context():
    db.drop_all()
    db.create_all()
