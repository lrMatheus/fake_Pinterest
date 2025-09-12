from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from fakepinters.models import Usuario


class FormLogin(FlaskForm):
    """
    Formulário de login que valida email e senha do usuário.
    """
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("senha", validators=[DataRequired()])
    botao = SubmitField("fazer login")

    def validate_email(self, email):
        """
        Valida se o email existe no banco de dados.
        """
        usuario_existente = Usuario.query.filter_by(email=email.data).first()
        if not usuario_existente:
            raise ValidationError("Nenhum usuário encontrado, crie uma conta para entrar")

class FormCriaConta(FlaskForm):
    """
    Formulário para criar nova conta com validação de email único e confirmação de senha.
    """
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("nome de usuario", validators=[DataRequired()])
    senha = PasswordField("senha", validators=[DataRequired(), Length(6,10)])
    confirma_senha = PasswordField("Confirme a senha", validators=[DataRequired(), EqualTo("senha")])
    botao = SubmitField("criar conta")

    def validate_email(self, email):
        """
        Valida se o email já está cadastrado.
        """
        usuario_existente = Usuario.query.filter_by(email=email.data).first()
        if usuario_existente:
            raise ValidationError("E-mail já cadastrado")
        
class FormFoto(FlaskForm):
    """
    Formulário simples para upload de fotos.
    """
    foto = FileField("Foto", validators=[DataRequired()])
    botao = SubmitField("enviar")