from flask import render_template, redirect, url_for, flash, Blueprint, request, g, session, abort, current_app
from app import db, encrypt_password, decryption_password
from hashlib import sha1
import requests


bp = Blueprint('view', __name__)
@bp.route('/', methods=('GET',))
def home():
    if 'loggedin' not in session:
        return redirect(url_for('auth.login'))

    
    key = session.get('main_password')
    email = session.get('email')
    cursor = db.connection.cursor()
    
    
    cursor.execute("""  SELECT p.id, p.website, p.username, p.password_hash, p.nonce, p.tag
                        FROM password_manager.user u
                        JOIN password_manager.password p ON u.id = p.user_id
                        WHERE u.email = %s;""",(email,))
    entry = cursor.fetchall()
    cursor.close
    passwords = []
    for e in entry:
        id, website, username, password_hash, nonce, tag = e

        d_password = decryption_password(key, password_hash, nonce, tag)
        passwords.append([id, website, username, d_password])

    
    g.passwords = passwords
    return render_template('manager/main.html.j2')



@bp.route('/add-credentials', methods=('GET', 'POST'))
def addcredentials():
    if 'loggedin' not in session:
        return redirect(url_for('auth.login'))
    
    

    if request.method == 'POST':
        if request.form.get('check-password'):
            check_password = request.form.get('check-password').encode('utf-8')
            hash_object = sha1(check_password)
            sha1_hex_check_password = hash_object.hexdigest()
            check_password_list = sha1_hex_check_password[:5], sha1_hex_check_password[5:]

            
            response_api = requests.get('https://api.pwnedpasswords.com/range/%s' % check_password_list[0])
            if response_api.status_code == 200:
                loop_flag = False
                response_lines = response_api.text.lower().strip().split('\n')
                for line in response_lines:
                    hash_value, count = line.split(':')
                    # print(hash_value.lower(), check_password_list[1].lower())
                    if hash_value == check_password_list[1]:
                        flash("Your password is pwned and seen %s times" % count, "warning")
                        loop_flag = True
                        break
                if not loop_flag:
                    flash("Password isn't pwned, you're safe to use this password!", "success")
                        
                        
                        
            else:
                flash("Something went wrong, couldn't make request to the api", "error")


            
        else:
            key = session.get('main_password')
            email = session.get('email')
            website = request.form.get('add-website')
            username = request.form.get('add-username')
            password = request.form.get('add-password')


            
            password_hash, nonce, tag = encrypt_password(key, password)

            
            cursor = db.connection.cursor()
            cursor.execute("SELECT id FROM user WHERE email = %s;", (email,))
            user_id = cursor.fetchone()[0]
            
            
            cursor.execute("INSERT INTO password (website, username, password_hash, nonce, tag, user_id) VALUES (%s, %s, %s, %s, %s, %s);", (website, username, password_hash, nonce, tag, user_id))
            db.connection.commit()
            cursor.close
            flash("Login credentials saved for %s" % website, "success" )
            return redirect(url_for('view.home'))
        
        
    return render_template('manager/add-password.html.j2')
    
    
    
@bp.route('/delete-credentials', methods=('POST',))
def deletecredentials():
    if 'loggedin' not in session:
        return redirect(url_for('auth.login'))
    
    if request.form.get('id'):
        password_id = request.form.get('id')
        email = session.get('email')
        
        cursor = db.connection.cursor()
        cursor.execute("SELECT id FROM user WHERE email = %s;", (email,))
        user_id = cursor.fetchone()[0]
        
        
        cursor.execute("DELETE FROM password WHERE id=%s AND user_id = %s", (password_id, user_id))
        db.connection.commit()
        cursor.close
    
    return redirect(url_for('view.home'))
