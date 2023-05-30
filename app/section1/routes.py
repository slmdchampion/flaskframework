from flask import Blueprint, render_template, request, redirect, url_for
from app.database.database import Database, Table
from app.database.base import sa


index_blueprint = Blueprint('index', __name__, template_folder='templates', static_folder='static')

# uses SQL directly to query the database
@index_blueprint.route("/")
def index():
    mybase=Database()
    result=mybase.get_test_table()
    return render_template('index.html', title='Home', table_data=result)

# uses the ORM to query the database
@index_blueprint.route("/page1")
def page1():
    result=sa.session.scalars(sa.select(Table)).all()
    return render_template('page1.html', title='Page1', table_data=result)
 