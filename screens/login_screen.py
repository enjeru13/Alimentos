import os
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image

from controllers.usuarios_controller import login_usuario


def crear_login_screen(parent, mostrar_registro, mostrar_principal):
    pantalla = ctk.CTkFrame(parent)
    pantalla.pack(expand=True, fill="both")

    pantalla.bind_class("CTkButton", "<Return>", lambda e: e.widget.invoke())

    try:
        img = Image.open(os.path.join("media", "background1.jpg"))
        fondo_img = ctk.CTkImage(light_image=img, dark_image=img, size=(900, 700))
        lbl_fondo = ctk.CTkLabel(
            pantalla, image=fondo_img, text="", fg_color="transparent"
        )
        lbl_fondo.place(relx=0, rely=0, relwidth=1, relheight=1)

        def redimensionar(e):
            nuevo = ctk.CTkImage(
                light_image=img, dark_image=img, size=(e.width, e.height)
            )
            lbl_fondo.configure(image=nuevo)
            lbl_fondo.image = nuevo

        pantalla.bind("<Configure>", redimensionar)
    except FileNotFoundError:
        pass

    cont = ctk.CTkFrame(pantalla, corner_radius=15, fg_color="transparent")
    cont.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(cont, text="Iniciar Sesión", font=("Segoe UI", 22, "bold")).pack(
        pady=(15, 20)
    )

    entry_usuario = _crear_input(cont, "Usuario:")
    entry_contra = _crear_input(cont, "Contraseña:", show="*")

    var_chk = ctk.BooleanVar(value=False)
    ctk.CTkCheckBox(
        cont,
        text="Mostrar contraseña",
        variable=var_chk,
        command=lambda: _toggle_password([entry_contra], var_chk),
    ).pack(pady=10)

    def login():
        u = entry_usuario.get().strip()
        p = entry_contra.get().strip()
        if not u or not p:
            return messagebox.showerror("Error", "Complete ambos campos.")

        usuario_obj = login_usuario(u, p)
        if not usuario_obj:
            return messagebox.showerror("Error", "Usuario o contraseña inválidos.")

        messagebox.showinfo("Bienvenido", f"¡Hola, {usuario_obj.nombre_usuario}!")
        mostrar_principal(usuario_obj.nombre_usuario, usuario_obj.rol)

    ctk.CTkButton(cont, text="Iniciar Sesión", width=180, command=login).pack(pady=15)
    ctk.CTkButton(cont, text="Registrarse", width=180, command=mostrar_registro).pack(
        pady=(0, 10)
    )

    entry_contra.bind("<Return>", lambda e: login())
    return pantalla


def _toggle_password(entries, var):
    ch = "" if var.get() else "*"
    for e in entries:
        e.configure(show=ch)


def _crear_input(frame, label_text, show="", ancho=24):
    cont = ctk.CTkFrame(frame, fg_color="transparent")
    lbl = ctk.CTkLabel(cont, text=label_text, font=("Segoe UI", 12, "bold"))
    ent = ctk.CTkEntry(cont, width=ancho * 10, show=show)
    lbl.pack(fill="x", padx=10, pady=(0, 5))
    ent.pack(fill="x", padx=10, pady=(0, 10))
    cont.pack(pady=8, fill="x")
    return ent
