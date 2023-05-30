from sqlalchemy import text, create_engine, MetaData
from app.database.base import sa

# with app.app_context():
#     db.reflect()

# class User:
#     __table__ = db.metadatas["auth"].tables["user"]

#  insertdata = mybase.table.insert().values(name="angela")
#  db.session.execute(insertdata) 
#  db.session.commit()
# 
# query = mybase.table.select().where(mybase.table.c.name == "angela")
# result = db.session.execute(query)
class Table(sa.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    
class Database:
    # table=sa.Table("table", sa.metadata, autoload_with=sa.engine)

    def __init__(self) -> None:
        #reflect existing tables
        self.table=sa.Table("table", sa.metadata, autoload_with=sa.engine)

    def get_test_table(self):
        result = sa.session.execute(text("SELECT * FROM `test`.`table`"))
        return result
    