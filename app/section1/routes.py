from flask import Blueprint, render_template, request, redirect, url_for
from app.database.calibration import Database

index_blueprint = Blueprint('index', __name__, template_folder='templates', static_folder='static')
mybase = Database()

@index_blueprint.route("/")
def index():
    result=mybase.get_test_table()
    return render_template('index.html', title='Home', table_data=result)
 