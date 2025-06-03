import tkinter as tk

def crear_perfil_screen(parent, nombres, apellidos, usuario, email, cedula, fecha_registro, rol, volver_callback):
    perfil_frame = tk.Frame(parent, bg="#FFF")
    perfil_frame.pack(expand=True, fill="both")

    tk.Label(perfil_frame, text="Perfil del Usuario", font=("Segoe UI", 18, "bold"), bg="#FFF").pack(pady=20)

    # Contenedor de datos
    contenedor_datos = tk.Frame(perfil_frame, bg="#FFF", padx=20, pady=20, relief="solid", bd=3)
    contenedor_datos.pack(pady=10, padx=30, fill="both", expand=True)

    # Función para crear líneas de información con separación
    def agregar_info(label_text, value):
        fila = tk.Frame(contenedor_datos, bg="#FFFACD")
        tk.Label(fila, text=label_text, font=("Segoe UI", 13, "bold"), bg="#FFFACD", fg="#333", anchor="w").pack(side="left", padx=5)
        tk.Label(fila, text=value, font=("Segoe UI", 12), bg="#FFFACD", fg="#555").pack(side="left", padx=10)
        fila.pack(fill="x", pady=5)
        tk.Frame(contenedor_datos, height=1, bg="#DDDDDD").pack(fill="x", padx=5, pady=5)  # Línea divisoria

    # Agregar datos del usuario
    agregar_info("Nombres y apellidos:", f"{nombres} {apellidos}")
    agregar_info("Usuario:", usuario)
    agregar_info("Cedula:", cedula)
    agregar_info("Email:", email)
    agregar_info("Fecha de Registro:", fecha_registro)
    agregar_info("Rol:", rol)

    # Botón de volver
    boton_volver = tk.Button(perfil_frame, text="Volver", command=volver_callback, bg="#6C757D", fg="white",
                             font=("Segoe UI", 11, "bold"), relief="flat", padx=12, pady=6)
    boton_volver.pack(pady=15)

    return perfil_frame