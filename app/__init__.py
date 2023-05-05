from flask import Flask
from app import database, section1

def create_app():
    app = Flask(__name__)
    
    # add inits for each section
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+pymysql://testuser:testPassword123!@127.0.0.1:3306/test'
    app.config['SECRET_KEY'] = 'you-will-never-guess'
    app.config['SECURITY_PASSWORD_SALT'] = 'insert_salt_here'
    database.init_app(app)
    section1.init_app(app)
    return app