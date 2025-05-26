def register_blueprints(app):
    # Esta función se encarga de importar y registrar todos los blueprints
    # que definen las rutas de cada módulo de la aplicación Flask.

    # Importa los Blueprints desde sus respectivos módulos de vistas
    from app.views.auth.routes import auth_routes         # Rutas de autenticación (login, registro, logout)
    from app.views.main.routes import main_routes         # Ruta principal (inicio)
    from app.views.movie.routes import movie_routes       # Rutas para gestión de películas
    from app.views.list.routes import list_routes         # Rutas para listas temáticas (watchlists)
    from app.views.review.routes import review_routes     # Rutas para reseñas de películas
    from app.views.explore.routes import explore_routes   # Rutas para explorar/importar películas

    # Registra cada Blueprint en la aplicación Flask principal
    app.register_blueprint(auth_routes)
    app.register_blueprint(main_routes)
    app.register_blueprint(movie_routes)
    app.register_blueprint(list_routes)
    app.register_blueprint(review_routes)
    app.register_blueprint(explore_routes)
