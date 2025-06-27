# screens/perfil_screen.py

import customtkinter as ctk
from models.usuario import Usuario


def crear_perfil_screen(parent, usuario: Usuario, volver_callback):
    """
    parent:      CTk window/frame
    usuario:     instancia de models.Usuario
    volver_callback(): función para volver al menú principal
    """
    perfil_frame = ctk.CTkFrame(parent)
    perfil_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Título
    ctk.CTkLabel(
        perfil_frame,
        text="Perfil del Usuario",
        font=("Segoe UI", 24, "bold"),
    ).pack(pady=20)

    contenedor = ctk.CTkFrame(
        perfil_frame, corner_radius=15, fg_color="#2C3E50", width=600
    )
    contenedor.pack(pady=10, padx=30, fill="both", expand=True)

    def agregar_seccion(titulo: str):
        ctk.CTkLabel(
            contenedor,
            text=titulo,
            font=("Segoe UI", 16, "bold"),
            anchor="w",
        ).pack(fill="x", padx=10, pady=(10, 5))

    def agregar_info(etiqueta: str, valor: str):
        fila = ctk.CTkFrame(contenedor, fg_color="transparent")
        lbl = ctk.CTkLabel(
            fila,
            text=etiqueta,
            font=("Segoe UI", 14, "bold"),
            width=180,
            anchor="w",
        )
        txt = ctk.CTkLabel(
            fila,
            text=valor,
            font=("Segoe UI", 12),
            anchor="w",
        )
        lbl.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")
        txt.grid(row=0, column=1, padx=10, pady=(5, 0), sticky="w")
        fila.pack(fill="x", padx=10, pady=5)

    # Sección: Datos Personales
    agregar_seccion("Datos Personales")
    agregar_info("Nombre Completo:", f"{usuario.nombres} {usuario.apellidos}")
    agregar_info("Cédula:", usuario.cedula)

    # Sección: Detalles de Cuenta
    agregar_seccion("Detalles de Cuenta")
    agregar_info("Usuario:", usuario.nombre_usuario)
    agregar_info("Email:", usuario.email)
    agregar_info("Fecha de Registro:", usuario.fecha_registro)

    # Sección: Información Académica
    agregar_seccion("Información Académica")
    agregar_info("Año y Sección:", usuario.año_seccion)
    agregar_info("Rol:", usuario.rol)

    # Botón Volver
    ctk.CTkButton(
        perfil_frame,
        text="Volver al Menú",
        command=volver_callback,
        fg_color="#27AE60",
        hover_color="#2ECC71",
        width=200,
    ).pack(pady=20)

    return perfil_frame
