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

from dotenv import load_dotenv
load_dotenv()


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



DB_HOST = get_env_variable("POSTGRES_DB_HOST")
DB_NAME = get_env_variable("POSTGRES_DB_NAME")
DB_USER = get_env_variable("POSTGRES_DB_USER")
DB_PASS = get_env_variable("POSTGRES_DB_PASS")
DB_PORT = get_env_variable("POSTGRES_DB_PORT")

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