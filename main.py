# main.py

import customtkinter as ctk
from tkinter import messagebox

from screens.login_screen import crear_login_screen
from screens.register_screen import crear_register_screen
from screens.main_screen import crear_main_screen
from screens.perfil_screen import crear_perfil_screen

# Importamos el controller que carga un Usuario completo
from controllers.usuarios_controller import obtener_usuario

# ── Configuración global CTk ──────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── Variables globales ────────────────────────────────────────────────────
usuario_actual_global = None
rol_actual_global = None


def mostrar_pantalla(parent, pantalla):
    """Oculta todos los widgets de parent y muestra solo pantalla."""
    for w in parent.winfo_children():
        w.pack_forget()
    pantalla.pack(expand=True, fill="both")


def mostrar_login_pantalla():
    mostrar_pantalla(ventana, login_screen)


def mostrar_registro_pantalla():
    mostrar_pantalla(ventana, register_screen)


def mostrar_principal(usuario, rol):
    """Guarda usuario/rol y muestra la pantalla principal."""
    global usuario_actual_global, rol_actual_global
    usuario_actual_global = usuario
    rol_actual_global = rol

    main = crear_main_screen(
        ventana, usuario_actual_global, rol_actual_global, mostrar_perfil_pantalla
    )
    mostrar_pantalla(ventana, main)


def mostrar_perfil_pantalla():
    """
    Obtiene un objeto Usuario desde el controller y construye la pantalla de perfil.
    """
    user = obtener_usuario(usuario_actual_global)
    if not user:
        messagebox.showerror("Error", "No se pudieron obtener los datos del usuario.")
        return

    perfil = crear_perfil_screen(
        ventana, user, lambda: mostrar_principal(user.nombre_usuario, user.rol)
    )
    mostrar_pantalla(ventana, perfil)


# ── Inicialización de la ventana ─────────────────────────────────────────
ventana = ctk.CTk()
ventana.title("Sistema de Usuarios")
ventana.geometry("900x700")

# ── Instancia de pantallas de login y registro ───────────────────────────
login_screen = crear_login_screen(ventana, mostrar_registro_pantalla, mostrar_principal)
register_screen = crear_register_screen(ventana, mostrar_login_pantalla)

# Arranca en login
mostrar_login_pantalla()

ventana.mainloop()
