from flask_wtf import FlaskForm  # Base para formularios en Flask con CSRF y validaciones integradas
from wtforms import StringField, TextAreaField, SubmitField  # Campos del formulario
from wtforms.validators import DataRequired, Length  # Validadores para asegurar formato correcto

# Define un formulario para crear una nueva lista de películas (watchlist)
class WatchlistForm(FlaskForm):
    # Campo de texto para el nombre de la lista, obligatorio y con longitud entre 1 y 50 caracteres
    name = StringField(
        "Nombre de la lista",
        validators=[DataRequired(), Length(min=1, max=50)]
    )

    # Campo de área de texto para la descripción, opcional pero con máximo 200 caracteres
    description = TextAreaField(
        "Descripción",
        validators=[Length(max=200)]
    )

    # Botón para enviar el formulario
    submit = SubmitField("Crear lista")
