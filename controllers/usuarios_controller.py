from typing import Optional
from datetime import datetime

from models.usuario import Usuario
from utils.auth import verificar_credenciales, hash_password
from utils.db_utils import (
    usuario_existe as _db_usuario_existe,
    obtener_datos_usuario as _db_obtener_datos,
    insertar_usuario,
)


def login_usuario(nombre_usuario: str, contraseña: str) -> Optional[Usuario]:
    """
    Verifica credenciales y, si son válidas, devuelve un Usuario.
    En caso contrario retorna None.
    """
    ok, rol = verificar_credenciales(nombre_usuario, contraseña)
    if not ok:
        return None

    data = _db_obtener_datos(nombre_usuario)
    if not data:
        return None

    # Parseamos fecha si viene como string
    fecha = data["fecha_registro"]
    if isinstance(fecha, str):
        fecha = datetime.fromisoformat(fecha)

    return Usuario(
        id_usuario=data["id_usuario"],
        nombres=data["nombres"],
        apellidos=data["apellidos"],
        nombre_usuario=data["nombre_usuario"],
        email=data["email"],
        cedula=data["cedula"],
        año_seccion=data["año_seccion"],
        fecha_registro=fecha,
        rol=data["rol"],
    )


def crear_usuario(u: Usuario, contraseña: str):
    """
    Crea un nuevo usuario en la BD:
      1) Verifica duplicados
      2) Hashea la contraseña
      3) Inserta el registro
    Lanza Exception si ya existe.
    """
    if _db_usuario_existe(u.nombre_usuario, u.email, u.cedula):
        raise Exception("El usuario, el email o la cédula ya están registrados.")

    hashed = hash_password(contraseña)

    # Normalizar fecha a string
    fecha = u.fecha_registro
    if isinstance(fecha, datetime):
        fecha = fecha.strftime("%Y-%m-%d %H:%M:%S")

    insertar_usuario(
        u.nombres,
        u.apellidos,
        u.nombre_usuario,
        u.email,
        hashed,
        u.cedula,
        u.año_seccion,
        fecha,
        u.rol,
    )


def existe_usuario(nombre_usuario: str, email: str, cedula: str) -> bool:
    """
    Wrapper para comprobar duplicados desde las vistas.
    """
    return _db_usuario_existe(nombre_usuario, email, cedula)


def obtener_usuario(nombre_usuario: str) -> Optional[Usuario]:
    """
    Carga un Usuario completo por nombre o email.
    Retorna None si no existe.
    """
    data = _db_obtener_datos(nombre_usuario)
    if not data:
        return None

    fecha = data["fecha_registro"]
    if isinstance(fecha, str):
        fecha = datetime.fromisoformat(fecha)

    return Usuario(
        id_usuario=data["id_usuario"],
        nombres=data["nombres"],
        apellidos=data["apellidos"],
        nombre_usuario=data["nombre_usuario"],
        email=data["email"],
        cedula=data["cedula"],
        año_seccion=data["año_seccion"],
        fecha_registro=fecha,
        rol=data["rol"],
    )
