# controllers/alimentos_controller.py

from typing import List, Optional
from models.alimento import Alimento
from utils.db_utils import (
    obtener_todos_los_alimentos as _fetch_all,
    buscar_alimento_db as _search_db,
    obtener_detalles_alimento_db as _fetch_one,
    insertar_alimento as _insert_db,
    actualizar_alimento as _update_db,
    eliminar_alimento as _delete_db,
    obtener_alimentos_por_categoria as _fetch_by_cat,
    obtener_categorias as _fetch_categories,
)


def listar_alimentos() -> List[Alimento]:
    """Devuelve todos los alimentos (id, nombre, categoría)."""
    rows = _fetch_all()
    return [
        Alimento(
            id_producto=r["id_producto"],
            nom_producto=r["nom_producto"],
            categoria=r.get("categoria") or "",
        )
        for r in rows
    ]


def buscar_alimentos(termino: str) -> List[Alimento]:
    """
    Busca alimentos por nombre parcial (case-insensitive).
    Usa la función buscar_alimento_db de la capa de datos.
    """
    rows = _search_db(termino)
    return [
        Alimento(
            id_producto=r["id_producto"],
            nom_producto=r["nom_producto"],
            categoria=r.get("categoria") or "",
        )
        for r in rows
    ]


def obtener_alimento(id_producto: int) -> Optional[Alimento]:
    """Devuelve un Alimento completo o None si no existe."""
    r = _fetch_one(id_producto)
    if not r:
        return None
    return Alimento(
        id_producto=r["id_producto"],
        nom_producto=r["nom_producto"],
        categoria=r.get("categoria") or "",
        calorias=r.get("calorias", 0),
        proteina=r.get("proteina", 0),
        grasas=r.get("grasas", 0),
        carbohidratos=r.get("carbohidratos", 0),
        descripcion=r.get("descripcion", ""),
        imagen_url=r.get("imagen_url"),
        fecha_registro=r.get("fecha_registro"),
    )


def crear_alimento(al: Alimento):
    """Inserta un nuevo alimento en la BD."""
    # buscamos el id de la categoría por nombre
    cats = _fetch_categories()
    idc = next((c["id_categoria"] for c in cats if c["nombre"] == al.categoria), None)
    _insert_db(
        al.nom_producto,
        idc,
        al.calorias,
        al.proteina,
        al.grasas,
        al.carbohidratos,
        al.descripcion,
        al.imagen_url,
    )


def actualizar_alimento(al: Alimento):
    """Actualiza los datos de un alimento existente."""
    cats = _fetch_categories()
    idc = next((c["id_categoria"] for c in cats if c["nombre"] == al.categoria), None)
    _update_db(
        al.id_producto,
        al.nom_producto,
        idc,
        al.calorias,
        al.proteina,
        al.grasas,
        al.carbohidratos,
        al.descripcion,
        al.imagen_url,
    )


def borrar_alimento(id_producto: int):
    """Elimina un alimento por su ID."""
    _delete_db(id_producto)


def listar_alimentos_por_categoria(id_categoria: int) -> List[Alimento]:
    """Recupera los alimentos de una categoría dada (sólo macros básicos)."""
    rows = _fetch_by_cat(id_categoria)
    return [
        Alimento(
            id_producto=r["id_producto"],
            nom_producto=r["nom_producto"],
            categoria="",
            calorias=r.get("calorias", 0),
            proteina=r.get("proteina", 0),
            grasas=r.get("grasas", 0),
            carbohidratos=r.get("carbohidratos", 0),
            descripcion="",
            imagen_url=None,
            fecha_registro=None,
        )
        for r in rows
    ]
