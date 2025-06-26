# screens/login_screen.py

import os
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image

from controllers.usuarios_controller import login_usuario


def crear_login_screen(parent, mostrar_registro, mostrar_principal):
    """
    parent: CTk window/frame
    mostrar_registro(): callback para ir a registro
    mostrar_principal(usuario: str, rol: str): callback tras login válido
    """
    pantalla = ctk.CTkFrame(parent)
    pantalla.pack(expand=True, fill="both")

    # Fondo
    try:
        img = Image.open(os.path.join("media", "background1.jpg"))
        fondo_img = ctk.CTkImage(light_image=img, dark_image=img, size=(900, 700))
        lbl_fondo = ctk.CTkLabel(
            pantalla, image=fondo_img, text="", fg_color="transparent"
        )
        lbl_fondo.place(relx=0, rely=0, relwidth=1, relheight=1)

        def redimensionar(e):
            size = (e.width, e.height)
            lbl_fondo.configure(
                image=ctk.CTkImage(light_image=img, dark_image=img, size=size)
            )

        pantalla.bind("<Configure>", redimensionar)

    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró 'media/background1.jpg'")

    # Contenedor central
    cont = ctk.CTkFrame(pantalla, corner_radius=15, fg_color="#2C3E50")
    cont.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(
        cont,
        text="Iniciar Sesión",
        font=("Segoe UI", 22, "bold"),
        text_color="#ECF0F1",
    ).pack(pady=(15, 20))

    entry_usuario = _crear_input(cont, "Usuario:")
    entry_contra = _crear_input(cont, "Contraseña:", show="*")

    # Mostrar/ocultar contraseña
    var_chk = ctk.BooleanVar()
    ctk.CTkCheckBox(
        cont,
        text="Mostrar contraseña",
        variable=var_chk,
        command=lambda: _toggle_password([entry_contra], var_chk),
        text_color="#ECF0F1",
    ).pack(pady=10)

    def login():
        usr = entry_usuario.get().strip()
        pwd = entry_contra.get().strip()
        if not usr or not pwd:
            return messagebox.showerror("Error", "Complete ambos campos.")

        usuario_obj = login_usuario(usr, pwd)
        if not usuario_obj:
            return messagebox.showerror("Error", "Usuario o contraseña inválidos.")

        messagebox.showinfo("Bienvenido", f"¡Hola, {usuario_obj.nombre_usuario}!")
        mostrar_principal(usuario_obj.nombre_usuario, usuario_obj.rol)

    # Botones
    ctk.CTkButton(
        cont,
        text="Iniciar Sesión",
        command=login,
        fg_color="#2980B9",
        hover_color="#3498DB",
        width=180,
    ).pack(pady=15)

    ctk.CTkButton(
        cont,
        text="Registrarse",
        command=mostrar_registro,
        fg_color="#27AE60",
        hover_color="#2ECC71",
        width=180,
    ).pack(pady=(0, 10))

    return pantalla


def _toggle_password(entries, var):
    ch = "" if var.get() else "*"
    for e in entries:
        e.configure(show=ch)


def _crear_input(frame, label_text, show="", ancho=24):
    cont = ctk.CTkFrame(frame, fg_color="transparent")
    lbl = ctk.CTkLabel(
        cont, text=label_text, font=("Segoe UI", 12, "bold"), text_color="#ECF0F1"
    )
    ent = ctk.CTkEntry(cont, width=ancho * 10, show=show, border_color="#ECF0F1")
    lbl.pack(fill="x", padx=10, pady=(0, 5))
    ent.pack(fill="x", padx=10, pady=(0, 10))
    cont.pack(pady=8, fill="x")
    return ent


# Para testeo en solitario
if __name__ == "__main__":

    def mock_reg():
        print("Registrar...")

    def mock_main(u, r):
        print("Main:", u, r)

    root = ctk.CTk()
    root.geometry("900x700")
    root.title("Login Demo")
    crear_login_screen(root, mock_reg, mock_main)
    root.mainloop()
