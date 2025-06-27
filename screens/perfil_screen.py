import customtkinter as ctk
from PIL import Image, ImageDraw
from models.usuario import Usuario


def crear_perfil_screen(parent, usuario: Usuario, volver_callback):
    perfil_frame = ctk.CTkFrame(parent)
    perfil_frame.pack(expand=True, fill="both", padx=20, pady=20)

    bg_color = ("#FFFFFF", "#2C3E50")
    cont_color = ("#F7F7F7", "#34495E")

    bg = ctk.CTkFrame(perfil_frame, corner_radius=15, fg_color=bg_color)
    bg.pack(expand=True, fill="both", padx=40, pady=20)

    ctk.CTkLabel(
        bg, text="Perfil del Usuario", font=("Segoe UI", 24, "bold"), justify="center"
    ).pack(pady=(20, 10))

    avatar_img = Image.new("RGBA", (100, 100), (200, 200, 200, 255))
    draw = ImageDraw.Draw(avatar_img)
    draw.ellipse((0, 0, 100, 100), fill=(150, 150, 150, 255))
    avatar_ctk = ctk.CTkImage(
        light_image=avatar_img, dark_image=avatar_img, size=(100, 100)
    )
    ctk.CTkLabel(bg, image=avatar_ctk, text="").pack(pady=(0, 20))

    cont = ctk.CTkFrame(bg, corner_radius=10, fg_color=cont_color)
    cont.pack(padx=40, pady=(0, 20), fill="x")
    cont.grid_columnconfigure(0, weight=1)
    cont.grid_columnconfigure(1, weight=1)

    fila = 0

    def nueva_seccion(titulo: str):
        nonlocal fila
        ctk.CTkLabel(
            cont, text=titulo, font=("Segoe UI", 18, "bold"), justify="center"
        ).grid(row=fila, column=0, columnspan=2, sticky="ew", pady=(15, 5))
        fila += 1

    def nuevo_campo(etq: str, val: str):
        nonlocal fila
        ctk.CTkLabel(
            cont, text=etq, font=("Segoe UI", 14, "bold"), justify="center"
        ).grid(row=fila, column=0, sticky="ew", padx=5, pady=2)
        ctk.CTkLabel(cont, text=val, font=("Segoe UI", 14), justify="center").grid(
            row=fila, column=1, sticky="ew", padx=5, pady=2
        )
        fila += 1

    nueva_seccion("Datos Personales")
    nuevo_campo("Nombre Completo:", f"{usuario.nombres} {usuario.apellidos}")
    nuevo_campo("Cédula:", usuario.cedula)

    nueva_seccion("Cuenta")
    nuevo_campo("Usuario:", usuario.nombre_usuario)
    nuevo_campo("Email:", usuario.email)
    nuevo_campo("Registrado:", usuario.fecha_registro)

    nueva_seccion("Académica")
    nuevo_campo("Año y Sección:", usuario.año_seccion)
    nuevo_campo("Rol:", usuario.rol)

    ctk.CTkButton(
        bg, text="Volver al Menú", width=180, corner_radius=8, command=volver_callback
    ).pack(pady=(10, 20))

    return perfil_frame
