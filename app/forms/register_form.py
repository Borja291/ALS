from flask_wtf import FlaskForm  # Clase base para formularios con protección CSRF
from wtforms import StringField, PasswordField, SubmitField  # Tipos de campos del formulario
from wtforms.validators import DataRequired, Email, Length  # Validadores para control de entrada

# Formulario de registro de usuario
class RegisterForm(FlaskForm):
    # Campo de texto para el nombre de usuario, obligatorio y con mínimo 3 caracteres
    username = StringField(
        "Nombre de usuario",
        validators=[DataRequired(), Length(min=3)]
    )

    # Campo de texto para el email, obligatorio y con validación de formato de correo
    email = StringField(
        "Correo electrónico",
        validators=[DataRequired(), Email()]
    )

    # Campo de contraseña, obligatorio y con mínimo 4 caracteres
    password = PasswordField(
        "Contraseña",
        validators=[DataRequired(), Length(min=4)]
    )

    # Botón para enviar el formulario
    submit = SubmitField("Registrarse")
