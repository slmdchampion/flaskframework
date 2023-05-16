from app.database.base import sa

def init_app(app):
    sa.init_app(app)