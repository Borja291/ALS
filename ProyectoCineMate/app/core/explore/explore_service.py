from app.models.movie import Movie  # Importa el modelo Movie
from app.models.review import Review  # Importa el modelo Review
from app.models.user import User  # Importa el modelo User
from flask_login import current_user  # Importa la variable que representa al usuario logueado actualmente
from collections import defaultdict  # Importa defaultdict para agrupar reseñas por película
import uuid  # Importa uuid para generar identificadores únicos
import datetime  # Importa datetime para trabajar con fechas
from sirope import Sirope  # Importa Sirope, el sistema de persistencia de objetos

# Devuelve todas las películas que se pueden importar (no duplicadas ni del mismo usuario)
def get_importable_movies(srp: Sirope) -> list[Movie]:
    all_movies = list(srp.load_all(Movie))  # Carga todas las películas de la base de datos
    user_movies = list(srp.filter(Movie, lambda m: m.user_id == current_user.id))  # Películas del usuario actual

    # Crea un conjunto con (título, año) de las películas del usuario para detectar duplicados
    existing = {(m.title, m.year) for m in user_movies}

    # Devuelve películas que no estén ya añadidas por el usuario y que pertenezcan a otros usuarios
    return [m for m in all_movies if (m.title, m.year) not in existing and m.user_id != current_user.id]

# Busca una película por su ID
def get_movie_by_id(srp: Sirope, movie_id: str) -> Movie | None:
    all_movies = list(srp.load_all(Movie))  # Carga todas las películas
    # Devuelve la primera que coincida con el ID o None si no se encuentra
    return next((m for m in all_movies if m.id == movie_id), None)

# Crea una copia de una película con una nueva fecha de visualización
def copy_movie_with_date(original_movie: Movie, date_str: str) -> Movie | None:
    try:
        # Intenta convertir el string de fecha a objeto datetime
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        # Si hay error en el formato de fecha, usa la fecha actual
        date = datetime.datetime.now().date()

    # Verifica que la fecha no sea anterior al año de estreno
    if date.year < original_movie.year:
        return None  # No permite copiar si la fecha es anterior al estreno

    # Retorna una nueva instancia de Movie con nuevos identificadores y manteniendo la referencia a la película original
    return Movie(
        user_id=current_user.id,
        title=original_movie.title,
        year=original_movie.year,
        genre=original_movie.genre,
        date_watched=date,
        movie_id=str(uuid.uuid4()),  # Genera nuevo ID único
        original_user_id=getattr(original_movie, 'original_user_id', original_movie.user_id),  # Mantiene el autor original
        original_movie_id=getattr(original_movie, 'original_movie_id', original_movie.id)  # Mantiene la referencia a la película fuente
    )

# Devuelve una lista de películas únicas con una bandera de si ya han sido añadidas por el usuario
def get_unique_movies_with_status(srp: Sirope) -> list[Movie]:
    all_movies = list(srp.load_all(Movie))  # Carga todas las películas
    user_movies = list(srp.filter(Movie, lambda m: m.user_id == current_user.id))  # Películas del usuario actual
    user_titles = {(m.title.lower(), m.year) for m in user_movies}  # Conjunto de títulos y años del usuario

    seen = set()  # Para evitar duplicados
    result = []  # Lista de resultado

    for movie in all_movies:
        key = (movie.title.lower(), movie.year)  # Clave única para comparar
        if key not in seen:
            # Marca si ya ha sido añadida por el usuario actual
            movie.already_added = key in user_titles

            # Asegura que cada película tenga un ID de película original
            if not hasattr(movie, 'original_movie_id') or movie.original_movie_id is None:
                movie.original_movie_id = movie.id

            result.append(movie)
            seen.add(key)

    return result

# Devuelve un diccionario con listas de reseñas agrupadas por ID de película
def get_reviews_by_movie_id(srp: Sirope) -> dict[str, list[Review]]:
    reviews = list(srp.load_all(Review))  # Carga todas las reseñas
    reviews_by_movie = defaultdict(list)  # Diccionario con listas por defecto

    # Agrupa las reseñas por ID de película
    for r in reviews:
        reviews_by_movie[r.movie_id].append(r)

    return reviews_by_movie

# Devuelve un diccionario de ID de usuario a nombre de usuario
def get_all_users_by_id(srp: Sirope) -> dict[str, str]:
    users = list(srp.filter(User, lambda u: True))  # Carga todos los usuarios
    return {u.id: u.username for u in users}  # Crea un diccionario {id: nombre de usuario}
