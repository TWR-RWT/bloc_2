#! C:\Users\tgp\AppData\Local\Programs\Python\Python310\python.exe
from functools import wraps
from app import app, psycopg2, render_template
from flask import jsonify, session
import jwt


##### token verification #####
def token_required_contr(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = session.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401
        try:#
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:#
            return jsonify({'Message': 'Invalid token'}), 403#
        return func(*args, **kwargs)
    return decorated

##### Page Sinistre #####
@app.route("/declaration")
@token_required_contr
def declaration():
    return render_template('sinistre/declaration.html')