# Importaciones necesarias desde Flask y otras partes del proyecto
from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import login_required, current_user  # Para proteger rutas y obtener el usuario autenticado
from app.forms.movie_form import MovieForm            # Formulario para añadir películas
from app import get_sirope                            # Función para acceder a la base de datos Sirope
from app.core.movie import movie_service              # Servicio con lógica relacionada con películas

# Se crea un Blueprint llamado "movies" con el prefijo de URL "/movies"
movie_routes = Blueprint("movies", __name__, url_prefix="/movies")


# Ruta para añadir manualmente una película mediante un formulario
@movie_routes.route("/add/form", methods=["GET", "POST"])
@login_required
def add_movie_form():
    form = MovieForm()  # Se instancia el formulario de película
    srp = get_sirope()  # Se obtiene la base de datos Sirope

    # Si el formulario ha sido enviado y es válido
    if form.validate_on_submit():
        # Verifica que la fecha de visualización no sea anterior al año de estreno
        if not movie_service.validar_fecha_visualizacion(form.year.data, form.date_watched.data):
            flash("❗ La fecha de visualización no puede ser anterior al año de estreno de la película.", "danger")
            return render_template("movies/add.html", form=form)

        # Comprueba si la película ya ha sido añadida por el usuario
        if movie_service.existe_pelicula_usuario(srp, current_user.id, form.title.data, form.year.data):
            flash("⚠️ Esta película ya está añadida a CineMate.", "warning")
            return redirect(url_for("movies.add_movie_form"))

        # Si pasa todas las validaciones, se añade la película
        movie_service.add_movie_from_form(srp, form)
        return redirect(url_for("main_routes.index"))  # Redirige al inicio

    # Si es una petición GET o el formulario no es válido, se muestra el formulario
    return render_template("movies/add.html", form=form)


# Ruta intermedia que permite al usuario decidir cómo añadir una película (manualmente o importada)
@movie_routes.route("/add", methods=["GET"])
@login_required
def add_movie_decision():
    return render_template("movies/add_decision.html")  # Muestra plantilla con opciones de decisión


# Ruta que maneja la decisión del usuario (POST desde el formulario de decisión)
@movie_routes.route("/add/decision", methods=["POST"])
@login_required
def handle_add_decision():
    decision = request.form.get("decision")  # Obtiene la decisión del formulario
    if decision == "yes":
        return redirect(url_for("explore.import_movie"))  # Redirige a la importación si elige sí
    else:
        return redirect(url_for("movies.add_movie_form"))  # Si no, redirige al formulario manual


# Ruta para eliminar una película
@movie_routes.route("/delete/<movie_id>", methods=["POST"])
@login_required
def delete_movie(movie_id):
    srp = get_sirope()

    # Comprueba si la película está en alguna lista del usuario
    if movie_service.is_movie_in_any_watchlist(srp, current_user.id, movie_id):
        flash("❗ Esta película está en una o más listas temáticas. Debes eliminarla de las listas primero.", "danger")
    else:
        # Intenta eliminar la película si pertenece al usuario
        deleted = movie_service.delete_movie_if_owned(srp, current_user.id, movie_id)
        if deleted:
            flash("✅ Película eliminada correctamente.", "success")
        else:
            flash("❌ No se encontró la película o no tienes permiso para eliminarla.", "warning")

    return redirect(url_for("main_routes.index"))  # Redirige al inicio tras la acción
