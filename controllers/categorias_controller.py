from typing import List
from controllers.authz import require_admin
from models.categoria import Categoria
from utils.db_utils import (
    obtener_categorias as _fetch_all,
    insertar_categoria as _insert_db,
    actualizar_categoria as _update_db,
    eliminar_categoria as _delete_db,
)


def listar_categorias() -> List[Categoria]:
    rows = _fetch_all()
    return [Categoria(id_categoria=r["id_categoria"], nombre=r["nombre"]) for r in rows]


def crear_categoria(cat: Categoria, rol: str):
    require_admin(rol)
    _insert_db(cat.nombre)


def actualizar_categoria(cat: Categoria, rol: str):
    require_admin(rol)
    _update_db(cat.id_categoria, cat.nombre)


def borrar_categoria(id_categoria: int, rol: str):
    require_admin(rol)
    _delete_db(id_categoria)
