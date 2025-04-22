import tkinter as tk
from tkinter import messagebox
import re
from auth import insertar_usuario, usuario_existe

def crear_register_screen(contenedor, mostrar_login):
    pantalla_registro = tk.Frame(contenedor, bg="#f3f4f6", bd=1, width=350, height=650)
    pantalla_registro.pack_propagate(False)

    tk.Label(pantalla_registro, text="Registro de Usuario", font=("Segoe UI", 18, "bold"),
             fg="#333", bg="#f3f4f6").pack(pady=(20, 10))

    entry_nombres_list = []
    entry_apellidos_list = []
    entry_usuario_list = []
    entry_email_list = []
    entry_contrasena_list = []
    entry_confirmar_list = []

    entry_nombres = crear_input_apilado_estetico(pantalla_registro, "Nombres:", entry_nombres_list)
    entry_apellidos = crear_input_apilado_estetico(pantalla_registro, "Apellidos:", entry_apellidos_list)
    entry_usuario = crear_input_apilado_estetico(pantalla_registro, "Usuario:", entry_usuario_list)
    entry_email = crear_input_apilado_estetico(pantalla_registro, "Email:", entry_email_list)
    entry_contrasena = crear_input_apilado_estetico(pantalla_registro, "Contraseña:", entry_contrasena_list, show="*")

    contenedor_confirmar = tk.Frame(pantalla_registro, bg="#f3f4f6")
    label_confirmar_contrasena = tk.Label(contenedor_confirmar, text="Confirmar Contraseña:", font=("Segoe UI", 10, "bold"), bg="#f3f4f6", fg="#555", anchor='w')
    entry_confirmar_contrasena = tk.Entry(contenedor_confirmar, font=("Segoe UI", 10), bd=1, relief="groove", width=20, show="*")
    entry_confirmar_list.append(entry_confirmar_contrasena)
    label_confirmar_contrasena.pack(fill='x', padx=10, pady=(0, 2))
    entry_confirmar_contrasena.pack(fill='x', padx=10, pady=(0, 5))
    contenedor_confirmar.pack(pady=8, fill='x')

    ver_registro_var = tk.BooleanVar()
    tk.Checkbutton(pantalla_registro, text="Mostrar contraseñas", variable=ver_registro_var,
                    command=lambda: toggle_password([entry_contrasena, entry_confirmar_contrasena], ver_registro_var),
                    bg="#f3f4f6", font=("Segoe UI", 9), fg="#777", anchor='w', padx=10).pack(pady=5)

    def registrar_usuario():
        nombres = entry_nombres.get()
        apellidos = entry_apellidos.get()
        usuario = entry_usuario.get()
        email = entry_email.get()
        contraseña = entry_contrasena.get()
        confirmar = entry_confirmar_contrasena.get()

        if not all([nombres, apellidos, usuario, email, contraseña, confirmar]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        if contraseña != confirmar:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return
        if not es_email_valido(email):
            messagebox.showerror("Error", "El email no es válido.")
            return
        if not es_contraseña_segura(contraseña):
            messagebox.showerror("Error", "La contraseña debe tener al menos 8 caracteres.")
            return
        if usuario_existe(usuario, email):
            messagebox.showerror("Error", "El usuario o el email ya están registrados.")
            return

        try:
            insertar_usuario(nombres, apellidos, usuario, email, contraseña) # El rol por defecto es 'usuario'
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            mostrar_login()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el usuario: {e}")

    tk.Button(pantalla_registro, text="Registrar", command=registrar_usuario,
              bg="#28A745", fg="white", font=("Segoe UI", 11, "bold"),
              relief="flat", padx=15, pady=8, width=15).pack(pady=15)

    tk.Button(pantalla_registro, text="Ir a Login", command=mostrar_login,
              bg="#6C757D", fg="white", font=("Segoe UI", 10),
              relief="flat", padx=10, pady=5, width=15).pack(pady=5)

    return pantalla_registro

def es_email_valido(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def es_contraseña_segura(contraseña):
    return len(contraseña) >= 8

def toggle_password(entries, var):
    for entry in entries:
        entry.config(show="" if var.get() else "*")

def crear_input_apilado_estetico(frame_padre, texto, var, ancho_entry=20, show=""):
    contenedor_input = tk.Frame(frame_padre, bg="#f3f4f6")
    label = tk.Label(contenedor_input, text=texto, font=("Segoe UI", 10, "bold"), bg="#f3f4f6", fg="#555", anchor='w')
    entry = tk.Entry(contenedor_input, font=("Segoe UI", 10), bd=1, relief="groove", width=ancho_entry, show=show)
    var.append(entry)
    label.pack(fill='x', padx=10, pady=(0, 2))
    entry.pack(fill='x', padx=10, pady=(0, 5))
    contenedor_input.pack(pady=8, fill='x')
    return entry