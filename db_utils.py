# db_utils.py (Nuevo archivo)
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', 'Angeleduardo13')
DB_NAME = os.getenv('DB_NAME', 'AlimentosDB')

def obtener_detalles_alimento_db(id_producto):
    """Recupera los detalles de un alimento por su ID."""
    try:
        cnx = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM alimentos WHERE id_producto = %s"
        cursor.execute(query, (id_producto,))
        resultado = cursor.fetchone()
        cursor.close()
        cnx.close()
        return resultado
    except mysql.connector.Error as err:
        print(f"Error al obtener detalle: {err}")
        return None