class Config(object):
    TESTING = False
    SECRET_KEY = 'you-will-never-guess'
    SECURITY_PASSWORD_SALT = 'insert_salt_here'
    SQLALCHEMY_DATABASE_URI = 'mariadb+pymysql://QC:bow123@127.0.0.1:3306/calibration'
    SQLALCHEMY_BINDS = {
        "qms": 'mariadb+pymysql://QMS:bob123@127.0.0.1:3306/qms'
    }
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True,}
    REMEMBER_COOKIE_SAMESITE = "strict"
    SESSION_COOKIE_SAMESITE = "strict"