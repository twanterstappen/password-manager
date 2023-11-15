from flask import render_template, redirect, url_for, flash, Blueprint, request, g, session, abort, current_app
from app import db, encrypt_password, decryption_password


bp = Blueprint('view', __name__)


@bp.route('/', methods=('GET',))
def home():
    if 'loggedin' not in session:
        return redirect(url_for('auth.login'))

    
    key = session.get('password')
    email = session.get('email')
    cursor = db.connection.cursor()
    
    
    cursor.execute("""  SELECT p.id, p.website, p.username, p.password_hash, p.nonce, p.tag, p.note
                        FROM password_manager.user u
                        JOIN password_manager.password p ON u.id = p.user_id
                        WHERE u.email = 'twanterstappen@gmail.com';""")
    entry = cursor.fetchall()
    cursor.close
    passwords = []
    for e in entry:
        id, website, username, password_hash, nonce, tag, note = e

        d_password = decryption_password(key, password_hash, nonce, tag)
        passwords.append([id, website, username, d_password, note])

    
    g.passwords = passwords
    
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

@bp.route('/add-password', methods=('get', 'post'))
def addpassword():

    # password = request.form['password_hash']
    if request.method == 'post':
        email = session.get('email')
        key = session.get('password')

        website = 'google.com.test'
        username = 'Username_test123!'
        note = 'This is a test note for testing'
        
        password_hash, nonce, tag = encrypt_password(key, 'hope this works')

        
        cursor = db.connection.cursor()
        cursor.execute("SELECT id FROM user where email = %s;", (email,))
        user_id = cursor.fetchone()[0]

        cursor.execute("INSERT INTO password (website, username, password_hash, nonce, tag, note, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s);", (website, username, password_hash, nonce, tag, note, user_id))
        db.connection.commit()
        
        cursor.close

        
        
        return f'{password_hash, nonce, tag}'
    return redirect(url_for('view.addpassword'))
    
