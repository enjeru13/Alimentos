import tkinter as tk
from tkinter import messagebox
import re
from PIL import Image, ImageTk
from auth import insertar_usuario, usuario_existe
import os

def crear_register_screen(parent, mostrar_login):
    
    # Contenedor principal que ocupa toda la ventana
    pantalla_registro = tk.Frame(parent, bg="#f3f4f6")
    pantalla_registro.pack(expand=True, fill="both")
    
    try:
        original_imagen = Image.open(os.path.join("media", "background.jpg"))
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró 'media/background.jpg'. Verifica la ruta de la imagen.")
        return pantalla_registro
    
    label_fondo = tk.Label(pantalla_registro)
    label_fondo.place(relx=0, rely=0, relwidth=1, relheight=1)
    label_fondo.lower()
    
    def redimensionar_fondo(event):
        nuevo_ancho = event.width
        nuevo_alto = event.height
        imagen_redimensionada = original_imagen.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
        foto_redimensionada = ImageTk.PhotoImage(imagen_redimensionada)
        label_fondo.config(image=foto_redimensionada)
        label_fondo.image = foto_redimensionada
    
    pantalla_registro.bind('<Configure>', redimensionar_fondo)
    
    contenedor_central = tk.Frame(pantalla_registro, bg="white", padx=25, pady=20, relief="solid", bd=1)
    contenedor_central.place(relx=0.7, rely=0.5, anchor=tk.CENTER)
    
    tk.Label(contenedor_central, 
             text="Registro de Usuario", 
             font=("Segoe UI", 18, "bold"),
             fg="#333", 
             bg="white").pack(pady=(20, 10))
    
    # Crear campos de entrada
    entry_nombres = crear_input_apilado_estetico(contenedor_central, "Nombres:")
    entry_apellidos = crear_input_apilado_estetico(contenedor_central, "Apellidos:")
    entry_cedula = crear_input_apilado_estetico(contenedor_central, "Cédula de Identidad:")
    entry_usuario = crear_input_apilado_estetico(contenedor_central, "Usuario:")
    entry_email = crear_input_apilado_estetico(contenedor_central, "Email:")
    entry_contrasena = crear_input_apilado_estetico(contenedor_central, "Contraseña:", show="*")
    
    # Campo para confirmar la contraseña
    contenedor_confirmar = tk.Frame(contenedor_central, bg="white")
    label_confirmar_contrasena = tk.Label(contenedor_confirmar, text="Confirmar Contraseña:", 
                                          font=("Segoe UI", 10, "bold"), bg="white", fg="#555", anchor='w')
    entry_confirmar_contrasena = tk.Entry(contenedor_confirmar, font=("Segoe UI", 10), 
                                          bd=1, relief="solid", width=20, show="*")
    label_confirmar_contrasena.pack(fill='x', padx=10, pady=(0, 2))
    entry_confirmar_contrasena.pack(fill='x', padx=10, pady=(0, 5))
    contenedor_confirmar.pack(pady=8, fill='x')
    
    # Opción para mostrar/ocultar contraseñas
    ver_registro_var = tk.BooleanVar()
    tk.Checkbutton(contenedor_central, text="Mostrar contraseñas", variable=ver_registro_var,
                   command=lambda: toggle_password([entry_contrasena, entry_confirmar_contrasena], ver_registro_var),
                   bg="white", font=("Segoe UI", 9), fg="#777", anchor='w', padx=10).pack(pady=5)
    
    # Función para registrar usuario
    def registrar_usuario():
        nombres = entry_nombres.get()
        apellidos = entry_apellidos.get()
        usuario = entry_usuario.get()
        email = entry_email.get()
        contraseña = entry_contrasena.get()
        confirmar = entry_confirmar_contrasena.get()
        cedula = entry_cedula.get()

        if not all([nombres, apellidos, usuario, email, contraseña, confirmar, cedula]):
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
        if usuario_existe(usuario, email, cedula):
            messagebox.showerror("Error", "El usuario o el email ya están registrados.")
            return
        if not cedula.isdigit() or len(cedula) not in range(7, 12):  # Ajusta el rango según tu país
            messagebox.showerror("Error", "La cédula debe contener solo números y tener una longitud válida.")
            return

        try:
            insertar_usuario(nombres, apellidos, usuario, email, contraseña, cedula)
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            mostrar_login()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el usuario: {e}")
    
    tk.Button(contenedor_central, text="Registrar", command=registrar_usuario,
              bg="#28A745", fg="white", font=("Segoe UI", 11, "bold"),
              relief="flat", padx=15, pady=8, width=15).pack(pady=15)
    
    tk.Button(contenedor_central, text="Ir a Login", command=mostrar_login,
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

def crear_input_apilado_estetico(frame_padre, texto, ancho_entry=20, show=""):
    contenedor_input = tk.Frame(frame_padre, bg="white")
    label = tk.Label(contenedor_input, text=texto, font=("Segoe UI", 10, "bold"),
                     bg="white", fg="#555", anchor='w')
    entry = tk.Entry(contenedor_input, font=("Segoe UI", 10), bd=1, relief="solid", width=ancho_entry, show=show)
    label.pack(fill='x', padx=10, pady=(0, 2))
    entry.pack(fill='x', padx=10, pady=(0, 5))
    contenedor_input.pack(pady=8, fill='x')
    return entry

# Bloque para prueba independiente del módulo
if __name__ == '__main__':
    def mostrar_login():
        print("Volviendo a Login (función de ejemplo)")
    
    root = tk.Tk()
    root.geometry("900x700")
    root.title("Registro de Usuario")
    
    register_screen = crear_register_screen(root, mostrar_login)
    
    root.mainloop()