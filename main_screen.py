import tkinter as tk
from tkinter import ttk, scrolledtext
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de la conexión a la base de datos.
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', 'Angeleduardo13')
DB_NAME = os.getenv('DB_NAME', 'AlimentosDB')

def buscar_alimento_db(termino_busqueda):
    """
    Esta función se conecta a la base de datos y devuelve los registros de la tabla 'alimentos'
    cuyo nombre se parezca al término de búsqueda.
    """
    try:
        cnx = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM alimentos WHERE nom_producto LIKE %s"
        search = f"%{termino_busqueda}%"
        cursor.execute(query, (search,))
        resultados = cursor.fetchall()
        cursor.close()
        cnx.close()
        return resultados
    except mysql.connector.Error as err:
        print(f"Error de Base de Datos: {err}")
        return []

def obtener_detalles_alimento_db(id_producto):
    """
    Consulta los detalles completos de un alimento a partir de su id_producto.
    """
    try:
        cnx = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
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

def crear_main_screen(ventana, usuario_actual, mostrar_perfil_cb):
    pantalla_principal = tk.Frame(ventana, bg="#f0f0f0")
    pantalla_principal.pack(expand=True, fill="both")

    # --- Barra Lateral Izquierda (Módulos) ---
    barra_lateral = tk.Frame(pantalla_principal, bg="#d0d0d0", width=150)
    barra_lateral.pack(side="left", fill="y")
    barra_lateral.pack_propagate(False)

    etiqueta_menu = tk.Label(barra_lateral, text="Menú", font=("Segoe UI", 12, "bold"), bg="#d0d0d0", pady=10)
    etiqueta_menu.pack(pady=(15, 10))

    boton_inicio = tk.Button(barra_lateral, text="Inicio", bg="#e0e0e0", font=("Segoe UI", 10),
                              relief="flat", padx=15, pady=8, width=12)
    boton_inicio.pack(pady=2)
    boton_alimentos = tk.Button(barra_lateral, text="Alimentos", bg="#e0e0e0", font=("Segoe UI", 10),
                                relief="flat", padx=15, pady=8, width=12)
    boton_alimentos.pack(pady=2)
    boton_recetas = tk.Button(barra_lateral, text="Categorias", bg="#e0e0e0", font=("Segoe UI", 10),
                              relief="flat", padx=15, pady=8, width=12)
    boton_recetas.pack(pady=2)
    boton_perfil = tk.Button(barra_lateral, text="Ver Perfil", command=mostrar_perfil_cb,
                             bg="#64B5F6", fg="white", font=("Segoe UI", 10),
                             relief="flat", padx=15, pady=8, width=12)
    boton_perfil.pack(pady=5)

    # --- Área Principal (Barra de Búsqueda y Contenido) ---
    area_principal = tk.Frame(pantalla_principal, bg="#f9f9f9")
    area_principal.pack(expand=True, fill="both", padx=10, pady=10)

    # Barra de Búsqueda
    barra_busqueda_frame = tk.Frame(area_principal, bg="#e0e0e0", pady=10)
    barra_busqueda_frame.pack(fill="x")
    etiqueta_buscar = tk.Label(barra_busqueda_frame, text="Buscar Alimento:", font=("Segoe UI", 10), bg="#e0e0e0")
    etiqueta_buscar.pack(side="left", padx=10)
    entry_busqueda = ttk.Entry(barra_busqueda_frame, font=("Segoe UI", 10), width=40)
    entry_busqueda.pack(side="left", padx=5, fill="x", expand=True)

    # Listbox para resultados y ScrolledText para detalles
    resultados_lista = tk.Listbox(area_principal, font=("Segoe UI", 10), width=60)
    resultados_lista.pack(pady=10, padx=10, fill="both", expand=True)

    detalles_texto = scrolledtext.ScrolledText(area_principal, font=("Segoe UI", 10), width=80, height=15)
    detalles_texto.pack(pady=10, padx=10, fill="x")
    detalles_texto.config(state=tk.DISABLED)

    def buscar_alimento():
        termino = entry_busqueda.get()
        resultados = buscar_alimento_db(termino)
        resultados_lista.delete(0, tk.END)
        if resultados:
            for alimento in resultados:
                nom = alimento.get('nom_producto', 'Sin nombre')
                categoria = alimento.get('categoria', '')
                id_producto = alimento.get('id_producto', 'N/A')
                texto_mostrar = f"{nom} ({categoria}) - ID: {id_producto}"
                resultados_lista.insert(tk.END, texto_mostrar)
        else:
            resultados_lista.insert(tk.END, "No se encontraron resultados.")
        detalles_texto.config(state=tk.DISABLED)

    def mostrar_detalles_seleccionado(event):
        seleccion = resultados_lista.curselection()
        if seleccion:
            indice = seleccion[0]
            item = resultados_lista.get(indice)
            # Extraer el id_producto del texto (asumimos que está al final luego de " - ID: ")
            try:
                id_str = item.split(" - ID: ")[-1]
                id_producto = int(id_str)
                detalles = obtener_detalles_alimento_db(id_producto)
                if detalles:
                    detalles_texto.config(state=tk.NORMAL)
                    detalles_texto.delete(1.0, tk.END)
                    detalles_texto.insert(tk.END, f"Nombre: {detalles.get('nom_producto')}\n")
                    detalles_texto.insert(tk.END, f"Categoría: {detalles.get('categoria')}\n")
                    detalles_texto.insert(tk.END, f"Calorías: {detalles.get('calorias')}\n")
                    detalles_texto.insert(tk.END, f"Proteína: {detalles.get('proteina')} g\n")
                    detalles_texto.insert(tk.END, f"Grasas: {detalles.get('grasas')} g\n")
                    detalles_texto.insert(tk.END, f"Carbohidratos: {detalles.get('carbohidratos')} g\n")
                    detalles_texto.insert(tk.END, f"Descripción: {detalles.get('descripcion')}\n")
                    detalles_texto.config(state=tk.DISABLED)
                else:
                    detalles_texto.config(state=tk.NORMAL)
                    detalles_texto.delete(1.0, tk.END)
                    detalles_texto.insert(tk.END, "No se pudieron obtener los detalles para este alimento.")
                    detalles_texto.config(state=tk.DISABLED)
            except ValueError:
                detalles_texto.config(state=tk.NORMAL)
                detalles_texto.delete(1.0, tk.END)
                detalles_texto.insert(tk.END, "Error al extraer el ID del alimento.")
                detalles_texto.config(state=tk.DISABLED)

    boton_buscar = tk.Button(barra_busqueda_frame, text="Buscar", command=buscar_alimento,
                               bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"),
                               relief="flat", padx=10)
    boton_buscar.pack(side="left", padx=10)

    resultados_lista.bind('<<ListboxSelect>>', mostrar_detalles_seleccionado)

    return pantalla_principal