from app.section1.routes import index_blueprint

def init_app(app):
    app.register_blueprint(index_blueprint)