import bcrypt
from typing import Tuple, Optional
from utils.db_utils import obtener_hash_contraseña


def hash_password(password: str) -> str:

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verificar_credenciales(usuario: str, contraseña: str) -> Tuple[bool, Optional[str]]:

    fila = obtener_hash_contraseña(usuario)
    if not fila:
        return False, None

    hash_bd = fila["hash_contraseña"].encode("utf-8")
    rol = fila["rol"]

    if bcrypt.checkpw(contraseña.encode("utf-8"), hash_bd):
        return True, rol

    return False, None
