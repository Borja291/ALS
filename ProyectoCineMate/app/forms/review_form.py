from flask_wtf import FlaskForm  # Clase base de formularios seguros en Flask
from wtforms import SelectField, TextAreaField, SubmitField  # Tipos de campos utilizados
from wtforms.validators import DataRequired, Length  # Validadores para validar campos

# Formulario para enviar una reseña de una película
class ReviewForm(FlaskForm):
    # Campo de selección para puntuación (obligatorio)
    rating = SelectField(
        "Puntuación",
        choices=[
            ("1", "⭐"),
            ("2", "⭐⭐"),
            ("3", "⭐⭐⭐"),
            ("4", "⭐⭐⭐⭐"),
            ("5", "⭐⭐⭐⭐⭐")
        ],
        validators=[DataRequired()]  # Se requiere seleccionar una opción
    )

    # Campo de texto largo para dejar un comentario, opcional pero limitado a 500 caracteres
    comment = TextAreaField(
        "Comentario",
        validators=[Length(max=500)]
    )

    # Botón para enviar la reseña
    submit = SubmitField("Enviar reseña")
