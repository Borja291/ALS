# Importaciones necesarias
import uuid
from flask import Flask
from flask_login import LoginManager  # Manejo de sesiones de usuario
import sirope  # Persistencia de datos simple y ligera

# Importaciones internas del proyecto
from app.models.user import User  # Modelo de usuario (asegúrate de que esté en app/models/user.py)
from app.views import register_blueprints  # Función para registrar todos los blueprints del proyecto

# Se inicializa el gestor de sesiones de Flask-Login
login_manager = LoginManager()

# Se declara la instancia de Sirope como variable global
sirope_inst = None


# 🔧 Función principal que crea y configura la aplicación Flask
def create_app():
    # Crea la instancia de Flask; instance_relative_config permite sobreescribir config desde una carpeta externa
    app = Flask(__name__, instance_relative_config=True)

    # Clave secreta para sesiones y protección CSRF
    app.config['SECRET_KEY'] = 'una_clave_supersecreta'

    # Inicializa la instancia global de Sirope (base de datos)
    global sirope_inst
    sirope_inst = sirope.Sirope()

    # 🔐 Configura el login manager con la aplicación Flask
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Define la ruta a redirigir si el usuario no está autenticado

    # 🔌 Registra todos los blueprints (rutas agrupadas por módulo)
    register_blueprints(app)

    return app  # Devuelve la instancia de la app configurada


# 🔄 Función requerida por Flask-Login para recuperar el usuario actual desde Sirope
@login_manager.user_loader
def load_user(user_id):
    srp = get_sirope()  # Obtiene la instancia global de Sirope
    # Busca el usuario con el ID especificado y lo devuelve; si no lo encuentra, devuelve None
    return next(srp.filter(User, lambda u: u.id == user_id), None)


# 📦 Función global para obtener la instancia de Sirope desde cualquier parte de la app
def get_sirope():
    return sirope_inst
