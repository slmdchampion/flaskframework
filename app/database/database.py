from flask_sqlalchemy import Text, create_engine, MetaData
from database.base import sa


class Database:
    def __init__(self) -> None:
        pass
        # engine = sa.create_engine("mariadb+pymysql://testuser:testPassword123!@127.0.0.1:330?6/test")
        # result = sa.session.execute(text("SELECT * FROM `test`.`table`"))