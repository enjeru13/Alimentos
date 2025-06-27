import os
import mysql.connector
from dotenv import load_dotenv
import bcrypt

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "AlimentosDB")


def conectar():
    return mysql.connector.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )


def usuario_existe(
    nombre_usuario: str, email: str, cedula: str, exclude_id: int | None = None
) -> bool:

    cnx = conectar()
    cur = cnx.cursor()
    try:
        sql = """
            SELECT 1
              FROM usuarios
             WHERE (nombre_usuario = %s OR email = %s OR cedula = %s)
        """
        params = [nombre_usuario, email, cedula]

        if exclude_id is not None:
            sql += " AND id != %s"
            params.append(exclude_id)

        cur.execute(sql, tuple(params))
        return cur.fetchone() is not None
    finally:
        cur.close()
        cnx.close()


def obtener_hash_contraseña(nombre_usuario: str) -> dict | None:

    cnx = conectar()
    cur = cnx.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT contraseña AS hash_contraseña, rol "
            "FROM usuarios "
            "WHERE nombre_usuario = %s OR email = %s",
            (nombre_usuario, nombre_usuario),
        )
        return cur.fetchone()
    finally:
        cur.close()
        cnx.close()


def obtener_datos_usuario(nombre_usuario: str) -> dict | None:

    cnx = conectar()
    cur = cnx.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT
              id           AS id_usuario,
              nombres, apellidos,
              nombre_usuario,
              email, cedula,
              año_seccion,
              fecha_registro,
              rol,
              pregunta_seguridad,
              respuesta_seguridad
            FROM usuarios
            WHERE nombre_usuario = %s OR email = %s
            """,
            (nombre_usuario, nombre_usuario),
        )
        return cur.fetchone()
    finally:
        cur.close()
        cnx.close()


def insertar_usuario(
    nombres: str,
    apellidos: str,
    nombre_usuario: str,
    email: str,
    contraseña_hashed: str,
    cedula: str,
    año_seccion: str,
    fecha_registro: str,
    rol: str,
):
    cnx = conectar()
    cur = cnx.cursor()
    try:
        cur.execute(
            """
            INSERT INTO usuarios
              (nombres, apellidos, nombre_usuario, email,
               contraseña, cedula, año_seccion, fecha_registro, rol)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                nombres,
                apellidos,
                nombre_usuario,
                email,
                contraseña_hashed,
                cedula,
                año_seccion,
                fecha_registro,
                rol,
            ),
        )
        cnx.commit()
    finally:
        cur.close()
        cnx.close()


def actualizar_usuario(
    id_usuario: int,
    nombres: str,
    apellidos: str,
    nombre_usuario: str,
    contraseña_hashed: str,
) -> None:

    cnx = conectar()
    cur = cnx.cursor()
    try:
        cur.execute(
            """
            UPDATE usuarios
               SET nombres        = %s,
                   apellidos      = %s,
                   nombre_usuario = %s,
                   contraseña     = %s
             WHERE id = %s
            """,
            (
                nombres,
                apellidos,
                nombre_usuario,
                contraseña_hashed,
                id_usuario,
            ),
        )
        cnx.commit()
    finally:
        cur.close()
        cnx.close()


def guardar_pregunta_respuesta(
    id_usuario: int, pregunta: str, respuesta_plana: str
) -> None:

    cnx = conectar()
    cur = cnx.cursor()
    try:
        hash_resp = bcrypt.hashpw(respuesta_plana.encode(), bcrypt.gensalt())
        cur.execute(
            """
            UPDATE usuarios
               SET pregunta_seguridad  = %s,
                   respuesta_seguridad = %s
             WHERE id = %s
            """,
            (pregunta, hash_resp.decode(), id_usuario),
        )
        cnx.commit()
    finally:
        cur.close()
        cnx.close()


def obtener_pregunta(id_o_nombre: int | str) -> dict | None:

    cnx = conectar()
    cur = cnx.cursor(dictionary=True)
    try:
        if isinstance(id_o_nombre, int):
            cur.execute(
                "SELECT id AS id_usuario, pregunta_seguridad FROM usuarios WHERE id = %s",
                (id_o_nombre,),
            )
        else:
            cur.execute(
                """
                SELECT id AS id_usuario, pregunta_seguridad
                  FROM usuarios
                 WHERE nombre_usuario = %s OR email = %s
                """,
                (id_o_nombre, id_o_nombre),
            )
        return cur.fetchone()
    finally:
        cur.close()
        cnx.close()


def verificar_respuesta(id_usuario: int, respuesta_plana: str) -> bool:

    cnx = conectar()
    cur = cnx.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT respuesta_seguridad FROM usuarios WHERE id = %s", (id_usuario,)
        )
        row = cur.fetchone()
        if not row or not row["respuesta_seguridad"]:
            return False
        return bcrypt.checkpw(
            respuesta_plana.encode(), row["respuesta_seguridad"].encode()
        )
    finally:
        cur.close()
        cnx.close()


def actualizar_contraseña(id_usuario: int, contraseña_hashed: str) -> None:

    cnx = conectar()
    cur = cnx.cursor()
    try:
        cur.execute(
            "UPDATE usuarios SET contraseña = %s WHERE id = %s",
            (contraseña_hashed, id_usuario),
        )
        cnx.commit()
    finally:
        cur.close()
        cnx.close()

        # Alimentos -----------------------------------


def obtener_todos_los_alimentos() -> list[dict]:
    cnx = conectar()
    cur = cnx.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT
              a.id_producto,
              a.nom_producto,
              c.nombre AS categoria
            FROM alimentos a
            LEFT JOIN categorias c
              ON a.id_categoria = c.id_categoria
            ORDER BY a.nom_producto
            """
        )
        return cur.fetchall()
    finally:
        cur.close()
        cnx.close()


def buscar_alimento_db(termino: str) -> list[dict]:

    patron = f"%{termino.lower()}%"
    cnx = conectar()
    cur = cnx.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT
              a.id_producto,
              a.nom_producto,
              c.nombre AS categoria
            FROM alimentos a
            LEFT JOIN categorias c
              ON a.id_categoria = c.id_categoria
            WHERE LOWER(a.nom_producto) LIKE %s
            ORDER BY a.nom_producto
            """,
            (patron,),
        )
        return cur.fetchall()
    finally:
        cur.close()
        cnx.close()


def obtener_detalles_alimento_db(id_producto: int) -> dict | None:
    cnx = conectar()
    cur = cnx.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT
              a.id_producto, a.nom_producto,
              a.calorias, a.proteina, a.grasas, a.carbohidratos,
              a.descripcion, a.imagen_url, a.fecha_registro,
              c.nombre AS categoria
            FROM alimentos a
            LEFT JOIN categorias c
              ON a.id_categoria = c.id_categoria
            WHERE a.id_producto = %s
            """,
            (id_producto,),
        )
        return cur.fetchone()
    finally:
        cur.close()
        cnx.close()


def obtener_alimentos_por_categoria(id_categoria: int) -> list[dict]:
    cnx = conectar()
    cur = cnx.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT
              id_producto, nom_producto,
              calorias, proteina, grasas, carbohidratos
            FROM alimentos
            WHERE id_categoria = %s
            ORDER BY nom_producto
            """,
            (id_categoria,),
        )
        return cur.fetchall()
    finally:
        cur.close()
        cnx.close()


def insertar_alimento(
    nom_producto: str,
    id_categoria: int | None,
    calorias: float | None = None,
    proteina: float | None = None,
    grasas: float | None = None,
    carbohidratos: float | None = None,
    descripcion: str | None = None,
    imagen_url: str | None = None,
):
    cnx = conectar()
    cur = cnx.cursor()
    try:
        cur.execute(
            """
            INSERT INTO alimentos
              (nom_producto, id_categoria, calorias, proteina,
               grasas, carbohidratos, descripcion, imagen_url)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                nom_producto,
                id_categoria,
                calorias,
                proteina,
                grasas,
                carbohidratos,
                descripcion,
                imagen_url,
            ),
        )
        cnx.commit()
    finally:
        cur.close()
        cnx.close()


def actualizar_alimento(
    id_producto: int,
    nom_producto: str,
    id_categoria: int | None,
    calorias: float | None = None,
    proteina: float | None = None,
    grasas: float | None = None,
    carbohidratos: float | None = None,
    descripcion: str | None = None,
    imagen_url: str | None = None,
):
    cnx = conectar()
    cur = cnx.cursor()
    try:
        cur.execute(
            """
            UPDATE alimentos SET
              nom_producto  = %s,
              id_categoria  = %s,
              calorias      = %s,
              proteina      = %s,
              grasas        = %s,
              carbohidratos = %s,
              descripcion   = %s,
              imagen_url    = %s
            WHERE id_producto = %s
            """,
            (
                nom_producto,
                id_categoria,
                calorias,
                proteina,
                grasas,
                carbohidratos,
                descripcion,
                imagen_url,
                id_producto,
            ),
        )
        cnx.commit()
    finally:
        cur.close()
        cnx.close()


def eliminar_alimento(id_producto: int):
    cnx = conectar()
    cur = cnx.cursor()
    try:
        cur.execute("DELETE FROM alimentos WHERE id_producto = %s", (id_producto,))
        cnx.commit()
    finally:
        cur.close()
        cnx.close()

        # Categoria -----------------------------------


def obtener_categorias() -> list[dict]:
    cnx = conectar()
    cur = cnx.cursor(dictionary=True)
    try:
        cur.execute("SELECT id_categoria, nombre FROM categorias ORDER BY nombre")
        return cur.fetchall()
    finally:
        cur.close()
        cnx.close()


def insertar_categoria(nombre: str):
    cnx = conectar()
    cur = cnx.cursor()
    try:
        cur.execute("INSERT INTO categorias(nombre) VALUES (%s)", (nombre,))
        cnx.commit()
    finally:
        cur.close()
        cnx.close()


def actualizar_categoria(id_categoria: int, nombre_nuevo: str):
    cnx = conectar()
    cur = cnx.cursor()
    try:
        cur.execute(
            "UPDATE categorias SET nombre = %s WHERE id_categoria = %s",
            (nombre_nuevo, id_categoria),
        )
        cnx.commit()
    finally:
        cur.close()
        cnx.close()


def eliminar_categoria(id_categoria: int):
    cnx = conectar()
    cur = cnx.cursor()
    try:
        cur.execute("DELETE FROM categorias WHERE id_categoria = %s", (id_categoria,))
        cnx.commit()
    finally:
        cur.close()
        cnx.close()
