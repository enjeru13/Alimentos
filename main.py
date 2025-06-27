import json
import os
import customtkinter as ctk
from tkinter import messagebox

from controllers.usuarios_controller import obtener_usuario
from screens.login_screen import crear_login_screen
from screens.register_screen import crear_register_screen
from screens.perfil_screen import crear_perfil_screen
from screens.main_screen import MainScreen

CONFIG_PATH = "config.json"


def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            return json.load(open(CONFIG_PATH, "r"))
        except:
            pass
    return {"appearance": "System", "color_theme": "blue"}


def save_config(cfg):
    json.dump(cfg, open(CONFIG_PATH, "w"), indent=2)


cfg = load_config()
ctk.set_appearance_mode(cfg.get("appearance", "System"))
ctk.set_default_color_theme(cfg.get("color_theme", "blue"))

usuario_actual = None
rol_actual = None


def mostrar_pantalla(parent, frame):
    for w in parent.winfo_children():
        w.pack_forget()
    frame.pack(expand=True, fill="both")


def mostrar_login():
    mostrar_pantalla(root, login_screen)


def mostrar_registro():
    mostrar_pantalla(root, register_screen)


def mostrar_principal(usuario, rol):
    global usuario_actual, rol_actual
    usuario_actual = usuario
    rol_actual = rol
    principal = MainScreen(root, usuario_actual, rol_actual, mostrar_perfil)
    mostrar_pantalla(root, principal)


def mostrar_perfil():
    user = obtener_usuario(usuario_actual)
    if not user:
        messagebox.showerror("Error", "No se pudieron obtener los datos del usuario.")
        return
    perfil = crear_perfil_screen(
        root, user, lambda: mostrar_principal(user.nombre_usuario, user.rol)
    )
    mostrar_pantalla(root, perfil)


root = ctk.CTk()
root.title("Sistema de Usuarios")
root.geometry("900x700")

login_screen = crear_login_screen(root, mostrar_registro, mostrar_principal)
register_screen = crear_register_screen(root, mostrar_login)

mostrar_login()
root.mainloop()
