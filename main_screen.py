import customtkinter as ctk
import mysql.connector
import os
from dotenv import load_dotenv
from alimentos_screen import crear_alimentos_screen
from db_utils import obtener_detalles_alimento_db  # ✅ Importación corregida

load_dotenv()

# Configuración de CustomTkinter
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")  

# Configuración de la conexión a la base de datos
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', 'Angeleduardo13')
DB_NAME = os.getenv('DB_NAME', 'AlimentosDB')

def buscar_alimento_db(termino_busqueda):
    try:
        cnx = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM alimentos WHERE nom_producto LIKE %s"
        cursor.execute(query, (f"%{termino_busqueda}%",))
        resultados = cursor.fetchall()
        cursor.close()
        cnx.close()
        return resultados
    except mysql.connector.Error as err:
        print(f"Error de Base de Datos: {err}")
        return []

def obtener_detalles_alimento_db(id_producto):
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

def mostrar_pantalla(ventana, pantalla):
    """Cambia la pantalla activa ocultando la anterior."""
    for widget in ventana.winfo_children():
        widget.pack_forget()
    pantalla.pack(expand=True, fill="both")

def crear_main_screen(ventana, usuario_actual, mostrar_perfil_cb):
    pantalla_principal = ctk.CTkFrame(ventana)
    pantalla_principal.pack(expand=True, fill="both")

    # 🔹 Menú lateral más ancho
    barra_lateral = ctk.CTkFrame(pantalla_principal, width=200, corner_radius=10)
    barra_lateral.pack(side="left", fill="y")
    barra_lateral.pack_propagate(False)

    # 🔹 Bienvenida dentro del menú lateral
    bienvenida_label = ctk.CTkLabel(barra_lateral, text=f"Bienvenido, {usuario_actual}", 
                                    font=("Segoe UI", 16, "bold"), text_color="#ECF0F1", anchor="center")
    bienvenida_label.pack(pady=(15, 10))

    # 🔹 Botones del menú con navegación
    ctk.CTkButton(barra_lateral, text="Inicio", width=200).pack(pady=5)
    ctk.CTkButton(barra_lateral, text="Alimentos", width=200, 
                  command=lambda: mostrar_pantalla(ventana, crear_alimentos_screen(ventana, lambda: crear_main_screen(ventana, usuario_actual, mostrar_perfil_cb)))).pack(pady=5)
    ctk.CTkButton(barra_lateral, text="Categorías", width=200).pack(pady=5)
    ctk.CTkButton(barra_lateral, text="Ver Perfil", width=200, command=mostrar_perfil_cb).pack(pady=10)

    # --- Área Principal (Mantiene la barra de búsqueda) ---
    area_principal = ctk.CTkFrame(pantalla_principal)
    area_principal.pack(expand=True, fill="both", padx=10, pady=10)

    barra_busqueda_frame = ctk.CTkFrame(area_principal)
    barra_busqueda_frame.pack(fill="x")

    ctk.CTkLabel(barra_busqueda_frame, text="Buscar Alimento:", font=("Segoe UI", 12)).pack(side="left", padx=10)
    entry_busqueda = ctk.CTkEntry(barra_busqueda_frame, font=("Segoe UI", 12), width=300)
    entry_busqueda.pack(side="left", padx=5, fill="x", expand=True)
    ctk.CTkButton(barra_busqueda_frame, text="Buscar", command=lambda: buscar_alimento()).pack(side="left", padx=10)

    # --- Lista de resultados con `CTkScrollableFrame` ---
    resultados_frame = ctk.CTkScrollableFrame(area_principal, width=400, height=200)
    resultados_frame.pack(pady=10, padx=10, fill="both", expand=True)

    detalles_texto = ctk.CTkTextbox(area_principal, font=("Segoe UI", 12), width=400, height=150)
    detalles_texto.pack(pady=10, padx=10, fill="x")
    detalles_texto.configure(state="disabled")

    def buscar_alimento():
        for widget in resultados_frame.winfo_children():
            widget.destroy()
        
        termino = entry_busqueda.get()
        resultados = buscar_alimento_db(termino)
        
        if resultados:
            for alimento in resultados:
                nom = alimento.get('nom_producto', 'Sin nombre')
                categoria = alimento.get('categoria', '')
                id_producto = alimento.get('id_producto', 'N/A')

                # Cada resultado será un botón que muestra los detalles al hacer clic
                boton_resultado = ctk.CTkButton(resultados_frame, 
                                                text=f"{nom} ({categoria})", 
                                                command=lambda id=id_producto: mostrar_detalles_seleccionado(id), 
                                                font=("Segoe UI", 12), 
                                                fg_color="#3498DB", 
                                                hover_color="#2980B9")
                boton_resultado.pack(fill="x", padx=5, pady=2)
        else:
            ctk.CTkLabel(resultados_frame, text="No se encontraron resultados.", font=("Segoe UI", 12)).pack(pady=5)

        detalles_texto.configure(state="disabled")

    def mostrar_detalles_seleccionado(id_producto):
        detalles = obtener_detalles_alimento_db(id_producto)
        detalles_texto.configure(state="normal")
        detalles_texto.delete("1.0", "end")
        
        if detalles:
            detalles_texto.insert("end", f"Nombre: {detalles.get('nom_producto')}\n")
            detalles_texto.insert("end", f"Categoría: {detalles.get('categoria')}\n")
            detalles_texto.insert("end", f"Calorías: {detalles.get('calorias')}\n")
            detalles_texto.insert("end", f"Proteína: {detalles.get('proteina')} g\n")
            detalles_texto.insert("end", f"Grasas: {detalles.get('grasas')} g\n")
            detalles_texto.insert("end", f"Carbohidratos: {detalles.get('carbohidratos')} g\n")
            detalles_texto.insert("end", f"Descripción: {detalles.get('descripcion')}\n")
        else:
            detalles_texto.insert("end", "No se pudieron obtener los detalles.\n")

        detalles_texto.configure(state="disabled")

    return pantalla_principal