import customtkinter as ctk

def crear_perfil_screen(parent, nombres, apellidos, usuario, email, cedula, año_seccion_actual, fecha_registro, rol, volver_callback):
    perfil_frame = ctk.CTkFrame(parent)
    perfil_frame.pack(expand=True, fill="both", padx=20, pady=20)

    ctk.CTkLabel(perfil_frame, text="Perfil del Usuario", font=("Segoe UI", 24, "bold"), text_color="#ECF0F1").pack(pady=20)

    # 🔹 Contenedor principal con división en secciones
    contenedor_datos = ctk.CTkFrame(perfil_frame, corner_radius=15, fg_color="#2C3E50", width=600)
    contenedor_datos.pack(pady=10, padx=30, fill="both", expand=True)

    def agregar_seccion(titulo):
        """Función para agregar un título de sección"""
        seccion_label = ctk.CTkLabel(contenedor_datos, text=titulo, font=("Segoe UI", 16, "bold"), text_color="#ECF0F1", anchor="w")
        seccion_label.pack(fill="x", padx=10, pady=(10, 5))

    def agregar_info(label_text, value):
        """Función para agregar cada campo con su valor"""
        fila = ctk.CTkFrame(contenedor_datos, fg_color="transparent")
        
        label = ctk.CTkLabel(fila, text=label_text, font=("Segoe UI", 14, "bold"), text_color="#ECF0F1", width=180, anchor="w")
        dato = ctk.CTkLabel(fila, text=value, font=("Segoe UI", 12), text_color="#BDC3C7", anchor="w")
        
        label.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")
        dato.grid(row=0, column=1, padx=10, pady=(5, 0), sticky="w")

        fila.pack(fill="x", padx=10, pady=5)

    # 🔹 Sección: Datos Personales
    agregar_seccion("Datos Personales")
    agregar_info("Nombre Completo:", f"{nombres} {apellidos}")
    agregar_info("Cédula:", cedula)

    # 🔹 Sección: Detalles de Cuenta
    agregar_seccion("Detalles de Cuenta")
    agregar_info("Usuario:", usuario)
    agregar_info("Email:", email)
    agregar_info("Fecha de Registro:", fecha_registro)

    # 🔹 Sección: Información Académica
    agregar_seccion("Información Académica")
    agregar_info("Año y Sección:", año_seccion_actual)
    agregar_info("Rol:", rol)

    # 🔹 Botón de volver con estilo moderno
    boton_volver = ctk.CTkButton(perfil_frame, text="Volver", command=volver_callback, 
                                 fg_color="#2980B9", hover_color="#3498DB", width=200)
    boton_volver.pack(pady=20)

    return perfil_frame