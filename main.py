import tkinter as tk
from login_screen import crear_login_screen
from register_screen import crear_register_screen
from main_screen import crear_main_screen

# --- Funciones para cambiar de pantalla ---
def mostrar_pantalla(contenedor, pantalla):
    for widget in contenedor.winfo_children():
        widget.pack_forget()
    pantalla.pack(expand=True, fill="both")

def mostrar_registro_pantalla():
    mostrar_pantalla(contenedor, register_screen)

def mostrar_login_pantalla():
    mostrar_pantalla(contenedor, login_screen)

def mostrar_main_pantalla(usuario):
    main_screen = crear_main_screen(contenedor, usuario, mostrar_perfil_pantalla)
    mostrar_pantalla(contenedor, main_screen)

def mostrar_admin_pantalla():
    admin_screen = tk.Frame(contenedor, bg="#E0F7FA", bd=1, relief="solid", width=500, height=500)
    admin_screen.pack_propagate(False)
    tk.Label(admin_screen, text="Panel de Administrador", font=("Segoe UI", 16, "bold")).pack(pady=20)
    mostrar_pantalla(contenedor, admin_screen)

def mostrar_perfil_pantalla():
    perfil_screen = tk.Frame(contenedor, bg="#FFFFE0", bd=1, relief="solid", width=400, height=400)
    perfil_screen.pack_propagate(False)
    tk.Label(perfil_screen, text="Perfil del Usuario", font=("Segoe UI", 16, "bold")).pack(pady=20)
    mostrar_pantalla(contenedor, perfil_screen)

# --- Interfaz gráfica principal ---
ventana = tk.Tk()
ventana.title("Sistema de Usuarios")
ventana.geometry("900x700")
ventana.configure(bg="#f3f4f6")

contenedor = tk.Frame(ventana, bg="#f3f4f6")
contenedor.pack(expand=True, padx=20, pady=20)

# --- Crear las pantallas ---
login_screen = crear_login_screen(contenedor, mostrar_registro_pantalla, mostrar_main_pantalla, mostrar_admin_pantalla)
register_screen = crear_register_screen(contenedor, mostrar_login_pantalla)

# --- Mostrar la pantalla inicial ---
mostrar_pantalla(contenedor, login_screen)

ventana.mainloop()