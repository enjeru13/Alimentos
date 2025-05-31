import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from auth import verificar_credenciales
import os

def crear_login_screen(parent, mostrar_registro, mostrar_principal, mostrar_admin):
    print("Directorio actual:", os.getcwd())

    # Contenedor principal que ocupa toda la ventana.
    pantalla_login = tk.Frame(parent, bg="#E3F2FD")
    pantalla_login.pack(expand=True, fill="both")

    try:
        original_imagen = Image.open(os.path.join("media", "background.jpg"))
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró 'media/background.jpg'. Verifica la ruta de la imagen.")
        return pantalla_login

    label_fondo = tk.Label(pantalla_login)
    label_fondo.place(relx=0, rely=0, relwidth=1, relheight=1)
    label_fondo.lower()

    def redimensionar_fondo(event):
        nuevo_ancho = event.width
        nuevo_alto = event.height
        imagen_redimensionada = original_imagen.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
        foto_redimensionada = ImageTk.PhotoImage(imagen_redimensionada)
        label_fondo.config(image=foto_redimensionada)
        label_fondo.image = foto_redimensionada

    pantalla_login.bind('<Configure>', redimensionar_fondo)

    # Contenedor del formulario.
    contenedor_central = tk.Frame(pantalla_login, bg="white", padx=25, pady=20, relief="solid", bd=1)
    # Posicionar el formulario; aquí se coloca al 70% del ancho y centrado verticalmente.
    contenedor_central.place(relx=0.7, rely=0.5, anchor="center")

    # Título del formulario.
    tk.Label(contenedor_central,
             text="Iniciar Sesión",
             font=("Segoe UI", 20, "bold"),
             fg="#333",
             bg="white").pack(pady=(10, 20))

    # Campos de entrada para usuario y contraseña.
    entry_login_usuario = crear_input_estilizado(contenedor_central, "Usuario:")
    entry_login_contrasena = crear_input_estilizado(contenedor_central, "Contraseña:", show="*")

    # Checkbox para mostrar/ocultar la contraseña.
    ver_login_var = tk.BooleanVar()
    tk.Checkbutton(contenedor_central,
                   text="Mostrar contraseña",
                   variable=ver_login_var,
                   command=lambda: toggle_password([entry_login_contrasena], ver_login_var),
                   bg="white",
                   font=("Segoe UI", 10),
                   fg="#777").pack(pady=5)

    # Función para gestionar el inicio de sesión.
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
                mostrar_admin(parent)
            else:
                mostrar_principal(usuario)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    btn_login = tk.Button(contenedor_central,
                          text="Iniciar Sesión",
                          command=login,
                          bg="#007BFF", fg="white",
                          font=("Segoe UI", 12, "bold"),
                          relief="flat", padx=15, pady=8)
    btn_login.pack(pady=15)
    btn_login.bind("<Enter>", lambda e: btn_login.config(bg="#0056b3"))
    btn_login.bind("<Leave>", lambda e: btn_login.config(bg="#007BFF"))

    btn_registro = tk.Button(contenedor_central,
                             text="Registrarse",
                             command=mostrar_registro,
                             bg="#6C757D", fg="white",
                             font=("Segoe UI", 11),
                             relief="flat", padx=10, pady=6)
    btn_registro.pack(pady=5)
    btn_registro.bind("<Enter>", lambda e: btn_registro.config(bg="#545b62"))
    btn_registro.bind("<Leave>", lambda e: btn_registro.config(bg="#6C757D"))

    return pantalla_login

def toggle_password(entries, var):
    for entry in entries:
        entry.config(show="" if var.get() else "*")

def crear_input_estilizado(frame_padre, texto, ancho_entry=22, show=""):
    contenedor_input = tk.Frame(frame_padre, bg="white")
    label = tk.Label(contenedor_input,
                     text=texto,
                     font=("Segoe UI", 11, "bold"),
                     bg="white", fg="#555")
    entry = tk.Entry(contenedor_input,
                     font=("Segoe UI", 11),
                     bd=1, relief="solid",
                     width=ancho_entry,
                     show=show)
    label.pack(fill='x', padx=10, pady=(0, 3))
    entry.pack(fill='x', padx=10, pady=(0, 5))
    contenedor_input.pack(pady=8, fill='x')
    return entry

if __name__ == '__main__':
    def mostrar_registro():
        print("Mostrar registro (función de ejemplo)")
    def mostrar_principal(usuario):
        print("Mostrar pantalla principal para", usuario)
    def mostrar_admin(parent):
        print("Mostrar pantalla de administrador")

    root = tk.Tk()
    root.geometry("900x700")
    root.title("Sistema de Usuarios")

    login_screen = crear_login_screen(root, mostrar_registro, mostrar_principal, mostrar_admin)

    root.mainloop()