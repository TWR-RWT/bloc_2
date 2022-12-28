#! C:\Users\tgp\AppData\Local\Programs\Python\Python310\python.exe
from app import app, DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT, request, render_template, flash, redirect, url_for, psycopg2
import sys
from flask import Response, jsonify, make_response, session, Flask
import jwt
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash



##### token verification #####
def token_required_auth(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = session.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401
        #try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        #except:
        #    return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return decorated

#############################


##### Page login #####
@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)#
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:#
            cur.execute("""
                    SELECT * FROM assurerplus.accounts 
                    WHERE username = %s
                """, (username,))
            user = cur.fetchone()
            conn.commit()
            cur.close()#
            conn.close()#
            if check_password_hash(user['password'], password):
                token = jwt.encode({'user': user['username'], 'exp': datetime.utcnow() + timedelta(hours=24)}, app.config['SECRET_KEY'])
                session['username'] = username
                session['logged_in'] = True
                session['token'] = token
                session['role'] = user['role']
                session['user_id'] = user['user_id']
                return redirect(url_for('index'))
            else:
                return jsonify({'Message': 'Invalid password'})
        except:#
            return jsonify({'Message': 'Invalid username'})


##### Page logout #####
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

##### Page Gestion utilisateurs #####
@app.route("/users")
@token_required_auth
def users():
    return render_template("authentification/auth.html")

##### Page creation login #####
@app.route('/create', methods=['POST'])
@token_required_auth
def create_user():
#    data = request.get_json()
    
    if request.method == 'POST':
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)#
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        username = request.form['username']
        hashed_password = generate_password_hash(request.form['password'], method='sha256')
        role = request.form['role']

        cur.execute("INSERT INTO assurerplus.accounts (username, password, role) VALUES (%s, %s, %s)", (username, hashed_password, role))
        conn.commit()
        cur.close()#
        conn.close()#
        flash('Compte créée avec succès')
        return redirect(url_for('users'))

