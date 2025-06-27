import os
import re
from datetime import datetime
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image

from controllers.usuarios_controller import crear_usuario
from models.usuario import Usuario


def crear_register_screen(parent, mostrar_login):
    pantalla = ctk.CTkFrame(parent)
    pantalla.pack(expand=True, fill="both")
    pantalla.bind_class("CTkButton", "<Return>", lambda e: e.widget.invoke())

    # Fondo de imagen (opcional)
    try:
        img = Image.open(os.path.join("media", "background1.jpg"))
        fondo = ctk.CTkImage(light_image=img, dark_image=img, size=(900, 700))
        lbl = ctk.CTkLabel(pantalla, image=fondo, text="", fg_color="transparent")
        lbl.place(relx=0, rely=0, relwidth=1, relheight=1)

        def redim(e):
            nueva = ctk.CTkImage(
                light_image=img, dark_image=img, size=(e.width, e.height)
            )
            lbl.configure(image=nueva)
            lbl.image = nueva

        pantalla.bind("<Configure>", redim)
    except FileNotFoundError:
        pass

    # Contenedor central transparente
    cont = ctk.CTkFrame(pantalla, corner_radius=15, fg_color="transparent")
    cont.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(cont, text="Registro de Usuario", font=("Segoe UI", 22, "bold")).pack(
        pady=(15, 10)
    )

    # ── Campos en dos columnas: etiqueta arriba, input abajo ────────
    e_nombres, e_apellidos = _crear_fila(cont, "Nombres:", "Apellidos:")
    e_cedula, e_email = _crear_fila(cont, "Cédula:", "Email:")
    e_usuario, e_ano_sec = _crear_fila(cont, "Usuario:", "Año y Sección:")
    e_pass, e_confirm = _crear_fila(cont, "Contraseña:", "Confirmar:", show="*")

    # Mostrar/ocultar contraseñas
    var = ctk.BooleanVar(value=False)
    ctk.CTkCheckBox(
        cont,
        text="Mostrar contraseñas",
        variable=var,
        command=lambda: _toggle_password([e_pass, e_confirm], var),
    ).pack(pady=(5, 15))

    # ── Función de registro ────────────────────────────────────────
    def registrar():
        d = dict(
            nombres=e_nombres.get().strip(),
            apellidos=e_apellidos.get().strip(),
            cedula=e_cedula.get().strip(),
            email=e_email.get().strip(),
            usuario=e_usuario.get().strip(),
            ano_sec=e_ano_sec.get().strip(),
            pwd=e_pass.get(),
            confirm=e_confirm.get().strip(),
        )
        if not all(d.values()):
            return messagebox.showerror("Error", "Todos los campos son obligatorios.")
        if d["pwd"] != d["confirm"]:
            return messagebox.showerror("Error", "Las contraseñas no coinciden.")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", d["email"]):
            return messagebox.showerror("Error", "Email no válido.")
        if len(d["pwd"]) < 8:
            return messagebox.showerror(
                "Error", "La contraseña debe tener ≥8 caracteres."
            )
        if not d["cedula"].isdigit() or not 7 <= len(d["cedula"]) <= 11:
            return messagebox.showerror("Error", "Cédula inválida.")

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        u = Usuario(
            id_usuario=0,
            nombres=d["nombres"],
            apellidos=d["apellidos"],
            nombre_usuario=d["usuario"],
            email=d["email"],
            cedula=d["cedula"],
            año_seccion=d["ano_sec"],
            fecha_registro=fecha,
            rol="usuario",
        )
        try:
            crear_usuario(u, d["pwd"])
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            mostrar_login()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    # ── Botones ────────────────────────────────────────────────────
    ctk.CTkButton(cont, text="Registrar", width=200, command=registrar).pack(
        pady=(0, 10)
    )
    ctk.CTkButton(cont, text="Ir a Login", width=200, command=mostrar_login).pack(
        pady=(0, 15)
    )

    return pantalla


def _crear_fila(parent, lbl1, lbl2, show=""):
    """
    Crea dos controles (label+entry) en dos columnas:
    - lbl1 sobre entry1 en columnas 0-1
    - lbl2 sobre entry2 en columnas 2-3
    """
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="x", padx=20, pady=5)

    # 4 columnas iguales
    for col in range(4):
        frame.grid_columnconfigure(col, weight=1, uniform="a")

    # Widgets
    l1 = ctk.CTkLabel(frame, text=lbl1, font=("Segoe UI", 12, "bold"))
    e1 = ctk.CTkEntry(frame, show=show)
    l2 = ctk.CTkLabel(frame, text=lbl2, font=("Segoe UI", 12, "bold"))
    e2 = ctk.CTkEntry(frame, show=show)

    # Posicionamiento: labels en fila 0, entries en fila 1
    l1.grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=(0, 2))
    e1.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=(0, 5))
    l2.grid(row=0, column=2, columnspan=2, sticky="w", padx=5, pady=(0, 2))
    e2.grid(row=1, column=2, columnspan=2, sticky="ew", padx=5, pady=(0, 5))

    return e1, e2


def _toggle_password(entries, var):
    ch = "" if var.get() else "*"
    for e in entries:
        e.configure(show=ch)
