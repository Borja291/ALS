from flask_wtf import FlaskForm  # Base para formularios seguros en Flask
from wtforms import StringField, IntegerField, DateField, SubmitField  # Tipos de campos del formulario
from wtforms.validators import DataRequired, Length, NumberRange  # Validadores para controlar los datos

# Define el formulario para añadir una nueva película
class MovieForm(FlaskForm):
    # Campo para el título de la película (obligatorio y con al menos 1 carácter)
    title = StringField(
        "Título",
        validators=[DataRequired(), Length(min=1)]
    )

    # Campo numérico para el año de estreno (obligatorio, entre 1888 y 2100)
    year = IntegerField(
        "Año",
        validators=[DataRequired(), NumberRange(min=1888, max=2100)]
    )

    # Campo de texto para el género de la película (obligatorio)
    genre = StringField(
        "Género",
        validators=[DataRequired()]
    )

    # Campo de fecha para indicar cuándo se vio la película (opcional)
    date_watched = DateField(
        "Fecha vista (opcional)"
    )

    # Botón para enviar el formulario
    submit = SubmitField("Añadir película")
