import hashlib        # Módulo para aplicar funciones hash (seguras) como SHA-256
import uuid           # Módulo para generar identificadores únicos (UUIDs)
from flask_login import UserMixin  # Clase base que proporciona funcionalidades para gestionar usuarios con Flask-Login

class User(UserMixin):
    def __init__(self, username, password, email, user_id=None):
        """
        Constructor de la clase User.

        Parámetros:
        - username: nombre de usuario.
        - password: contraseña del usuario (en texto plano, será cifrada).
        - email: dirección de correo electrónico del usuario.
        - user_id: (opcional) ID único del usuario. Si no se proporciona, se genera uno automáticamente.
        """

        self.id = user_id or str(uuid.uuid4())   # Asigna un ID único si no se da uno (string UUID)
        self.username = username                 # Guarda el nombre de usuario
        self.password = self._hash_password(password)  # Guarda la contraseña en forma cifrada
        self.email = email                       # Guarda el correo electrónico

    def get_id(self):
        """
        Método requerido por Flask-Login. Retorna el ID del usuario.
        Se usa para identificar al usuario de forma única en la sesión.
        """
        return self.id

    def check_password(self, password):
        """
        Verifica si la contraseña ingresada coincide con la contraseña cifrada.
        
        Parámetro:
        - password: contraseña en texto plano introducida por el usuario.
        
        Retorna:
        - True si coincide, False si no.
        """
        return self.password == self._hash_password(password)

    def _hash_password(self, password):
        """
        Cifra la contraseña usando SHA-256.
        
        Parámetro:
        - password: contraseña en texto plano.
        
        Retorna:
        - Contraseña cifrada como una cadena hexadecimal.
        """
        return hashlib.sha256(password.encode()).hexdigest()
