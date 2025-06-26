from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Alimento:
    id_producto: int
    nom_producto: str
    id_categoria: Optional[int] = None
    categoria: Optional[str] = None
    calorias: float = 0.0
    proteina: float = 0.0
    grasas: float = 0.0
    carbohidratos: float = 0.0
    descripcion: Optional[str] = ""
    imagen_url: Optional[str] = None
    fecha_registro: Optional[datetime] = None
