import datetime  # Módulo para trabajar con fechas y horas
import uuid      # Módulo para generar identificadores únicos (UUIDs)

class Watchlist:
    def __init__(self, user_id, name, description, movie_ids=None, created_at=None, list_id=None):
        """
        Constructor de la clase Watchlist.

        Parámetros:
        - user_id: ID del usuario que creó la lista.
        - name: Nombre de la lista (por ejemplo, "Favoritas", "Pendientes").
        - description: Descripción opcional de la lista.
        - movie_ids: (opcional) Lista de IDs de películas asociadas a esta lista.
        - created_at: (opcional) Fecha de creación de la lista. Se pone la fecha actual si no se da.
        - list_id: (opcional) ID único de la lista. Se genera uno nuevo si no se proporciona.
        """

        self.user_id = user_id                      # Guarda el ID del usuario dueño de esta lista
        self.name = name                            # Guarda el nombre de la lista
        self.description = description              # Guarda la descripción de la lista
        self.movie_ids = movie_ids or []            # Guarda una lista de IDs de películas; si no hay, inicia vacía
        self.created_at = created_at or datetime.datetime.now()  # Fecha de creación, por defecto la actual
        self.id = list_id or str(uuid.uuid4())      # Genera un ID único si no se proporciona
