from flask import render_template, redirect, url_for, flash, Blueprint, request, g, session, abort, current_app
from flask_mysqldb import MySQL
from app import db

bp = Blueprint('view', __name__)


@bp.route('/', methods=('GET',))
def home():
    # if 'loggedin' not in session:
    #     return redirect(url_for('auth.login'))
    
    g.passwords = [['google.com', 'aapje123', 'Welkom123!'],['auacb.nl','langemanv1','secret']]
    return render_template('manager/main.html.j2')


@bp.route('/profile', methods=('GET',))
def profile():
    if 'loggedin' not in session:
        return redirect(url_for('auth.login'))
    cursor = db.connection.cursor()
    query = "select * from password;"
    cursor.execute(query,)
    entry = cursor.fetchone()
    
    return f'{entry}'

# Dark theme
@bp.route('/dark', methods=('GET',))
def dark():
    session['dark'] = True
    return redirect(url_for('view.home'))

# Light theme
@bp.route('/light', methods=('GET',))
def light():
    session.pop('dark')
    return redirect(url_for('view.home'))