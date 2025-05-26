from app.models.user import User  # Importa la clase User desde los modelos de la aplicación
from flask_login import login_user, logout_user  # Importa funciones para gestionar sesiones de usuario con Flask-Login
from sirope import Sirope  # Importa la librería Sirope, que gestiona la persistencia de objetos

# Función para iniciar sesión con nombre de usuario y contraseña
def login_with_credentials(srp: Sirope, username: str, password: str):
    # Busca un usuario con el nombre de usuario proporcionado
    user = next(srp.filter(User, lambda u: u.username == username), None)

    # Si el usuario existe y la contraseña es correcta
    if user and user.check_password(password):
        login_user(user)  # Inicia la sesión del usuario
        return True  # Devuelve True indicando que el inicio de sesión fue exitoso

    return False  # Si no se encuentra el usuario o la contraseña es incorrecta

# Función para registrar un nuevo usuario
def register_user(srp: Sirope, username: str, password: str, email: str):
    # Verifica si ya existe un usuario con el mismo nombre de usuario
    existing = next(srp.filter(User, lambda u: u.username == username), None)

    if existing:
        return False  # No se puede registrar un usuario con nombre ya existente

    # Crea un nuevo usuario y lo guarda en la base de datos
    user = User(username, password, email)
    srp.save(user)
    return True  # Registro exitoso

# Función para actualizar el nombre de usuario de un usuario existente
def update_username(srp: Sirope, user_id: str, new_username: str):
    # Busca al usuario por su ID
    user = next(srp.filter(User, lambda u: u.id == user_id), None)

    if not user:
        return None, "Usuario no encontrado."  # Si no se encuentra, devuelve un error

    if new_username == user.username:
        return user, None  # Si el nuevo nombre es igual al actual, no hace nada

    # Comprueba si el nuevo nombre ya está en uso por otro usuario
    if next(srp.filter(User, lambda u: u.username == new_username), None):
        return None, "El nombre de usuario ya está en uso."

    # Valida que el nuevo nombre no esté vacío
    if not new_username:
        return None, "El nombre no puede estar vacío."

    # Actualiza el nombre de usuario y guarda los cambios
    user.username = new_username
    srp.save(user)

    # Cierra la sesión actual para evitar inconsistencias con el nombre de usuario antiguo
    logout_user()

    return user, None  # Devuelve el usuario actualizado y sin mensaje de error

# Función para cerrar sesión del usuario actual
def logout_current_user():
    logout_user()  # Llama a la función de Flask-Login para cerrar sesión
