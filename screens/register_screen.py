# screens/register_screen.py

import os
import re
from datetime import datetime
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image

# 1) Importamos solo del controlador, ya no de utils/db_utils ni utils/auth
from controllers.usuarios_controller import crear_usuario
from models.usuario import Usuario


def crear_register_screen(parent, mostrar_login):
    pantalla = ctk.CTkFrame(parent)
    pantalla.pack(expand=True, fill="both")

    # Fondo (idéntico), solo cuidado con el path
    try:
        img = Image.open(os.path.join("media", "background1.jpg"))
        fondo = ctk.CTkImage(light_image=img, dark_image=img, size=(900, 700))
        lbl = ctk.CTkLabel(pantalla, image=fondo, text="", fg_color="transparent")
        lbl.place(relx=0, rely=0, relwidth=1, relheight=1)

        def redim(e):
            lbl.configure(
                image=ctk.CTkImage(
                    light_image=img, dark_image=img, size=(e.width, e.height)
                )
            )

        pantalla.bind("<Configure>", redim)

    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró 'media/background1.jpg'")

    # Contenedor de campos
    cont = ctk.CTkFrame(pantalla, corner_radius=15, fg_color="#2C3E50", width=650)
    cont.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(
        cont,
        text="Registro de Usuario",
        font=("Segoe UI", 22, "bold"),
        text_color="#ECF0F1",
    ).pack(pady=(15, 20))

    # Entradas de formulario
    e_nombres, e_apellidos = _crear_fila(cont, "Nombres:", "Apellidos:")
    e_cedula, e_email = _crear_fila(cont, "Cédula:", "Email:")
    e_usuario, e_ano_sec = _crear_fila(cont, "Usuario:", "Año y Sección:")
    e_pass, e_confirm = _crear_fila(cont, "Contraseña:", "Confirmar:", show="*")

    # Toggle visibilidad password (igual que login)
    var = ctk.BooleanVar()
    ctk.CTkCheckBox(
        cont,
        text="Mostrar contraseñas",
        variable=var,
        command=lambda: _toggle_password([e_pass, e_confirm], var),
        text_color="#ECF0F1",
    ).pack(pady=10)

    def registrar():
        # 2) Validaciones estrictas de formulario (sin tocar BD aquí)
        nombres = e_nombres.get().strip()
        apellidos = e_apellidos.get().strip()
        usuario = e_usuario.get().strip()
        email = e_email.get().strip()
        año_sec = e_ano_sec.get().strip()
        password = e_pass.get()
        confirm = e_confirm.get()
        cedula = e_cedula.get().strip()

        if not all(
            [nombres, apellidos, usuario, email, año_sec, password, confirm, cedula]
        ):
            return messagebox.showerror("Error", "Todos los campos son obligatorios.")
        if password != confirm:
            return messagebox.showerror("Error", "Las contraseñas no coinciden.")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return messagebox.showerror("Error", "Email no válido.")
        if len(password) < 8:
            return messagebox.showerror(
                "Error", "La contraseña debe tener al menos 8 caracteres."
            )
        if not cedula.isdigit() or not 7 <= len(cedula) <= 11:
            return messagebox.showerror("Error", "Cédula inválida.")

        # 3) Creamos el dataclass Usuario, sin id ni password
        fecha_reg = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        u = Usuario(
            id_usuario=0,
            nombres=nombres,
            apellidos=apellidos,
            nombre_usuario=usuario,
            email=email,
            cedula=cedula,
            año_seccion=año_sec,
            fecha_registro=fecha_reg,
            rol="usuario",
        )

        # 4) Llamamos a crear_usuario del controller, que verifica duplicados, hashea y guarda
        try:
            crear_usuario(u, password)
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            mostrar_login()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    # Botones de acción
    ctk.CTkButton(
        cont,
        text="Registrar",
        command=registrar,
        fg_color="#2980B9",
        hover_color="#3498DB",
        width=200,
    ).pack(pady=15)

    ctk.CTkButton(
        cont,
        text="Ir a Login",
        command=mostrar_login,
        fg_color="#27AE60",
        hover_color="#2ECC71",
        width=200,
    ).pack(pady=5)

    return pantalla


def _crear_fila(parent, lbl1, lbl2, show=""):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    l1 = ctk.CTkLabel(
        frame, text=lbl1, font=("Segoe UI", 12, "bold"), text_color="#ECF0F1", width=120
    )
    e1 = ctk.CTkEntry(frame, width=220, show=show)
    l2 = ctk.CTkLabel(
        frame, text=lbl2, font=("Segoe UI", 12, "bold"), text_color="#ECF0F1", width=120
    )
    e2 = ctk.CTkEntry(frame, width=220, show=show)
    l1.grid(row=0, column=0, padx=4, pady=5, sticky="w")
    e1.grid(row=0, column=1, padx=4, pady=5)
    l2.grid(row=0, column=2, padx=4, pady=5, sticky="w")
    e2.grid(row=0, column=3, padx=4, pady=5)
    frame.pack(pady=12, padx=10, fill="x")
    return e1, e2


def _toggle_password(entries, var):
    ch = "" if var.get() else "*"
    for e in entries:
        e.configure(show=ch)
