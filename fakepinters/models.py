from fakepinters import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    """
    Carrega o usuário pelo ID para autenticação.
    """
    return Usuario.query.get(id_usuario)

class Usuario(db.Model, UserMixin):
    """
    Modelo de usuário, armazena dados de login e perfil.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    senha = db.Column(db.String(100), nullable=False)
    fotos = db.relationship("Foto", backref="usuario", lazy=True)

class Foto(db.Model):
    """
    Modelo de foto, armazena imagens postadas pelo usuário.
    """
    id = db.Column(db.Integer, primary_key=True)
    imagem = db.Column(db.String(500), default="default.png")  # Aumentado para URLs do Cloudinary
    data_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)