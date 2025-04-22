import tkinter as tk
from tkinter import ttk

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

    boton_buscar = tk.Button(barra_busqueda_frame, text="Buscar", command=lambda: buscar_alimento(entry_busqueda.get()),
                                 bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=10)
    boton_buscar.pack(side="left", padx=10)

    # --- Barra Lateral Izquierda ---
    barra_lateral = tk.Frame(pantalla_principal, bg="#d0d0d0", width=150)
    barra_lateral.pack(side="left", fill="y")
    barra_lateral.pack_propagate(False) # Evitar que el tamaño cambie con el contenido

    etiqueta_perfil = tk.Label(barra_lateral, text="Perfil", font=("Segoe UI", 12, "bold"), bg="#d0d0d0", pady=10)
    etiqueta_perfil.pack(pady=(15, 5))

    boton_perfil = tk.Button(barra_lateral, text="Ver Perfil", command=mostrar_perfil_cb,
                                 bg="#64B5F6", fg="white", font=("Segoe UI", 10), relief="flat", padx=15, pady=8, width=12)
    boton_perfil.pack(pady=5)

    # --- Área de Contenido Principal ---
    area_contenido = tk.Frame(pantalla_principal, bg="#f9f9f9")
    area_contenido.pack(expand=True, fill="both", padx=10, pady=10)

    etiqueta_bienvenida = tk.Label(area_contenido, text=f"Bienvenido, {usuario_actual}!", font=("Segoe UI", 14, "bold"), bg="#f9f9f9")
    etiqueta_bienvenida.pack(pady=10)
    etiqueta_instruccion = tk.Label(area_contenido, text="Utiliza la barra de búsqueda para encontrar información sobre alimentos.", font=("Segoe UI", 10), bg="#f9f9f9")
    etiqueta_instruccion.pack(pady=5)

    def buscar_alimento(termino_busqueda):
        print(f"Buscando alimento: {termino_busqueda}")

    return pantalla_principal