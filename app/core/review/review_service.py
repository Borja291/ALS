from app.models.movie import Movie  # Importa el modelo de películas
from app.models.review import Review  # Importa el modelo de reseñas
from flask_login import current_user  # Obtiene el usuario autenticado actualmente
from sirope import Sirope  # Librería de persistencia

# Busca una película por ID que pertenezca al usuario actual
def find_user_movie_by_id(srp: Sirope, movie_id: str) -> Movie | None:
    return next(
        srp.filter(Movie, lambda m: m.id == movie_id and m.user_id == current_user.id),
        None
    )
    # Devuelve la película si se encuentra y pertenece al usuario, si no devuelve None

# Busca la reseña de una película por parte del usuario actual, considerando el ID original si es una copia
def find_review_by_movie_and_user(srp: Sirope, movie_id: str) -> Review | None:
    movie_ref_id = movie_id  # Por defecto se usa el ID recibido

    movie = srp.find_first(Movie, lambda m: m.id == movie_id)  # Busca la película por ID
    if movie and hasattr(movie, "original_movie_id"):
        # Si existe y tiene ID de película original, lo usamos para buscar la reseña
        movie_ref_id = movie.original_movie_id

    # Busca la primera reseña para ese movie_ref_id hecha por el usuario actual
    return srp.find_first(
        Review,
        lambda r: r.movie_id == movie_ref_id and r.user_id == current_user.id
    )

# Crea y guarda una nueva reseña para una película
def save_new_review(srp: Sirope, movie_id: str, rating: int, comment: str) -> Review:
    review = Review(
        user_id=current_user.id,  # Asocia la reseña al usuario actual
        movie_id=movie_id,
        rating=rating,
        comment=comment
    )
    srp.save(review)  # Guarda la reseña en la base de datos
    return review  # Devuelve la reseña creada

# Actualiza una reseña existente con nuevos datos y la guarda
def update_existing_review(srp: Sirope, review: Review, rating: int, comment: str):
    review.rating = rating  # Actualiza la puntuación
    review.comment = comment  # Actualiza el comentario
    srp.save(review)  # Guarda los cambios
