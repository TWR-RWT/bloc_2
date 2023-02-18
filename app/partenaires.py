#! C:\Users\tgp\AppData\Local\Programs\Python\Python310\python.exe
from functools import wraps
from app import app, psycopg2, render_template, request, session, DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT, flash, redirect, url_for, getcursor
from flask import jsonify, session, send_from_directory, send_file
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

##### PARTENAIRES #####
@app.route('/partenaires', methods=['GET'])
@token_required_contr
def partenaires():
    #conn = get_db()
    #cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    with getcursor() as cur:
        cur.execute("SELECT * FROM assurerplus.partenaires")
        partenaires = cur.fetchall()
        cur.close()
        #conn.close()
        return render_template('partenaires/partenaires.html', partenaires=partenaires)

@app.route('/partenaires/modifier/<string:partenaire_id>', methods=['GET', 'POST'])
@token_required_contr
def red_modif_partenaire(partenaire_id):
    #conn = get_db()
    #cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    with getcursor() as cur:
        cur.execute("SELECT * FROM assurerplus.partenaires WHERE id = %s", (partenaire_id,))
        partenaire = cur.fetchone()
        cur.close()
        #conn.close()
        return render_template('partenaires/modifier_partenaire.html', partenaire=partenaire)

@app.route('/partenaires/modifier_submit/<string:partenaire_id>', methods=['POST'])
@token_required_contr
def submit_modif_partenaire(partenaire_id):
    if request.method == 'POST':
        type = request.form['type']
        entreprise = request.form['Entreprise']
        telephone = request.form['telephone']
        email = request.form['email']
        adresse = request.form['adresse']
        ville = request.form['ville']
        code_postal = request.form['CP']
        website = request.form['website']

        #conn = get_db()
        #cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        with getcursor() as cur:
            cur.execute("UPDATE assurerplus.partenaires SET type_ = %s, entreprise = %s, telephone = %s, email = %s, adresse = %s, ville = %s, code_postal = %s, website = %s WHERE id = %s", (type, entreprise, telephone, email, adresse, ville, code_postal, website, partenaire_id))
            #conn.commit()
            cur.close()
            #conn.close()
            flash('Partenaire modifié avec succès', 'success')
            return redirect(url_for('partenaires'))

@app.route('/partenaires/supprimer/<string:partenaire_id>', methods=['GET', 'POST'])
@token_required_contr
def supprimer_partenaire(partenaire_id):
    #conn = get_db()
    #cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    with getcursor() as cur:
        cur.execute("DELETE FROM assurerplus.partenaires WHERE id = %s", (partenaire_id,))
        #conn.commit()
        cur.close()
        #conn.close()
        flash('Partenaire supprimé avec succès', 'success')
        return redirect(url_for('partenaires'))

@app.route('/partenaires/ajouter', methods=['GET', 'POST'])
@token_required_contr
def ajout_partenaire():
    if request.method == 'POST':
        type = request.form['type']
        entreprise = request.form['Entreprise']
        telephone = request.form['telephone']
        email = request.form['email']
        adresse = request.form['adresse']
        ville = request.form['ville']
        code_postal = request.form['CP']
        website = request.form['website']

        #conn = get_db()
        #cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        with getcursor() as cur:
            cur.execute("INSERT INTO assurerplus.partenaires (type_, entreprise, telephone, email, adresse, ville, code_postal, website) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (type, entreprise, telephone, email, adresse, ville, code_postal, website))
            #conn.commit()
            cur.close()
            #conn.close()

            flash('Partenaire ajouté avec succès', 'success')
            return redirect(url_for('partenaires'))


###### propostions de partenaires #####
@app.route('/partenaires/propositions', methods=['GET'])
@token_required_contr
def propositions_partenaires():
    #conn = get_db()
    #cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    with getcursor() as cur:
        cur.execute("SELECT * FROM assurerplus.partenaires")
        partenaires = cur.fetchall()
        cur.close()
        #conn.close()
        return render_template('partenaires/proposition_partenaire.html', partenaires=partenaires)