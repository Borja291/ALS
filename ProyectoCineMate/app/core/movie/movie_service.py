from app.models.movie import Movie  # Importa el modelo de películas
from app.models.watchlist import Watchlist  # Importa el modelo de listas de películas (watchlists)
from flask_login import current_user  # Accede al usuario autenticado actualmente
from sirope import Sirope  # Librería de persistencia de objetos
import unicodedata  # Para normalizar texto eliminando tildes y caracteres especiales
from datetime import date  # Para trabajar con fechas

# Verifica si la fecha de visualización es igual o posterior al año de estreno
def validar_fecha_visualizacion(year: int, date_watched: date) -> bool:
    return date_watched.year >= year

# Normaliza texto eliminando acentos y convirtiendo a minúsculas
def normalizar_texto(texto: str) -> str:
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)  # Descompone caracteres acentuados
        if unicodedata.category(c) != 'Mn'  # Elimina los signos diacríticos (acentos, tildes)
    ).lower()  # Convierte a minúsculas para comparación uniforme

# Añade una nueva película a la base de datos usando datos del formulario
def add_movie_from_form(srp: Sirope, form) -> Movie:
    movie = Movie(
        user_id=current_user.id,  # Asocia la película al usuario actual
        title=form.title.data,
        year=form.year.data,
        genre=form.genre.data,
        date_watched=form.date_watched.data
    )
    srp.save(movie)  # Guarda la película
    return movie  # Devuelve la película creada

# Comprueba si una película ya está en alguna lista del usuario
def is_movie_in_any_watchlist(srp: Sirope, user_id: str, movie_id: str) -> bool:
    watchlists = srp.filter(Watchlist, lambda wl: wl.user_id == user_id)  # Obtiene listas del usuario
    return any(movie_id in wl.movie_ids for wl in watchlists)  # Devuelve True si la película está en alguna lista

# Elimina una película si pertenece al usuario indicado
def delete_movie_if_owned(srp: Sirope, user_id: str, movie_id: str) -> bool:
    for oid in srp.load_all_keys(Movie):  # Recorre todas las claves de películas
        movie = srp.load(oid)  # Carga la película por su clave
        if movie.user_id == user_id and movie.id == movie_id:  # Comprueba propiedad e ID
            srp.delete(oid)  # Elimina la película
            return True  # Confirmación de eliminación
    return False  # No se encontró o no pertenece al usuario

# Comprueba si ya existe una película con mismo título y año para ese usuario
def existe_pelicula_usuario(srp, user_id: str, titulo: str, year: int) -> bool:
    titulo_normalizado = normalizar_texto(titulo)  # Normaliza el título para comparación
    return any(
        normalizar_texto(m.title) == titulo_normalizado and m.year == year
        for m in srp.filter(Movie, lambda m: m.user_id == user_id)  # Busca películas del usuario
    )
