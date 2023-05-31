from flask_security import SQLAlchemySessionUserDatastore
from app.database.base import sa,security
from app.database.security import User, Role

def init_app(app):
    sa.init_app(app)
    user_datastore = SQLAlchemySessionUserDatastore(sa.session, User, Role)
    security.init_app(app, user_datastore)