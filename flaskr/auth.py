from flask import render_template, redirect, url_for, flash, Blueprint, request, g, session, abort, app
from flask_mysqldb import MySQL


from app import db

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if 'loggedin' in session:
        return redirect(url_for('view.home'))
    
    if request.method == 'POST':
        token = request.form['token']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['c-password']
    
    return render_template('auth/register.html.j2')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if 'loggedin' in session:
        return redirect(url_for('view.home'))
    
    if request.method == 'POST':
        g.email = request.form['email']
        g.password = request.form['password']
    
    
    # session['loggedin'] = True
    return render_template('auth/login.html.j2')

@bp.route('/logout', methods=('GET',))
def logout():
    if 'loggedin' not in session:
        return redirect(url_for('view.home'))
    
    session.clear()
    return 'Hello World'