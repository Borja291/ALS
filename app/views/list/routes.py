# Importaciones necesarias desde Flask y otros módulos del proyecto
from flask import Blueprint, flash, render_template, redirect, url_for, request, abort
from flask_login import login_required, current_user
from app.forms.list_form import WatchlistForm             # Formulario para crear o editar listas
from app import get_sirope                                # Función para obtener la instancia de Sirope (persistencia de datos)
from app.core.list import list_service                    # Servicio que maneja la lógica relacionada con las listas

# Se define un blueprint llamado "lists" con prefijo de ruta "/lists"
list_routes = Blueprint("lists", __name__, url_prefix="/lists")


# Ruta para crear una nueva lista de seguimiento
@list_routes.route("/create", methods=["GET", "POST"])
@login_required  # Solo accesible si el usuario ha iniciado sesión
def create_list():
    form = WatchlistForm()  # Se crea una instancia del formulario
    srp = get_sirope()  # Se obtiene la instancia de Sirope
    movies = list_service.get_user_movies(srp, current_user.id)  # Se obtienen las películas del usuario actual

    # Si el formulario es válido tras ser enviado (POST)
    if form.validate_on_submit():
        selected_ids = request.form.getlist("movie_ids")  # Se obtienen las películas seleccionadas
        list_service.create_watchlist(srp, form, selected_ids)  # Se crea la lista usando el servicio
        return redirect(url_for("lists.view_lists"))  # Redirige al listado de listas

    # Si es una petición GET, se renderiza el formulario con las películas disponibles
    return render_template("lists/create.html", form=form, movies=movies)


# Ruta para ver todas las listas de seguimiento del usuario actual
@list_routes.route("/")
@login_required
def view_lists():
    srp = get_sirope()
    lists = list_service.get_user_watchlists(srp, current_user.id)  # Se obtienen todas las listas del usuario
    return render_template("lists/index.html", lists=lists)  # Se renderiza la vista con las listas


# Ruta para gestionar (editar) una lista existente
@list_routes.route("/<list_id>", methods=["GET", "POST"])
@login_required
def manage_list(list_id):
    srp = get_sirope()
    # Se obtiene la lista por ID y se comprueba que pertenece al usuario actual
    watchlist = list_service.get_watchlist_by_id(srp, current_user.id, list_id)
    if not watchlist:
        abort(404)  # Si no existe o no es del usuario, error 404

    movies = list_service.get_user_movies(srp, current_user.id)  # Películas disponibles para agregar a la lista

    # Si se envía el formulario (POST), se actualizan las películas en la lista
    if request.method == "POST":
        selected_ids = request.form.getlist("movie_ids")
        list_service.update_watchlist_movies(srp, watchlist, selected_ids)  # Se actualiza la lista
        return redirect(url_for("lists.view_lists"))  # Redirige a la vista de todas las listas

    # Si es GET, se muestra la vista de edición
    return render_template("lists/manage.html", watchlist=watchlist, movies=movies)


# Ruta para ver los detalles de una lista (películas incluidas)
@list_routes.route("/view/<list_id>")
@login_required
def view_list_detail(list_id):
    srp = get_sirope()
    watchlist = list_service.get_watchlist_by_id(srp, current_user.id, list_id)  # Se obtiene la lista del usuario
    if not watchlist:
        abort(404)  # Si no existe o no es del usuario, error 404

    # Se obtienen las películas contenidas en esa lista
    movies = list_service.get_movies_in_watchlist(srp, current_user.id, watchlist.movie_ids)
    return render_template("lists/view.html", watchlist=watchlist, movies=movies)  # Se muestra la lista y las pelis


# Ruta para eliminar una lista de seguimiento
@list_routes.route("/delete/<list_id>", methods=["POST"])
@login_required
def delete_watchlist(list_id):
    srp = get_sirope()

    # Intenta eliminar la lista solo si pertenece al usuario actual
    if list_service.delete_watchlist_if_owned(srp, current_user.id, list_id):
        flash("✅ Lista eliminada correctamente.", "success")  # Mensaje de éxito
    else:
        flash("❗ No se pudo encontrar la lista o no tienes permiso.", "danger")  # Mensaje de error

    return redirect(url_for("lists.view_lists"))  # Redirige a la lista de listas
