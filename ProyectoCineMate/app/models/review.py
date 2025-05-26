import datetime  # Importa el módulo para trabajar con fechas y horas
import uuid      # Importa el módulo para generar identificadores únicos (UUIDs)

class Review:
    def __init__(self, user_id, movie_id, rating, comment, created_at=None, review_id=None):
        """
        Constructor de la clase Review.

        Parámetros:
        - user_id: ID del usuario que escribe la reseña.
        - movie_id: ID de la película a la que pertenece la reseña.
        - rating: Puntuación dada por el usuario (por ejemplo, entre 1 y 5).
        - comment: Comentario del usuario sobre la película.
        - created_at: (opcional) Fecha y hora de creación de la reseña. Si no se proporciona, se toma la fecha actual.
        - review_id: (opcional) ID único de la reseña. Si no se proporciona, se genera uno nuevo automáticamente.
        """

        self.user_id = user_id                                # Guarda el ID del usuario que escribió la reseña
        self.movie_id = movie_id                              # Guarda el ID de la película reseñada
        self.rating = rating                                  # Guarda la puntuación (valor numérico)
        self.comment = comment                                # Guarda el texto del comentario del usuario
        self.created_at = created_at or datetime.datetime.now()  # Usa la fecha actual si no se proporciona
        self.id = review_id or str(uuid.uuid4())              # Genera un ID único si no se proporciona uno
