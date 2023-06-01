from flask_security import Security
from app.database.base import sa
from app.database.security import user_datastore

def init_app(app):
    sa.init_app(app)

    security = Security(app, user_datastore)