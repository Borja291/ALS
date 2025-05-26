from flask_wtf import FlaskForm  # Clase base para formularios seguros con CSRF integrado
from wtforms import StringField, PasswordField, SubmitField  # Tipos de campos para el formulario
from wtforms.validators import DataRequired  # Validador que exige que el campo no esté vacío

# Define un formulario para el inicio de sesión
class LoginForm(FlaskForm):
    # Campo de texto para el nombre de usuario, obligatorio
    username = StringField(
        "Nombre de usuario",
        validators=[DataRequired()]  # No se permite enviar el formulario si está vacío
    )

    # Campo de contraseña, también obligatorio
    password = PasswordField(
        "Contraseña",
        validators=[DataRequired()]  # No se permite dejarlo en blanco
    )

    # Botón para enviar el formulario
    submit = SubmitField("Iniciar sesión")
