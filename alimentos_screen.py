import customtkinter as ctk
import mysql.connector
import os
from dotenv import load_dotenv

from db_utils import obtener_detalles_alimento_db  # ✅ Importación corregida

load_dotenv()

# Configuración de la conexión a la base de datos
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', 'Angeleduardo13')
DB_NAME = os.getenv('DB_NAME', 'AlimentosDB')

def obtener_todos_los_alimentos():
    """Recupera todos los alimentos registrados en la base de datos."""
    try:
        cnx = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
        cursor = cnx.cursor(dictionary=True)
        
        query = "SELECT id_producto, nom_producto, categoria FROM alimentos ORDER BY nom_producto ASC"
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        cursor.close()
        cnx.close()
        
        return resultados
    except mysql.connector.Error as err:
        print(f"Error al obtener los alimentos: {err}")
        return []

def crear_alimentos_screen(parent, mostrar_main_cb):
    """Crea la pantalla de alimentos."""
    pantalla_alimentos = ctk.CTkFrame(parent)
    pantalla_alimentos.pack(expand=True, fill="both")

    ctk.CTkLabel(pantalla_alimentos, text="Lista de Alimentos", font=("Segoe UI", 22, "bold"), text_color="#ECF0F1").pack(pady=20)

    # 🔹 Contenedor de resultados con scroll
    lista_alimentos_frame = ctk.CTkScrollableFrame(pantalla_alimentos, width=600, height=400)
    lista_alimentos_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # 🔹 Obtener los alimentos de la base de datos
    alimentos = obtener_todos_los_alimentos()

    if alimentos:
        for alimento in alimentos:
            nom = alimento.get('nom_producto', 'Sin nombre')
            categoria = alimento.get('categoria', 'Sin categoría')
            id_producto = alimento.get('id_producto', 'N/A')

            # 🔹 Botón para mostrar detalles con `lambda id=id_producto`
            boton_alimento = ctk.CTkButton(lista_alimentos_frame, text=f"{nom} ({categoria})", 
                                           fg_color="#3498DB", hover_color="#2980B9", 
                                           command=lambda id=id_producto: mostrar_detalles_alimento(id),
                                           width=500)
            boton_alimento.pack(fill="x", padx=5, pady=3)
    else:
        ctk.CTkLabel(lista_alimentos_frame, text="No hay alimentos registrados.", font=("Segoe UI", 14)).pack(pady=10)

    # 🔹 Botón para volver al menú principal
    boton_volver = ctk.CTkButton(pantalla_alimentos, text="Volver al Menú",
                                 command=lambda: [pantalla_alimentos.pack_forget(), mostrar_main_cb()],
                                 fg_color="#27AE60", hover_color="#2ECC71", width=200)

    boton_volver.pack(pady=15)

    return pantalla_alimentos

def mostrar_detalles_alimento(id_producto):
    """Función para obtener y mostrar los detalles de un alimento en una ventana emergente."""
    detalles = obtener_detalles_alimento_db(id_producto)

    if detalles:
        detalles_window = ctk.CTkToplevel()
        detalles_window.title(f"Detalles de {detalles.get('nom_producto', 'Alimento')}")
        detalles_window.geometry("400x300")

        detalles_texto = f"""
        🔹 Nombre: {detalles.get('nom_producto')}
        🔹 Categoría: {detalles.get('categoria')}
        🔹 Calorías: {detalles.get('calorias')} kcal
        🔹 Proteína: {detalles.get('proteina')} g
        🔹 Grasas: {detalles.get('grasas')} g
        🔹 Carbohidratos: {detalles.get('carbohidratos')} g
        🔹 Descripción: {detalles.get('descripcion')}
        """
        
        label_detalles = ctk.CTkLabel(detalles_window, text=detalles_texto, font=("Segoe UI", 12), text_color="#ECF0F1", justify="left")
        label_detalles.pack(padx=10, pady=10)
    else:
        print("No se pudieron obtener los detalles del alimento.")