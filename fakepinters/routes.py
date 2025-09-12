"""
Rotas principais do site: login, cadastro, perfil e upload de fotos.
"""
# routes.py

from flask import render_template, url_for, redirect, flash
from fakepinters import app, db, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from fakepinters.forms import FormCriaConta, FormLogin, FormFoto
from fakepinters.models import Usuario, Foto
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import cloudinary.api
import cloudinary
import cloudinary.uploader

load_dotenv()

# Configurar Cloudinary
cloudinary.config(cloudinary_url=os.getenv("CLOUDINARY_URL"))

# página de login e início do site
@app.route("/", methods=["GET", "POST"])
def homepage():
    """
    Exibe a página inicial e processa login do usuário.
    """
    form_Login = FormLogin()
    if form_Login.validate_on_submit():
        usuario_existente = Usuario.query.filter_by(email=form_Login.email.data).first()
        if usuario_existente and bcrypt.check_password_hash(usuario_existente.senha, form_Login.senha.data):
            login_user(usuario_existente, remember=True)
            return redirect(url_for("perfil", id_usuario=usuario_existente.id))
        else:
            flash("E-mail ou senha incorretos", "danger")
    return render_template("homepage.html", form=form_Login)

# página de criar conta
@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    """
    Exibe formulário de cadastro e cria novo usuário.
    """
    form_CriaConta = FormCriaConta()
    if form_CriaConta.validate_on_submit():
        # Criptografa a senha antes de salvar
        cria_senha = bcrypt.generate_password_hash(form_CriaConta.senha.data).decode("utf-8")

        # Cria a instância do novo usuário
        novo_usuario = Usuario(
            username=form_CriaConta.username.data,
            email=form_CriaConta.email.data,
            senha=cria_senha
        )

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            login_user(novo_usuario, remember=True)
            flash("Conta criada e login realizado com sucesso!", "success")
            return redirect(url_for("perfil", id_usuario=novo_usuario.id))
        except Exception as e:
            db.session.rollback()
            flash("Erro ao criar conta. Verifique os dados ou tente outro e-mail.", "danger")

    return render_template("criarconta.html", form=form_CriaConta)

# página de perfil do usuário
@app.route("/perfil/<id_usuario>", methods=["GET","POST"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            
            try:
                # Upload para Cloudinary
                result = cloudinary.uploader.upload(
                    arquivo,
                    folder="fakepinters",
                    transformation=[
                        {'width': 800, 'height': 600, 'crop': 'fill'},
                        {'quality': 'auto'}
                    ]
                )
                
                # URL da imagem otimizada
                url_imagem = result['secure_url']
                
                # Salva no banco
                foto = Foto(imagem=url_imagem, id_usuario=current_user.id)
                db.session.add(foto)
                db.session.commit()
                
                flash("Foto enviada com sucesso!", "success")
                
            except Exception as e:
                flash("Erro ao enviar foto. Tente novamente.", "danger")
                print(f"Erro no upload: {e}")
                
        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None)

# pagina de sair
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout realizado com sucesso!", "info")
    return redirect(url_for("homepage"))

@app.route("/feed")
@login_required
def feed():
    fotos=Foto.query.order_by(Foto.data_post.desc()).all()
    return render_template("feed.html", fotos=fotos)