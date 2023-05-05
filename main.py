from app import create_app
from database.database import Database

db = Database()
app = create_app(db) 