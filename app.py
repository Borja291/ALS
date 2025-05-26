# Importa la función create_app que configura y devuelve la instancia de Flask ya preparada
from app import create_app

# Crea la aplicación utilizando la fábrica definida en app.py
app = create_app()

# Este bloque asegura que el servidor solo se ejecute si se lanza directamente este archivo
if __name__ == '__main__':
    # Ejecuta el servidor de desarrollo de Flask con modo debug activado
    # Esto permite ver errores detallados y recarga automática al guardar cambios
    app.run(debug=True)
