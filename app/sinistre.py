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
        ville = request.form['ville']
        code_postal = request.form['code_postal']
        description = request.form['description']
        file_sinistre = request.files['file_sinistre'] #request.form['file_sinistre']
        
        if file_sinistre.filename == '':
            uuid_filename = None
        else:
            #grab image name
            filename = secure_filename(file_sinistre.filename)
            #set uuid
            uuid_filename = str(uuid.uuid1()) +"_"+ filename
            #save the image
            file_sinistre.save(os.path.join(app.config['UPLOAD_FOLDER'], uuid_filename))

        #conn = get_db()
        #conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
        #cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        #print("after conn")
        
        try:
            with getcursor() as cur:
                cur.execute("""
                    INSERT INTO assurerplus.sinistres (id_user, nom, prenom, telephone, email, date_sinistre, adresse_sinistre, ville_sinistre, code_postal_sinistre, description, file_sinistre) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (session.get('user_id') ,nom, prenom, telephone, email, date_sinistre, adresse_sinistre, ville, code_postal, description, uuid_filename)) #, uuid_filename
                #conn.commit()
                cur.close()
                #conn.close()
                flash('Sinistre déclaré avec succès')
                return redirect(url_for('mes_sinistres'))
        except Exception as e:
            return jsonify({'Message': 'Sinistre non déclaré', 'Error': str(e)})

##### select all Sinistres #####
@app.route("/sinistres")
@token_required_contr
def sinistres():
    #conn = get_db()
    #conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
    #cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    with getcursor() as cur:
        cur.execute("SELECT * FROM assurerplus.sinistres")
        sinistres = cur.fetchall()
        cur.close()
        #conn.close()
    return render_template('sinistre/sinistres.html', list_sinistres=sinistres)


##### sinistres_modif #####
@app.route("/sinistres/<string:id>", methods=['POST', 'GET'])
@token_required_contr
def sinistres_modif(id):
    if request.method == 'POST':
        print("after if")
        name_attribut = "statut_"+id
        statut = request.form[name_attribut]
        #conn = get_db()
        #conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
        #cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try: 
            with getcursor() as cur:
                cur.execute(""" UPDATE assurerplus.sinistres SET status = %s WHERE id_sinistre = %s
                """, (statut, id))
                #conn.commit()
                cur.execute("SELECT * FROM assurerplus.sinistres")
                sinistres = cur.fetchall()
                cur.close()
                #conn.close()
                return render_template('sinistre/sinistres.html', list_sinistres=sinistres)
        except Exception as e:
            return e

##### sinistres_modif_com #####
@app.route("/sinistres/modif_com/<string:id>", methods=['POST', 'GET'])
@token_required_contr
def sinistres_modif_com(id):
    if request.method == 'POST':
        print("after if")
        name_attribut = "commentaire"
        commentaire = request.form[name_attribut]
        #conn = get_db()
        #conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
        #cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try: 
            with getcursor() as cur:
                cur.execute(""" UPDATE assurerplus.sinistres SET commentaires = %s WHERE id_sinistre = %s
                """, (commentaire, id))
                #conn.commit()
                cur.execute("SELECT * FROM assurerplus.sinistres")
                sinistres = cur.fetchall()
                cur.close()
                #conn.close()
                return render_template('sinistre/sinistres.html', list_sinistres=sinistres)
        except Exception as e:
            return e

##### select mes_sinistres #####
@app.route("/mes_sinistres")
@token_required_contr
def mes_sinistres():
    #conn = get_db()
    #conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
    #cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    with getcursor() as cur:
        cur.execute("SELECT * FROM assurerplus.sinistres WHERE id_user = %s", (session.get('user_id'),))
        mes_sinistres = cur.fetchall()
        cur.close()
        #conn.close()
        return render_template('sinistre/mes_sinistres.html', list_mes_sinistres=mes_sinistres)

##### See picture #####
@app.route('/download/<filename>')
def download_file(filename):
    path_to_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(path_to_file[4:], as_attachment=True)

##### delete picture #####
@app.route('/<sinistre_id>/delete/<filename>')
def delete_file(sinistre_id, filename):
    try:
        #conn = get_db()
        #conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
        #cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        with getcursor() as cur:
            cur.execute("""UPDATE assurerplus.sinistres SET file_sinistre = NULL WHERE id_sinistre = %s
            """, (sinistre_id,))
            #conn.commit()
            cur.close()
            #conn.close()
            path_to_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.remove(path_to_file)
            return redirect(url_for('mes_sinistres'))
    except Exception as e:
        return e

##### upload picture #####
@app.route('/<sinistre_id>/upload', methods=['POST'])
def upload_file(sinistre_id):
    if request.method == 'POST':
        file = request.files['picture'] #request.form['file_sinistre']
        
        if file.filename == '':
            uuid_filename = None
            flash("Vous devez uploader une image d'abord")
            return redirect(url_for('mes_sinistres'))
        else:
            #grab image name
            filename = secure_filename(file.filename)
            #set uuid
            uuid_filename = str(uuid.uuid1()) +"_"+ filename
            #save the image
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], uuid_filename))
            #conn = get_db()
            #cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            #print("after conn")
            try:
                with getcursor() as cur:
                    cur.execute("""
                        UPDATE assurerplus.sinistres SET file_sinistre = %s WHERE id_sinistre = %s
                    """, (uuid_filename, sinistre_id))

                    #conn.commit()
                    cur.close()
                    #conn.close()
                    flash('Sinistre déclaré avec succès')
                    return redirect(url_for('mes_sinistres'))
            except Exception as e:
                return jsonify({'Message': 'Sinistre non déclaré', 'Error': str(e)})


##### redirection modif_declaration #####
@app.route("/sinistres/modif_declaration/<string:sinistre_id>", methods=['POST', 'GET'])
@token_required_contr
def red_modif_declaration(sinistre_id):
    #conn = get_db()
    #cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    with getcursor() as cur:
        cur.execute("SELECT * FROM assurerplus.sinistres WHERE id_sinistre = %s", (sinistre_id,))
        sinistre = cur.fetchone()
        cur.close()
        #conn.close()
    if sinistre['file_sinistre'] == None:
        sinistre_file_string ="empty_file"
    else:
        sinistre_file_string = sinistre['file_sinistre']
    return render_template('sinistre/modif_declaration.html', sinistre=sinistre, sinistre_file=sinistre_file_string)

##### submit modif_declaration #####
@app.route("/sinistres/submit_modif_declaration/<string:sinistre_id>/<string:sinistre_file>", methods=['POST', 'GET'])
@token_required_contr
def submit_modif_declaration(sinistre_id, sinistre_file):
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        telephone = request.form['telephone']
        email = request.form['email']
        date_sinistre = request.form['date_sinistre']
        adresse_sinistre = request.form['adresse_sinistre']
        ville = request.form['ville']
        code_postal = request.form['code_postal']
        description = request.form['description']
        checked = request.form.get('check')
        if checked != "on":
            #conn = get_db()
            #cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            # UPDATE assurerplus.sinistres SET nom = %s, prenom = %s, telephone = %s, email = %s, date_sinistre = %s, adresse_sinistre = %s, description = %s, checked = %s WHERE id_sinistre = %s
            
            with getcursor() as cur:
                cur.execute("""
                    UPDATE assurerplus.sinistres SET nom = %s, prenom = %s, telephone = %s, email = %s, date_sinistre = %s, adresse_sinistre = %s, ville_sinistre = %s, code_postal_sinistre = %s, description = %s WHERE id_sinistre = %s
                """, (nom, prenom, telephone, email, date_sinistre, adresse_sinistre, ville, code_postal, description, sinistre_id))
                #conn.commit()
                cur.close()
                #conn.close()
                flash('Sinistre modifié avec succès')
                return redirect(url_for('mes_sinistres'))
        else:
            try:
                file_sinistre = request.files['file_sinistre'] #request.form['file_sinistre']
                if sinistre_file != "empty_file":
                    path_to_file = os.path.join(app.config['UPLOAD_FOLDER'], sinistre_file)
                    os.remove(path_to_file)
                if file_sinistre.filename == '':
                    uuid_filename = None
                else:
                    #grab image name
                    filename = secure_filename(file_sinistre.filename)
                    #set uuid
                    uuid_filename = str(uuid.uuid1()) +"_"+ filename
                    #save the image
                    file_sinistre.save(os.path.join(app.config['UPLOAD_FOLDER'], uuid_filename))
                #conn = get_db()
                #cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                with getcursor() as cur:
                    cur.execute("""
                        UPDATE assurerplus.sinistres SET nom = %s, prenom = %s, telephone = %s, email = %s, date_sinistre = %s, adresse_sinistre = %s, ville_sinistre = %s, code_postal_sinistre = %s, description = %s, file_sinistre = %s WHERE id_sinistre = %s
                    """, (nom, prenom, telephone, email, date_sinistre, adresse_sinistre, ville, code_postal, description, uuid_filename, sinistre_id))
                    #conn.commit()
                    cur.close()
                    #conn.close()
                    flash('Sinistre modifié avec succès')
                    return redirect(url_for('mes_sinistres'))
            except Exception as e:
                return jsonify({'Message': 'Sinistre non déclaré', 'Error': str(e)})