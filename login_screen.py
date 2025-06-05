import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from auth import verificar_credenciales
import os

# Configuración de CustomTkinter
ctk.set_appearance_mode("dark")  # Opciones: "light", "dark", "system"
ctk.set_default_color_theme("blue")  # También puedes usar "green", "dark-blue")

def crear_login_screen(parent, mostrar_registro, mostrar_principal, mostrar_admin):
    print("Directorio actual:", os.getcwd())

    # Contenedor principal
    pantalla_login = ctk.CTkFrame(parent)
    pantalla_login.pack(expand=True, fill="both")

    # Cargar la imagen de fondo
    try:
        original_imagen = Image.open(os.path.join("media", "background1.jpg"))
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró 'media/background1.jpg'. Verifica la ruta de la imagen.")
        return pantalla_login

    # Crear `CTkImage` correctamente desde el principio
    foto_ctk = ctk.CTkImage(light_image=original_imagen, dark_image=original_imagen, size=(900, 700))
    label_fondo = ctk.CTkLabel(pantalla_login, image=foto_ctk, text="", fg_color="transparent")
    label_fondo.place(relx=0, rely=0, relwidth=1, relheight=1)

    def redimensionar_fondo(event):
        nuevo_ancho = event.width
        nuevo_alto = event.height

        # Evitar `ImageTk.PhotoImage` y actualizar `CTkImage`
        label_fondo.configure(image=ctk.CTkImage(light_image=original_imagen, dark_image=original_imagen, size=(nuevo_ancho, nuevo_alto)))

    pantalla_login.bind('<Configure>', redimensionar_fondo)

    # Contenedor del formulario con mayor padding y bordes redondeados
    contenedor_central = ctk.CTkFrame(pantalla_login, corner_radius=15, fg_color="#2C3E50")
    contenedor_central.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(contenedor_central, 
                 text="Iniciar Sesión", 
                 font=("Segoe UI", 22, "bold"),
                 text_color="#ECF0F1").pack(pady=(15, 20))

    entry_login_usuario = crear_input_estilizado(contenedor_central, "Usuario:")
    entry_login_contrasena = crear_input_estilizado(contenedor_central, "Contraseña:", show="*")

    ver_login_var = ctk.BooleanVar()
    ctk.CTkCheckBox(contenedor_central, 
                    text="Mostrar contraseña", 
                    variable=ver_login_var, 
                    command=lambda: toggle_password([entry_login_contrasena], ver_login_var),
                    text_color="#ECF0F1").pack(pady=10)

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

    btn_login = ctk.CTkButton(contenedor_central, text="Iniciar Sesión", command=login, 
                              fg_color="#2980B9", hover_color="#3498DB", width=180)
    btn_login.pack(pady=15)

    btn_registro = ctk.CTkButton(contenedor_central, text="Registrarse", command=mostrar_registro, 
                                 fg_color="#27AE60", hover_color="#2ECC71", width=180)
    btn_registro.pack(pady=5)

    return pantalla_login

def toggle_password(entries, var):
    for entry in entries:
        entry.configure(show="" if var.get() else "*")

def crear_input_estilizado(frame_padre, texto, ancho_entry=24, show=""):
    contenedor_input = ctk.CTkFrame(frame_padre, fg_color="transparent")
    label = ctk.CTkLabel(contenedor_input, text=texto, font=("Segoe UI", 12, "bold"), text_color="#ECF0F1")
    entry = ctk.CTkEntry(contenedor_input, width=ancho_entry * 10, show=show, border_color="#ECF0F1")
    label.pack(fill='x', padx=10, pady=(0, 5))
    entry.pack(fill='x', padx=10, pady=(0, 10))
    contenedor_input.pack(pady=8, fill='x')
    return entry

# Bloque para prueba independiente del módulo
if __name__ == '__main__':
    def mostrar_registro():
        print("Mostrar registro (función de ejemplo)")
    def mostrar_principal(usuario):
        print("Mostrar pantalla principal para", usuario)
    def mostrar_admin(parent):
        print("Mostrar pantalla de administrador")

    root = ctk.CTk()
    root.geometry("900x700")
    root.title("Sistema de Usuarios")

    login_screen = crear_login_screen(root, mostrar_registro, mostrar_principal, mostrar_admin)

    root.mainloop()