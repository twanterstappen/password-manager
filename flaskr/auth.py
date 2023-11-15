from flask import render_template, redirect, url_for, flash, Blueprint, request, g, session, abort, app
import bcrypt
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
        
        if password != c_password:
            flash(f"Password not matching", "error")
            return render_template('auth/register.html.j2')
        
        if not token or not username or not email or not password or not c_password:
            flash('Please fill all the fields in!', 'error')
            return render_template('auth/register.html.j2')
        
        
        
        cursor = db.connection.cursor()
        cursor.execute("SELECT email FROM user where email = %s;", (email,))
        entry = cursor.fetchone()
        if entry:
            cursor.close
            flash(f"Email already used", "error")
            return render_template('auth/register.html.j2')
            
        main_password_hash = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
        
        # Need to look into this, I think it wont commit. Because nothing shows up in the database
        cursor.execute("INSERT INTO user (username, email, main_password_hash) VALUES (%s, %s, %s);", (username, email, main_password_hash))
        db.connection.commit()
        cursor.close
        
        
        flash(f"Welcome, you succussfully registerd, please login with your credentials!", "success")
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html.j2')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if 'loggedin' in session:
        return redirect(url_for('view.home'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        
        if not email or not password:
            flash('Please fill in the required fields!', 'error')
            return render_template('auth/login.html.j2')
        
        cursor = db.connection.cursor()
        cursor.execute("SELECT username, email, main_password_hash FROM user WHERE email = %s;", (email,))
        entry = cursor.fetchone()
        username, email_db, main_password_hash = entry
        cursor.close
        
        if entry and bcrypt.checkpw(password, main_password_hash.encode('utf-8')):
            session.permanent = True
            session['loggedin'] = True
            session['username'] = username
            session['email'] = email_db
            session['password'] = password.decode('utf-8')

            
            
            flash(f"Welcome { entry[0] }, you succussfully logged in!", "success")
            
            return redirect(url_for('view.home'))
        else:
            flash('Combination of email and password wrong', 'error')
   
        # query = "select * from password;"
        # cursor.execute(query,)
        # entry = cursor.fetchone()
    

    
    return render_template('auth/login.html.j2')

@bp.route('/logout', methods=('GET',))
def logout():
    if 'loggedin' not in session:
        return redirect(url_for('view.home'))
    
    session.pop('loggedin')
    session.pop('username')
    session.pop('email')
    return redirect(url_for('auth.login'))