from flask import Flask
from app import database, section1

def create_app():
    app = Flask(__name__)
    
    # add inits for each section
    

    app.config.from_object('app.config.Config')
    app.config.from_envvar('FLASKFRAMEWORK_SETTINGS')
    

    database.init_app(app)
    section1.init_app(app)
    return app