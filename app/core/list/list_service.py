from app.models.watchlist import Watchlist  # Importa el modelo Watchlist
from app.models.movie import Movie  # Importa el modelo Movie
from flask_login import current_user  # Importa al usuario actualmente logueado
from sirope import Sirope  # Importa Sirope, el sistema de persistencia de objetos

# Crea una nueva watchlist para el usuario actual, usando los datos del formulario y las películas seleccionadas
def create_watchlist(srp: Sirope, form, selected_ids: list[str]) -> Watchlist:
    watchlist = Watchlist(
        user_id=current_user.id,  # Asocia la lista al usuario actual
        name=form.name.data,  # Toma el nombre desde el formulario
        description=form.description.data,  # Toma la descripción desde el formulario
        movie_ids=selected_ids  # Lista de IDs de películas seleccionadas
    )
    srp.save(watchlist)  # Guarda la nueva lista en la base de datos
    return watchlist  # Devuelve la lista creada

# Obtiene todas las listas de un usuario por su ID
def get_user_watchlists(srp: Sirope, user_id: str) -> list[Watchlist]:
    return list(srp.filter(Watchlist, lambda wl: wl.user_id == user_id))  # Filtra las listas por el ID del usuario

# Obtiene una lista específica por su ID y verifica que pertenezca al usuario
def get_watchlist_by_id(srp: Sirope, user_id: str, list_id: str) -> Watchlist | None:
    return next(srp.filter(Watchlist, lambda wl: wl.id == list_id and wl.user_id == user_id), None)
    # Busca una lista con ese ID y que sea del usuario; devuelve None si no la encuentra

# Devuelve todas las películas de un usuario por su ID
def get_user_movies(srp: Sirope, user_id: str) -> list[Movie]:
    return list(srp.filter(Movie, lambda m: m.user_id == user_id))  # Filtra películas por usuario

# Actualiza las películas asociadas a una watchlist y guarda los cambios
def update_watchlist_movies(srp: Sirope, watchlist: Watchlist, selected_ids: list[str]):
    watchlist.movie_ids = selected_ids  # Actualiza la lista de películas con los nuevos IDs
    srp.save(watchlist)  # Guarda los cambios en la base de datos

# Devuelve las películas de un usuario que están en una lista de IDs específica
def get_movies_in_watchlist(srp: Sirope, user_id: str, movie_ids: list[str]) -> list[Movie]:
    # Filtra películas del usuario y devuelve solo las que están en la lista de IDs proporcionada
    return [m for m in srp.filter(Movie, lambda m: m.user_id == user_id) if m.id in movie_ids]

# Elimina una watchlist solo si pertenece al usuario que la solicita
def delete_watchlist_if_owned(srp: Sirope, user_id: str, list_id: str) -> bool:
    for oid in srp.load_all_keys(Watchlist):  # Recorre todas las claves (IDs internos de Sirope)
        watchlist = srp.load(oid)  # Carga cada watchlist por su clave
        if watchlist.id == list_id and watchlist.user_id == user_id:  # Comprueba que el ID y el dueño coincidan
            srp.delete(oid)  # Elimina la lista
            return True  # Indica que se ha eliminado correctamente
    return False  # Si no se encuentra la lista o no es del usuario, no se elimina
