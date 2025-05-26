from app.models.movie import Movie
from sirope import Sirope

def get_user_movies(srp: Sirope, user_id: str) -> list[Movie]:
    return list(srp.filter(Movie, lambda m: m.user_id == user_id))
