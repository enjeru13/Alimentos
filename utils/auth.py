import bcrypt
from typing import Tuple, Optional
from utils.db_utils import obtener_hash_contraseña


def hash_password(password: str) -> str:
    """
    Genera un hash bcrypt para la contraseña dada.
    Devuelve el hash como cadena UTF-8.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verificar_credenciales(usuario: str, contraseña: str) -> Tuple[bool, Optional[str]]:
    """
    Comprueba que el usuario (nombre o email) exista y
    que la contraseña coincida con su hash en la BD.

    Retorna (True, rol) o (False, None).
    """
    fila = obtener_hash_contraseña(usuario)
    if not fila:
        return False, None

    hash_bd = fila["hash_contraseña"].encode("utf-8")
    rol = fila["rol"]

    if bcrypt.checkpw(contraseña.encode("utf-8"), hash_bd):
        return True, rol

    return False, None
