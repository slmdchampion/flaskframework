from app.calibration.routes import index_blueprint, calibration_blueprint

def init_app(app):
    app.register_blueprint(index_blueprint)
    app.register_blueprint(calibration_blueprint)