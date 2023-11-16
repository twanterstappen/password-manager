from flask import Flask, render_template, redirect, url_for, flash, Blueprint, request, g, session, abort
from flask_mysqldb import MySQL
import os
import secrets
import datetime
from Crypto.Cipher import AES
from flask_qrcode import QRcode
from flask_session import Session

# TODO: https://www.youtube.com/watch?v=lvKjQhQ8Fwk&ab_channel=PrettyPrinted
# Save sessions in a safe way

db = MySQL()
qrcode = QRcode()
sess = Session()


def password_padding(key, target_key_length):
    while len(key) <  target_key_length:
        key += key

    b_formatted_key = key[:target_key_length]
    
    return b_formatted_key



def encrypt_password(key, data):
    b_data = data.encode('UTF-8')
    target_key_length = 32
    
    b_formatted_key = password_padding(key, target_key_length).encode('UTF-8')
        
    # Encryption
    cipher = AES.new(b_formatted_key, AES.MODE_EAX)
    encrypted_password, tag = cipher.encrypt_and_digest(b_data)
    nonce = cipher.nonce
    return encrypted_password, nonce, tag
    

def decryption_password(key, password_hash, nonce, tag):
    target_key_length = 32
    
    b_formatted_key = password_padding(key, target_key_length).encode('UTF-8')
    

    cipher = AES.new(b_formatted_key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(password_hash, tag).decode('UTF-8')

    return data



def main():
    app = Flask(__name__, instance_relative_config=True)
    import view, auth
    # app.secret_key = secrets.token_urlsafe(32)
    app.secret_key = 'asdjflsajflkjskfkdaks'

    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)
    app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
    # app.config['SESSION_PERMANENT'] = True
    app.config['SESSION_FILE_THRESHOLD'] = 30
    app.config['SESSION_TYPE'] = 'filesystem'

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'password_manager'

    
    db.init_app(app)
    qrcode.init_app(app)
    sess.init_app(app)

    app.register_blueprint(view.bp)
    app.register_blueprint(auth.bp)



    return app

if __name__ == '__main__':
    app = main()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)