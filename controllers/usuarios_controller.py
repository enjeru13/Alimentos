from typing import Optional
from datetime import datetime

from models.usuario import Usuario
from utils.auth import verificar_credenciales, hash_password
from utils.db_utils import (
    usuario_existe as _db_usuario_existe,
    obtener_datos_usuario as _db_obtener_datos,
    insertar_usuario,
    actualizar_usuario as _db_actualizar_usuario,
    guardar_pregunta_respuesta,
    obtener_pregunta,
    verificar_respuesta,
    actualizar_contraseña,
)


def login_usuario(nombre_usuario: str, contraseña: str) -> Optional[Usuario]:
    ok, rol = verificar_credenciales(nombre_usuario, contraseña)
    if not ok:
        return None

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
        contraseña=data.get("contraseña"),
        pregunta_seguridad=data.get("pregunta_seguridad"),
        respuesta_seguridad=data.get("respuesta_seguridad"),
    )


def crear_usuario(u: Usuario, contraseña: str):
    if _db_usuario_existe(u.nombre_usuario, u.email, u.cedula):
        raise Exception("El usuario, el email o la cédula ya están registrados.")

    hashed = hash_password(contraseña)
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
    return _db_usuario_existe(nombre_usuario, email, cedula)


def obtener_usuario(nombre_usuario: str) -> Optional[Usuario]:
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
        contraseña=data.get("contraseña"),
        pregunta_seguridad=data.get("pregunta_seguridad"),
        respuesta_seguridad=data.get("respuesta_seguridad"),
    )


def actualizar_usuario(usuario: Usuario) -> None:
    if _db_usuario_existe(
        usuario.nombre_usuario,
        usuario.email,
        usuario.cedula,
        exclude_id=usuario.id_usuario,
    ):
        raise Exception(
            "El nombre de usuario, email o cédula ya están en uso por otro usuario."
        )

    _db_actualizar_usuario(
        usuario.id_usuario,
        usuario.nombres,
        usuario.apellidos,
        usuario.nombre_usuario,
        usuario.contraseña,
    )


def set_pregunta_seguridad(
    usuario: Usuario, pregunta: str, respuesta_plana: str
) -> None:

    guardar_pregunta_respuesta(usuario.id_usuario, pregunta, respuesta_plana)
    usuario.pregunta_seguridad = pregunta
    usuario.respuesta_seguridad = None


def iniciar_recuperacion(nombre_usr_o_email: str) -> Optional[str]:

    datos = obtener_pregunta(nombre_usr_o_email)
    return (
        datos["pregunta_seguridad"]
        if datos and datos.get("pregunta_seguridad")
        else None
    )


def completar_recuperacion(
    id_usuario: int, respuesta_plana: str, nueva_contraseña: str
) -> bool:

    if not verificar_respuesta(id_usuario, respuesta_plana):
        return False

    hashed = hash_password(nueva_contraseña)
    actualizar_contraseña(id_usuario, hashed)
    return True
