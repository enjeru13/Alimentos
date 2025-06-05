import customtkinter as ctk
import re
from PIL import Image
from auth import insertar_usuario, usuario_existe
import os
from datetime import datetime
from tkinter import messagebox

# Configuración de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def crear_register_screen(parent, mostrar_login):
    pantalla_registro = ctk.CTkFrame(parent)
    pantalla_registro.pack(expand=True, fill="both")

    # Cargar la imagen de fondo
    try:
        original_imagen = Image.open(os.path.join("media", "background1.jpg"))
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró 'media/background1.jpg'. Verifica la ruta de la imagen.")
        return pantalla_registro

    foto_ctk = ctk.CTkImage(light_image=original_imagen, dark_image=original_imagen, size=(900, 700))
    label_fondo = ctk.CTkLabel(pantalla_registro, image=foto_ctk, text="", fg_color="transparent")
    label_fondo.place(relx=0, rely=0, relwidth=1, relheight=1)

    def redimensionar_fondo(event):
        label_fondo.configure(image=ctk.CTkImage(light_image=original_imagen, dark_image=original_imagen, size=(event.width, event.height)))

    pantalla_registro.bind('<Configure>', redimensionar_fondo)

    # Contenedor central
    contenedor_central = ctk.CTkFrame(pantalla_registro, corner_radius=15, fg_color="#2C3E50", width=650)
    contenedor_central.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(contenedor_central, text="Registro de Usuario", font=("Segoe UI", 22, "bold"), text_color="#ECF0F1").pack(pady=(15, 20))

    # Campos del formulario
    entry_nombres, entry_apellidos = crear_fila_estilizada(contenedor_central, "Nombres:", "Apellidos:")
    entry_cedula, entry_email = crear_fila_estilizada(contenedor_central, "Cédula:", "Email:")
    entry_usuario, entry_año_seccion = crear_fila_estilizada(contenedor_central, "Usuario:", "Año y Sección:")
    entry_contrasena, entry_confirmar_contrasena = crear_fila_estilizada(contenedor_central, "Contraseña:", "Confir. Contraseña:", show="*")

    # Opción para mostrar/ocultar contraseñas
    ver_registro_var = ctk.BooleanVar()
    ctk.CTkCheckBox(contenedor_central, text="Mostrar contraseñas", variable=ver_registro_var,
                    command=lambda: toggle_password([entry_contrasena, entry_confirmar_contrasena], ver_registro_var),
                    text_color="#ECF0F1").pack(pady=10)

    # Función para registrar usuario
    def registrar_usuario():
        nombres = entry_nombres.get()
        apellidos = entry_apellidos.get()
        usuario = entry_usuario.get()
        email = entry_email.get()
        año_seccion = entry_año_seccion.get()
        contraseña = entry_contrasena.get()
        confirmar = entry_confirmar_contrasena.get()
        cedula = entry_cedula.get()
        
        rol = "usuario"  # Asignar rol por defecto
        fecha_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Fecha actual

        if not all([nombres, apellidos, usuario, email, año_seccion, contraseña, confirmar, cedula]):
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
            messagebox.showerror("Error", "El usuario, el email o la cédula ya están registrados.")
            return
        if not cedula.isdigit() or len(cedula) not in range(7, 12):  
            messagebox.showerror("Error", "La cédula debe contener solo números y tener una longitud válida.")
            return

        try:
            insertar_usuario(nombres, apellidos, usuario, email, contraseña, cedula, año_seccion, fecha_registro, rol)  # Se envían todos los valores
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            mostrar_login()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el usuario: {e}")

    btn_registro = ctk.CTkButton(contenedor_central, text="Registrar", command=registrar_usuario,
                                 fg_color="#2980B9", hover_color="#3498DB", width=200)
    btn_registro.pack(pady=15)

    btn_login = ctk.CTkButton(contenedor_central, text="Ir a Login", command=mostrar_login,
                              fg_color="#27AE60", hover_color="#2ECC71", width=200)
    btn_login.pack(pady=5)

    return pantalla_registro

# Función para crear filas de inputs
def crear_fila_estilizada(parent, label1_text, label2_text, show=""):
    fila = ctk.CTkFrame(parent, fg_color="transparent")
    
    label_ancho = 120
    label1 = ctk.CTkLabel(fila, text=label1_text, font=("Segoe UI", 12, "bold"), text_color="#ECF0F1", width=label_ancho)
    entry1 = ctk.CTkEntry(fila, width=220, show=show)

    label2 = ctk.CTkLabel(fila, text=label2_text, font=("Segoe UI", 12, "bold"), text_color="#ECF0F1", width=label_ancho)
    entry2 = ctk.CTkEntry(fila, width=220, show=show)

    label1.grid(row=0, column=0, padx=4, pady=5, sticky="w")
    entry1.grid(row=0, column=1, padx=4, pady=5)

    label2.grid(row=0, column=2, padx=4, pady=5, sticky="w")
    entry2.grid(row=0, column=3, padx=4, pady=5)

    fila.pack(pady=12, padx=10, fill="x")
    return entry1, entry2

# Funciones auxiliares
def es_email_valido(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def es_contraseña_segura(contraseña):
    return len(contraseña) >= 8

def toggle_password(entries, var):
    for entry in entries:
        entry.configure(show="" if var.get() else "*")

# Bloque para prueba independiente
if __name__ == '__main__':
    root = ctk.CTk()
    root.geometry("900x700")
    root.title("Registro de Usuario")

    register_screen = crear_register_screen(root, lambda: print("Ir a Login"))
    
    root.mainloop()