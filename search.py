import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
import json


API_KEY = 'A8KmASCGg2Fn7igt0jpgsEQHcRdn6KfSrsAhFEcT'
BASE_URL = 'https://api.nal.usda.gov/fdc/v1/foods/search'
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

def crear_main_screen(contenedor, usuario_actual, mostrar_perfil_cb):
    pantalla_principal = tk.Frame(contenedor, bg="#f0f0f0")
    pantalla_principal.pack(expand=True, fill="both")

    # --- Barra de Búsqueda ---
    barra_busqueda_frame = tk.Frame(pantalla_principal, bg="#e0e0e0", pady=10)
    barra_busqueda_frame.pack(fill="x")

    etiqueta_buscar = tk.Label(barra_busqueda_frame, text="Buscar Alimento:", font=("Segoe UI", 10), bg="#e0e0e0")
    etiqueta_buscar.pack(side="left", padx=10)

    entry_busqueda = ttk.Entry(barra_busqueda_frame, font=("Segoe UI", 10), width=40)
    entry_busqueda.pack(side="left", padx=5, fill="x", expand=True)

    resultados_lista = tk.Listbox(pantalla_principal, font=("Segoe UI", 10), width=60)
    resultados_lista.pack(pady=10, padx=10, fill="both", expand=True)

    detalles_texto = scrolledtext.ScrolledText(pantalla_principal, font=("Segoe UI", 10), width=80, height=15)
    detalles_texto.pack(pady=10, padx=10, fill="x")
    detalles_texto.config(state=tk.DISABLED) # Hacerlo de solo lectura

    def buscar_alimento():
        termino = entry_busqueda.get()
        resultados = buscar_alimento_api(termino)
        resultados_lista.delete(0, tk.END)  # Limpiar la lista anterior
        if resultados:
            for alimento in resultados:
                nombre = alimento.get('description', 'Sin nombre')
                marca = alimento.get('brandName', '')
                fdc_id = alimento.get('fdcId')
                texto_mostrar = f"{nombre} {'(' + marca + ')' if marca else ''} - ID: {fdc_id}"
                resultados_lista.insert(tk.END, texto_mostrar)
        else:
            resultados_lista.insert(tk.END, "No se encontraron resultados.")
        detalles_texto.config(state=tk.DISABLED) # Limpiar detalles al buscar de nuevo

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
                    detalles_texto.delete(1.0, tk.END) # Limpiar texto anterior
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

    # --- Barra Lateral Izquierda (Placeholder) ---
    barra_lateral = tk.Frame(pantalla_principal, bg="#d0d0d0", width=150)
    barra_lateral.pack(side="left", fill="y")
    barra_lateral.pack_propagate(False)
    etiqueta_placeholder = tk.Label(barra_lateral, text="Barra Lateral", font=("Segoe UI", 10), bg="#d0d0d0")
    etiqueta_placeholder.pack(pady=20)

    # --- Área de Contenido Principal ---
    area_contenido = tk.Frame(pantalla_principal, bg="#f9f9f9")
    area_contenido.pack(expand=True, fill="both", padx=10, pady=10)

    etiqueta_bienvenida = tk.Label(area_contenido, text=f"Bienvenido, Invitado!", font=("Segoe UI", 14, "bold"), bg="#f9f9f9")
    etiqueta_bienvenida.pack(pady=10)
    etiqueta_instruccion = tk.Label(area_contenido, text="Utiliza la barra de búsqueda para encontrar información sobre alimentos.", font=("Segoe UI", 10), bg="#f9f9f9")
    etiqueta_instruccion.pack(pady=5)

    return pantalla_principal

if __name__ == "__main__":
    nueva_ventana = tk.Tk()
    nueva_ventana.title("Búsqueda de Alimentos")
    nueva_ventana.geometry("1000x700")  # Aumentar el tamaño para los detalles

    contenedor_principal = tk.Frame(nueva_ventana)
    contenedor_principal.pack(expand=True, fill="both", padx=10, pady=10)

    # Llamamos a crear_main_screen pasando el contenedor de la nueva ventana
    main_screen = crear_main_screen(contenedor_principal, "Invitado", None) # No necesitamos mostrar_perfil_cb por ahora

    nueva_ventana.mainloop()