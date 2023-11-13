from flask import render_template, redirect, url_for, flash, Blueprint, request, g, session, abort, current_app
from flask_mysqldb import MySQL
from app import db

bp = Blueprint('view', __name__)


@bp.route('/', methods=('GET',))
def home():
    if 'loggedin' not in session:
        return redirect(url_for('auth.login'))
    return render_template('manager/password.html')


@bp.route('/profile', methods=('GET',))
def profile():
    if 'loggedin' not in session:
        return redirect(url_for('auth.login'))
    cursor = db.connection.cursor()
    query = "select * from password;"
    cursor.execute(query,)
    entry = cursor.fetchone()
    
    return f'{entry}'