import tkinter as tk
from tkinter import ttk, scrolledtext
import requests # type: ignore
import json
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

API_KEY = os.getenv('API_KEY_ALIMENTOS')
BASE_URL = 'https://foodapi.calorieking.com/v1'
DETAILS_URL = 'https://api.nal.usda.gov/fdc/v1/food/{}?api_key={}'

def buscar_alimento_api(termino_busqueda):
    params = {
        'api_key': API_KEY,
        'query': termino_busqueda,
        'pageSize': 10
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if 'foods' in data:
            return data['foods']
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error al decodificar la respuesta JSON: {e}")
        return []

def obtener_detalles_alimento(fdc_id):
    url = DETAILS_URL.format(fdc_id, API_KEY)
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener detalles del alimento {fdc_id}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error al decodificar los detalles del alimento {fdc_id}: {e}")
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

    # Aquí puedes agregar más botones o elementos para tus módulos
    boton_inicio = tk.Button(barra_lateral, text="Inicio", bg="#e0e0e0", font=("Segoe UI", 10), relief="flat", padx=15, pady=8, width=12)
    boton_inicio.pack(pady=2)

    boton_alimentos = tk.Button(barra_lateral, text="Alimentos", bg="#e0e0e0", font=("Segoe UI", 10), relief="flat", padx=15, pady=8, width=12)
    boton_alimentos.pack(pady=2)

    boton_recetas = tk.Button(barra_lateral, text="Categorias", bg="#e0e0e0", font=("Segoe UI", 10), relief="flat", padx=15, pady=8, width=12)
    boton_recetas.pack(pady=2)

    boton_perfil = tk.Button(barra_lateral, text="Ver Perfil", command=mostrar_perfil_cb,
                                    bg="#64B5F6", fg="white", font=("Segoe UI", 10), relief="flat", padx=15, pady=8, width=12)
    boton_perfil.pack(pady=5)

    # --- Área Principal (Barra de Búsqueda y Contenido) ---
    area_principal = tk.Frame(pantalla_principal, bg="#f9f9f9")
    area_principal.pack(expand=True, fill="both", padx=10, pady=10)

    # Barra de Búsqueda dentro del área principal
    barra_busqueda_frame = tk.Frame(area_principal, bg="#e0e0e0", pady=10)
    barra_busqueda_frame.pack(fill="x")

    etiqueta_buscar = tk.Label(barra_busqueda_frame, text="Buscar Alimento:", font=("Segoe UI", 10), bg="#e0e0e0")
    etiqueta_buscar.pack(side="left", padx=10)

    entry_busqueda = ttk.Entry(barra_busqueda_frame, font=("Segoe UI", 10), width=40)
    entry_busqueda.pack(side="left", padx=5, fill="x", expand=True)

    resultados_lista = tk.Listbox(area_principal, font=("Segoe UI", 10), width=60)
    resultados_lista.pack(pady=10, padx=10, fill="both", expand=True)

    detalles_texto = scrolledtext.ScrolledText(area_principal, font=("Segoe UI", 10), width=80, height=15)
    detalles_texto.pack(pady=10, padx=10, fill="x")
    detalles_texto.config(state=tk.DISABLED)

    def buscar_alimento():
        termino = entry_busqueda.get()
        resultados = buscar_alimento_api(termino)
        resultados_lista.delete(0, tk.END)
        if resultados:
            for alimento in resultados:
                nombre = alimento.get('description', 'Sin nombre')
                marca = alimento.get('brandName', '')
                fdc_id = alimento.get('fdcId')
                texto_mostrar = f"{nombre} {'(' + marca + ')' if marca else ''} - ID: {fdc_id}"
                resultados_lista.insert(tk.END, texto_mostrar)
        else:
            resultados_lista.insert(tk.END, "No se encontraron resultados.")
        detalles_texto.config(state=tk.DISABLED)

    def mostrar_detalles_seleccionado(event):
        seleccion = resultados_lista.curselection()
        if seleccion:
            indice = seleccion[0]
            item = resultados_lista.get(indice)
            # Extraer el fdcId del texto del Listbox
            fdc_id_str = item.split(" - ID: ")[-1]
            try:
                fdc_id = int(fdc_id_str)
                detalles = obtener_detalles_alimento(fdc_id)
                if detalles:
                    detalles_texto.config(state=tk.NORMAL)
                    detalles_texto.delete(1.0, tk.END)
                    nombre_cientifico = detalles.get('scientificName', 'No disponible')
                    detalles_texto.insert(tk.END, f"Nombre Científico: {nombre_cientifico}\n\n")
                    detalles_texto.insert(tk.END, "Componentes Nutricionales:\n")
                    for nutriente in detalles.get('foodNutrients', []):
                        nombre_nutriente = nutriente.get('nutrientName', 'Desconocido')
                        valor = nutriente.get('value', 'N/A')
                        unidad = nutriente.get('unitName', '')
                        detalles_texto.insert(tk.END, f"- {nombre_nutriente}: {valor} {unidad}\n")
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
                                    bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=10)
    boton_buscar.pack(side="left", padx=10)

    resultados_lista.bind('<<ListboxSelect>>', mostrar_detalles_seleccionado)

    return pantalla_principal