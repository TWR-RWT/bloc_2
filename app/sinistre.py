#! C:\Users\tgp\AppData\Local\Programs\Python\Python310\python.exe
from functools import wraps
from app import app, psycopg2, render_template, request, session, DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT, flash
from flask import jsonify, session
import jwt
from werkzeug.utils import secure_filename
import uuid as uuid
import os

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

##### declarer un Sinistre #####
@app.route("/declation/submit_declaration", methods=['POST'])
@token_required_contr
def submit_declaration():
    print("before if")
    if request.method == 'POST':
        print("after if")
        nom = request.form['nom']
        prenom = request.form['prenom']
        telephone = request.form['telephone']
        email = request.form['email']
        date_sinistre = request.form['date_sinistre']
        adresse_sinistre = request.form['adresse_sinistre']
        description = request.form['description']
        file_sinistre = request.files['file_sinistre'] #request.form['file_sinistre']
        
        #grab image name
        filename = secure_filename(file_sinistre.filename)
        #set uuid
        uuid_filename = str(uuid.uuid1()) +"_"+ filename
        #save the image

        file_sinistre.save(os.path.join(app.config['UPLOAD_FOLDER'], uuid_filename))

        
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        print("after conn")
        
        try:
            cur.execute("""
                INSERT INTO assurerplus.sinistres (id_user, nom, prenom, telephone, email, date_sinistre, adresse_sinistre, description, file_sinistre) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (session.get('user_id') ,nom, prenom, telephone, email, date_sinistre, adresse_sinistre, description, uuid_filename)) #, uuid_filename
            conn.commit()
            cur.close()
            conn.close()
            flash('Sinistre déclaré avec succès')
            return jsonify({'Message': 'Sinistre déclaré avec succès'}) 
        except Exception as e:
            return jsonify({'Message': 'Sinistre non déclaré', 'Error': str(e)})

##### select all Sinistres #####
@app.route("/sinistres")
@token_required_contr
def sinistres():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM assurerplus.sinistres")
    sinistres = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('sinistre/sinistres.html', list_sinistres=sinistres)