#! C:\Users\tgp\AppData\Local\Programs\Python\Python310\python.exe
import os
from flask import Flask, render_template, request, flash, redirect, url_for, session
from jinja2 import Template
import psycopg2
import psycopg2.extras
import json
import sys
from urllib import parse
import jwt
from dotenv import load_dotenv
load_dotenv()
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager


# Function to get the environmental variables
def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected env variable '{}' not set.".format(name)
        raise Exception(message)

app = Flask(__name__)

app.secret_key = get_env_variable("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = get_env_variable("UPLOAD_FOLDER")
app.config['SQLALCHEMY_DATABASE_URI'] = get_env_variable("SQLALCHEMY_DATABASE_URI")

DB_HOST = get_env_variable("POSTGRES_DB_HOST")
DB_NAME = get_env_variable("POSTGRES_DB_NAME")
DB_USER = get_env_variable("POSTGRES_DB_USER")
DB_PASS = get_env_variable("POSTGRES_DB_PASS")
DB_PORT = get_env_variable("POSTGRES_DB_PORT")

dbConnection = "dbname="+DB_NAME+" user="+DB_USER+" host="+DB_HOST+" password="+DB_PASS+" port="+DB_PORT

# pool define with 10 live connections
connectionpool = SimpleConnectionPool(1,10,dsn=dbConnection)

#def get_db():
#    db = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
#    return db

@contextmanager
def getcursor():
    con = connectionpool.getconn()
    try:
        yield con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    finally:
        connectionpool.putconn(con)



@app.route("/")
def index():
    if not session.get('logged_in'):
        return render_template('/authentification/login.html')
    elif session.get('role') == 'private':
        return sinistre.sinistres()
    else:
        return sinistre.declaration()

from app import sinistre
from app import authentification
from app import partenaires