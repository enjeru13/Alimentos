import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from auth import verificar_credenciales

def crear_login_screen(contenedor, mostrar_registro, mostrar_principal, mostrar_admin):
    pantalla_login = tk.Frame(contenedor, bg="#f3f4f6", bd=1, width=300, height=400)
    pantalla_login.pack_propagate(False)

    tk.Label(pantalla_login, text="Iniciar Sesión", font=("Segoe UI", 18, "bold"), fg="#333", bg="#f3f4f6").pack(pady=(20, 10))

    entry_login_usuario_list = []
    entry_login_contrasena_list = []
    entry_login_usuario = crear_input_apilado_estetico(pantalla_login, "Usuario:", entry_login_usuario_list)
    entry_login_contrasena = crear_input_apilado_estetico(pantalla_login, "Contraseña:", entry_login_contrasena_list, show="*")

    ver_login_var = tk.BooleanVar()
    tk.Checkbutton(pantalla_login, text="Mostrar contraseña", variable=ver_login_var,
                    command=lambda: toggle_password([entry_login_contrasena], ver_login_var),
                    bg="#f3f4f6", font=("Segoe UI", 9), fg="#777", anchor='w', padx=10).pack(pady=5)

    def login():
        usuario = entry_login_usuario.get()
        contraseña = entry_login_contrasena.get()
        if not usuario or not contraseña:
            messagebox.showerror("Error", "Por favor, ingrese ambos campos.")
            return
        exito, rol = verificar_credenciales(usuario, contraseña)
        if exito:
            messagebox.showinfo("Bienvenido", f"¡Bienvenido, {usuario}!")
            if rol == 'admin':
                mostrar_admin(contenedor)
            else:
                mostrar_principal(usuario)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    tk.Button(pantalla_login, text="Iniciar Sesión", command=login,
              bg="#007BFF", fg="white", font=("Segoe UI", 11, "bold"),
              relief="flat", padx=15, pady=8, width=15).pack(pady=15)

    tk.Button(pantalla_login, text="Ir a Registro", command=mostrar_registro,
              bg="#6C757D", fg="white", font=("Segoe UI", 10),
              relief="flat", padx=10, pady=5, width=15).pack(pady=5)

    return pantalla_login

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