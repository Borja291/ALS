# Importaciones necesarias desde Flask y extensiones
from flask import Blueprint, render_template, redirect, url_for, abort, request
from flask_login import login_required, current_user  # Para proteger rutas y obtener el usuario logueado
from app.forms.review_form import ReviewForm          # Formulario para crear o editar una reseña
from app import get_sirope                            # Base de datos Sirope
from app.core.review import review_service            # Servicio con la lógica de reseñas

# Se define un blueprint llamado "reviews" con el prefijo de ruta "/reviews"
review_routes = Blueprint("reviews", __name__, url_prefix="/reviews")


# Ruta para crear una reseña de una película específica
@review_routes.route("/create/<movie_id>", methods=["GET", "POST"])
@login_required
def create_review(movie_id):
    srp = get_sirope()
    
    # Se busca la película del usuario por su ID
    movie = review_service.find_user_movie_by_id(srp, movie_id)
    if not movie:
        abort(404)  # Si no se encuentra, se lanza error 404

    # Se obtiene el ID de referencia de la película (original si es una copia)
    movie_ref_id = getattr(movie, 'original_movie_id', movie.id)
    
    # Se comprueba si ya existe una reseña de esta película para este usuario
    existing = review_service.find_review_by_movie_and_user(srp, movie_ref_id)
    if existing:
        return redirect(url_for("main_routes.index"))  # Si ya existe, redirige al inicio (no permite duplicados)

    form = ReviewForm()  # Se crea una instancia del formulario

    # Si el formulario es válido tras el POST, se guarda la nueva reseña
    if form.validate_on_submit():
        review_service.save_new_review(srp, movie_ref_id, form.rating.data, form.comment.data)
        return redirect(url_for("main_routes.index"))

    # Si es GET o el formulario no es válido, se muestra el formulario
    return render_template("reviews/review.html", form=form, movie=movie, review=None)


# Ruta para ver la reseña existente de una película
@review_routes.route("/view/<movie_id>")
@login_required
def view_review(movie_id):
    srp = get_sirope()
    
    # Se busca la película del usuario
    movie = review_service.find_user_movie_by_id(srp, movie_id)
    if not movie:
        abort(404)

    # Se obtiene el ID original de la película (por si es una copia)
    movie_ref_id = getattr(movie, 'original_movie_id', movie.id)

    # Se busca la reseña de la película hecha por el usuario actual
    review = review_service.find_review_by_movie_and_user(srp, movie_ref_id)

    # Se muestra la plantilla con la reseña
    return render_template("reviews/view.html", movie=movie, review=review)


# Ruta para crear o actualizar una reseña desde la vista de "reseñar"
@review_routes.route("/reseñar/<movie_id>", methods=["GET", "POST"])
@login_required
def review_movie(movie_id):
    srp = get_sirope()

    # Se busca directamente la película por su ID en la base de datos
    movie = srp.find_first(review_service.Movie, lambda m: m.id == movie_id)
    if not movie:
        abort(404)

    # Se obtiene el ID original en caso de que la película sea una copia
    movie_ref_id = getattr(movie, 'original_movie_id', movie.id)

    # Se busca si ya existe una reseña previa de esta película por el usuario
    existing_review = review_service.find_review_by_movie_and_user(srp, movie_ref_id)

    form = ReviewForm()

    # Si se envía el formulario correctamente
    if form.validate_on_submit():
        if existing_review:
            # Si ya existe, se actualiza la reseña
            review_service.update_existing_review(srp, existing_review, form.rating.data, form.comment.data)
        else:
            # Si no existe, se crea una nueva
            review_service.save_new_review(srp, movie_ref_id, form.rating.data, form.comment.data)

        return redirect(url_for("main_routes.index"))

    # Si ya hay una reseña existente, se rellenan los campos del formulario con sus datos
    if existing_review:
        form.rating.data = existing_review.rating
        form.comment.data = existing_review.comment

    # Se muestra el formulario con la información cargada si aplica
    return render_template("reviews/review.html", form=form, movie=movie, review=existing_review)
