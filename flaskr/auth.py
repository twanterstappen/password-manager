from flask import render_template, redirect, url_for, flash, Blueprint, request, g, session, abort, app
import bcrypt
from app import db, qrcode
import pyotp


bp = Blueprint('auth', __name__)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if 'loggedin' in session:
        return redirect(url_for('view.home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        c_password = request.form.get('c-password')

        
        if password != c_password:
            flash(f"Password not matching", "error")
            return render_template('auth/register.html.j2')
        
        if not username or not email or not password or not c_password:
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
        
        cursor.execute("INSERT INTO user (username, email, main_password_hash) VALUES (%s, %s, %s);", (username, email, main_password_hash))
        db.connection.commit()
        cursor.close
        
        session['email'] = email
        flash(f"You succussfully registerd, please login with your credentials!", "success")
        return redirect(url_for('auth.totp'))
    
    return render_template('auth/register.html.j2')



@bp.route('/totp', methods=('GET', 'POST'))
def totp():
    email = session.get('email')
    
    if request.method == 'POST':
        totp_secret = request.form.get('totp_secret')
        code = request.form.get('code')

        totp = pyotp.TOTP(totp_secret)
        if totp.verify(code):
            
            
            cursor = db.connection.cursor()
            cursor.execute("UPDATE user SET totp_secret = %s WHERE email = %s", (totp_secret, email))
            db.connection.commit()
            cursor.close
            
            session.clear()
            flash('TOTP code was correct, please login first', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('TOTP code was not correct, try again!', 'error')
            return render_template('auth/totp.html.j2')
    else:
        secret = pyotp.random_base32()
        g.totp_secret = secret

        g.totp_uri = f'otpauth://totp/2fa-pm:{email}?secret={secret}&issuer=2fa-pm'
        "otpauth://totp/Example:alice@google.com?secret=JBSWY3DPEHPK3PXP&issuer=Example"

    return render_template('auth/totp.html.j2')



@bp.route('/login', methods=('GET', 'POST'))
def login():
    if 'loggedin' in session:
        return redirect(url_for('view.home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password').encode('utf-8')
        totp_code = request.form.get('totp').encode('utf-8')
        
        if not email or not password or not totp_code:
            flash('Please fill all the fields in!', 'error')
            return render_template('auth/login.html.j2')
        
        cursor = db.connection.cursor()
        cursor.execute("SELECT username, email, main_password_hash, totp_secret FROM user WHERE email = %s;", (email,))
        entry = cursor.fetchone()
        username, email_db, main_password_hash, totp_secret = entry
        cursor.close
        
        if entry and bcrypt.checkpw(password, main_password_hash.encode('utf-8')):
            totp = pyotp.TOTP(totp_secret)
            if totp.verify(int(totp_code)):
                session.permanent = True
                session['loggedin'] = True
                session['username'] = username
                session['email'] = email_db
                session['main_password'] = password.decode('utf-8')
                
                flash(f"Welcome { entry[0] }, you succussfully logged in!", "success")
                
                return redirect(url_for('view.home'))
            else:
                flash('TOTP code was not correct, try again!', 'error')
        else:
            flash('Combination of email and password wrong', 'error')
   
    return render_template('auth/login.html.j2')

@bp.route('/logout', methods=('GET',))
def logout():
    if 'loggedin' not in session:
        return redirect(url_for('view.home'))
    
    session.clear()
    return redirect(url_for('auth.login'))