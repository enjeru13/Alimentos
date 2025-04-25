import tkinter as tk
from login_screen import crear_login_screen
from register_screen import crear_register_screen
from main_screen import crear_main_screen
from perfil_screen import crear_perfil_screen # Importa la nueva función

# --- Variable global para el usuario actual ---
usuario_actual_global = None

# --- Funciones para cambiar de pantalla ---
def mostrar_pantalla(parent, pantalla):
    for widget in parent.winfo_children():
        widget.pack_forget()
    pantalla.pack(expand=True, fill="both")

def mostrar_pantalla_centrada(parent, pantalla):
    for widget in parent.winfo_children():
        widget.pack_forget()
    pantalla.pack(expand=True, fill="both")

def mostrar_registro_pantalla():
    mostrar_pantalla_centrada(ventana, register_screen)

def mostrar_login_pantalla():
    mostrar_pantalla_centrada(ventana, login_screen)

def mostrar_main_pantalla(usuario):
    global usuario_actual_global
    usuario_actual_global = usuario
    main_screen = crear_main_screen(ventana, usuario, mostrar_perfil_pantalla)
    mostrar_pantalla(ventana, main_screen) # La pantalla principal ocupa todo el espacio

def mostrar_admin_pantalla():
    admin_screen = tk.Frame(ventana, bg="#E0F7FA", bd=1, relief="solid")
    admin_screen.pack(expand=True, fill="both")
    tk.Label(admin_screen, text="Panel de Administrador", font=("Segoe UI", 16, "bold")).pack(pady=20)
    mostrar_pantalla(ventana, admin_screen)

def mostrar_perfil_pantalla():
    perfil_screen = crear_perfil_screen(ventana, lambda: mostrar_main_pantalla(usuario_actual_global))
    mostrar_pantalla(ventana, perfil_screen)

# --- Interfaz gráfica principal ---
ventana = tk.Tk()
ventana.title("Sistema de Usuarios")
ventana.geometry("900x700")
ventana.configure(bg="#f3f4f6")

# --- Crear las pantallas ---
login_screen = crear_login_screen(ventana, mostrar_registro_pantalla, mostrar_main_pantalla, mostrar_admin_pantalla)
register_screen = crear_register_screen(ventana, mostrar_login_pantalla)

# --- Mostrar la pantalla inicial (centrada) ---
mostrar_pantalla_centrada(ventana, login_screen)

ventana.mainloop()