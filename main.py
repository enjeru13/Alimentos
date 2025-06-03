import tkinter as tk
from tkinter import messagebox
from login_screen import crear_login_screen
from register_screen import crear_register_screen
from main_screen import crear_main_screen
from perfil_screen import crear_perfil_screen
from auth import obtener_datos_usuario

# Variable global para almacenar el usuario actual
usuario_actual_global = None

# Función para cambiar de pantalla
def mostrar_pantalla(parent, pantalla):
    for widget in parent.winfo_children():
        widget.pack_forget()
    pantalla.pack(expand=True, fill="both")

# Funciones para navegación
def mostrar_registro_pantalla():
    mostrar_pantalla(ventana, register_screen)

def mostrar_login_pantalla():
    mostrar_pantalla(ventana, login_screen)

def mostrar_admin_pantalla():
    admin_screen = tk.Frame(ventana, bg="#E0F7FA", bd=1, relief="solid")
    admin_screen.pack(expand=True, fill="both")
    tk.Label(admin_screen, text="Panel de Administrador", font=("Segoe UI", 16, "bold")).pack(pady=20)
    mostrar_pantalla(ventana, admin_screen)

def mostrar_main_pantalla(usuario):
    global usuario_actual_global
    usuario_actual_global = usuario

    main_screen = crear_main_screen(ventana, usuario, mostrar_perfil_pantalla)
    mostrar_pantalla(ventana, main_screen)

def mostrar_perfil_pantalla():
    global usuario_actual_global
    
    # Obtener los datos del usuario antes de mostrar la pantalla de perfil
    datos_usuario = obtener_datos_usuario(usuario_actual_global)
    if datos_usuario:
        nombres_actual, apellidos_actual, usuario_actual, email_actual, cedula_actual, fecha_registro_actual, rol_actual = datos_usuario
        perfil_screen = crear_perfil_screen(ventana, nombres_actual, apellidos_actual, usuario_actual, email_actual, cedula_actual, fecha_registro_actual, rol_actual, lambda: mostrar_main_pantalla(usuario_actual))
        mostrar_pantalla(ventana, perfil_screen)
    else:
        messagebox.showerror("Error", "No se pudieron obtener los datos del usuario.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Usuarios")
ventana.geometry("900x700")
ventana.configure(bg="#f3f4f6")

# Crear las pantallas
login_screen = crear_login_screen(ventana, mostrar_registro_pantalla, mostrar_main_pantalla, mostrar_admin_pantalla)
register_screen = crear_register_screen(ventana, mostrar_login_pantalla)

# Mostrar la pantalla inicial
mostrar_pantalla(ventana, login_screen)

ventana.mainloop()