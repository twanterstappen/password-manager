from flask import Flask, render_template, redirect, url_for, flash, Blueprint, request, g, session, abort
from flask_mysqldb import MySQL
import os
import secrets
import datetime


db = MySQL()



def main():
    app = Flask(__name__, instance_relative_config=True)
    import view, auth
    app.secret_key = secrets.token_urlsafe(32)

    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)
    app.config['SESSION_COOKIE_SAMESITE'] = None

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'password_manager'
    
    db.init_app(app)

    app.register_blueprint(view.bp)
    app.register_blueprint(auth.bp)



    return app
if __name__ == '__main__':
    app = main()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)