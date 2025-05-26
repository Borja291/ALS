from flask import Blueprint, flash, render_template, request, redirect, url_for, abort  # Importaciones de Flask
from flask_login import login_required, current_user  # Requiere usuario logueado
from app import get_sirope  # Función que devuelve la instancia de almacenamiento Sirope
from app.core.explore import explore_service  # Servicio que gestiona la lógica de exploración

# Definimos el Blueprint para las rutas del módulo de exploración
# Todas las rutas aquí tendrán el prefijo /explorar
explore_routes = Blueprint("explore", __name__, url_prefix="/explorar")


# === Ruta para listar películas que el usuario puede importar ===
@explore_routes.route("/importar", methods=["GET"])
@login_required
def import_movie():
    srp = get_sirope()  # Obtiene la base de datos
    importables = explore_service.get_importable_movies(srp)  # Películas que aún no ha visto/importado el usuario
    return render_template("explore/import_movie.html", movies=importables)  # Muestra la vista con esas películas


# === Ruta intermedia POST que redirige a la ruta donde se selecciona la fecha de visualización ===
@explore_routes.route("/importar/redirigir", methods=["POST"])
@login_required
def redirect_to_date():
    movie_id = request.form.get("movie_id")  # Obtiene el ID de la película seleccionada

    if not movie_id:
        # Si no se seleccionó ninguna película, redirige al listado de importables
        return redirect(url_for("explore.import_movie"))

    # Redirige a la ruta donde se selecciona la fecha de visualización de esa película
    return redirect(url_for("explore.import_movie_date", movie_id=movie_id))


# === Ruta para importar una película seleccionando la fecha de visualización ===
@explore_routes.route("/importar/<movie_id>/fecha", methods=["GET", "POST"])
@login_required
def import_movie_date(movie_id):
    srp = get_sirope()  # Accede al almacenamiento
    movie_to_copy = explore_service.get_movie_by_id(srp, movie_id)  # Busca la película por su ID

    if not movie_to_copy:
        # Si no existe la película (ID inválido), devuelve error 404
        abort(404)

    # Si se ha enviado el formulario (POST)
    if request.method == "POST":
        # Crea una copia de la película con la nueva fecha proporcionada
        new_movie = explore_service.copy_movie_with_date(movie_to_copy, request.form.get("date_watched"))

        if new_movie is None:
            # Si la fecha es inválida (por ejemplo, anterior al año de estreno), muestra error
            flash("❗ La fecha de visualización no puede ser anterior al año de estreno.", "danger")
            return render_template("explore/import_date.html", movie=movie_to_copy)

        srp.save(new_movie)  # Guarda la nueva película importada
        return redirect(url_for("main_routes.index"))  # Redirige a la página principal

    # Si GET, muestra el formulario para introducir la fecha de visualización
    return render_template("explore/import_date.html", movie=movie_to_copy)


# === Ruta para mostrar todas las películas guardadas por todos los usuarios ===
@explore_routes.route("/peliculas")
@login_required
def all_movies():
    srp = get_sirope()  # Accede al almacenamiento

    # Obtiene películas únicas con información sobre si el usuario ya las ha importado
    unique_movies = explore_service.get_unique_movies_with_status(srp)

    # Aplica filtro de búsqueda si el usuario escribió algo en el campo de búsqueda
    search_query = request.args.get("search", "").lower()
    if search_query:
        unique_movies = [m for m in unique_movies if search_query in m.title.lower()]

    # Obtiene reseñas por ID de película
    reviews_by_movie = explore_service.get_reviews_by_movie_id(srp)

    # Obtiene los usuarios por ID para mostrar nombres de quienes subieron/reseñaron
    users_by_id = explore_service.get_all_users_by_id(srp)

    # Renderiza la vista general con todas las películas
    return render_template(
        "explore/all_movies.html",
        movies=unique_movies,
        reviews_by_movie=reviews_by_movie,
        users_by_id=users_by_id
    )
