from typing import List, Optional
from models.categoria import Categoria
from utils.db_utils import (
    obtener_categorias as _fetch_all,
    insertar_categoria as _insert_db,
    actualizar_categoria as _update_db,
    eliminar_categoria as _delete_db,
)


def listar_categorias() -> List[Categoria]:
    """
    Devuelve la lista de todas las categorías.
    """
    rows = _fetch_all()
    return [Categoria(id_categoria=r["id_categoria"], nombre=r["nombre"]) for r in rows]


def obtener_categoria(id_categoria: int) -> Optional[Categoria]:
    """
    Recupera una categoría por su ID.
    Devuelve un model Categoria o None si no existe.
    """
    for r in _fetch_all():
        if r["id_categoria"] == id_categoria:
            return Categoria(id_categoria=r["id_categoria"], nombre=r["nombre"])
    return None


def crear_categoria(cat: Categoria) -> None:
    """
    Inserta una nueva categoría en la base de datos.
    """
    _insert_db(cat.nombre)


def actualizar_categoria(cat: Categoria) -> None:
    """
    Actualiza el nombre de una categoría existente.
    """
    _update_db(cat.id_categoria, cat.nombre)


def borrar_categoria(id_categoria: int) -> None:
    """
    Elimina una categoría por su ID.
    """
    _delete_db(id_categoria)
