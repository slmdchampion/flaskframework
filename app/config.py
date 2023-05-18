class Config(object):
    TESTING = False
    SECRET_KEY = 'you-will-never-guess'
    SECURITY_PASSWORD_SALT = 'insert_salt_here'
    SQLALCHEMY_DATABASE_URI = 'mariadb+pymysql://testuser:testPassword123!@127.0.0.1:3306/test'