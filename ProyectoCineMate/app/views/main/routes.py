# Importaciones necesarias desde Flask y extensiones
from flask import Blueprint, render_template
from flask_login import login_required, current_user  # Para proteger rutas y obtener el usuario logueado
from app import get_sirope  # Función que devuelve la instancia de Sirope (base de datos)
from app.core.main import main_service  # Servicio que gestiona la lógica principal relacionada con películas

# Se define un Blueprint llamado "main_routes" (no tiene prefijo de URL)
main_routes = Blueprint("main_routes", __name__)

# Ruta principal de la aplicación ("/")
@main_routes.route("/")
@login_required  # Solo accesible para usuarios logueados
def index():
    srp = get_sirope()  # Se obtiene la base de datos Sirope
    movies = main_service.get_user_movies(srp, current_user.id)  # Se obtienen las películas del usuario actual
    return render_template("index.html", movies=movies)  # Se renderiza la plantilla principal con las películas del usuario
