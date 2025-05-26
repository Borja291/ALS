import datetime  # Importa el módulo para trabajar con fechas
import uuid      # Importa el módulo para generar identificadores únicos (UUID)

class Movie:
    def __init__(self, user_id, title, year, genre, date_watched, movie_id=None, original_user_id=None, original_movie_id=None):
        """
        Constructor de la clase Movie.
        
        Parámetros:
        - user_id: ID del usuario que añadió la película.
        - title: Título de la película.
        - year: Año de estreno de la película.
        - genre: Género de la película.
        - date_watched: Fecha en que el usuario vio la película.
        - movie_id: (opcional) ID único de la película. Si no se proporciona, se genera uno nuevo.
        - original_user_id: (opcional) ID del usuario original (útil si es una copia de otra película).
        - original_movie_id: (opcional) ID de la película original.
        """

        self.user_id = user_id                        # Guarda el ID del usuario actual
        self.title = title                            # Guarda el título de la película
        self.year = year                              # Guarda el año de la película
        self.genre = genre                            # Guarda el género de la película
        self.date_watched = date_watched              # Guarda la fecha en que se vio la película
        self.id = movie_id or str(uuid.uuid4())       # Asigna un ID: si no se da, se genera uno único con uuid
        self.original_user_id = original_user_id or user_id  # Si no se da el original_user_id, se asume que es el mismo usuario
        self.original_movie_id = original_movie_id or self.id  # Si no se da el original_movie_id, se asume que es esta misma película

    def update(self, title, year, genre, date_watched):
        """
        Actualiza los datos de la película con nuevos valores.
        
        Parámetros:
        - title: Nuevo título.
        - year: Nuevo año.
        - genre: Nuevo género.
        - date_watched: Nueva fecha de visualización.
        """

        self.title = title                  # Actualiza el título
        self.year = year                    # Actualiza el año
        self.genre = genre                  # Actualiza el género
        self.date_watched = date_watched    # Actualiza la fecha de visualización
