from sqlalchemy import text, create_engine, MetaData
from app.database.base import sa


class Database:
    def get_test_table(self):
        result = sa.session.execute(text("SELECT * FROM `test`.`table`"))
        return result