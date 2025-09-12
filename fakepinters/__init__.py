"""
Inicializa o app Flask, banco de dados, login e configurações.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import pymysql
import urllib.parse

# Configurar PyMySQL para MySQL
pymysql.install_as_MySQLdb()

load_dotenv()

app = Flask(__name__)

# Configuração do Flask
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')


# Configuração do PostgreSQL (Render)
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_HOST = os.getenv('PG_HOST', 'localhost')
PG_PORT = os.getenv('PG_PORT', '5432')
PG_DATABASE = os.getenv('PG_DATABASE')

# Checagem simples para variáveis essenciais
if not all([PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_DATABASE]):
    raise RuntimeError('Variáveis de ambiente do banco de dados PostgreSQL não estão completamente definidas!')

pg_password = urllib.parse.quote_plus(PG_PASSWORD or "")

# cloudinary
cloudinary_url = os.getenv("CLOUDINARY_URL")
if cloudinary_url:
	os.environ["CLOUDINARY_URL"] = cloudinary_url


# Monta a URI do banco de dados PostgreSQL
DATABASE_URI = f"postgresql://{PG_USER}:{pg_password}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"

from fakepinters import routes