from dataclasses import dataclass
from datetime import datetime


@dataclass
class Usuario:
    id_usuario: int
    nombres: str
    apellidos: str
    nombre_usuario: str
    email: str
    cedula: str
    año_seccion: str
    fecha_registro: datetime
    rol: str
