import customtkinter as ctk
from tkinter import messagebox
from models.usuario import Usuario
from controllers.usuarios_controller import actualizar_usuario
import bcrypt


def abrir_editor_perfil(parent, usuario_actual: Usuario, on_guardado=None):

    top = ctk.CTkToplevel(parent)
    top.title("Editar Perfil")
    top.geometry("400x360")
    top.resizable(False, False)

    ctk.CTkLabel(
        top, text="Editar Perfil", font=("Segoe UI", 18, "bold"), justify="center"
    ).pack(pady=(20, 10))

    frame = ctk.CTkFrame(top, corner_radius=8)
    frame.pack(padx=20, pady=10, fill="both", expand=True)
    frame.grid_columnconfigure(0, weight=1)

    entry_nom = ctk.CTkEntry(frame, placeholder_text="Nombres")
    entry_ap = ctk.CTkEntry(frame, placeholder_text="Apellidos")
    entry_usr = ctk.CTkEntry(frame, placeholder_text="Nombre de usuario")
    entry_pass = ctk.CTkEntry(
        frame, placeholder_text="Nueva contraseña (opcional)", show="*"
    )

    entry_nom.insert(0, usuario_actual.nombres)
    entry_ap.insert(0, usuario_actual.apellidos)
    entry_usr.insert(0, usuario_actual.nombre_usuario)

    entry_nom.pack(pady=5, fill="x")
    entry_ap.pack(pady=5, fill="x")
    entry_usr.pack(pady=5, fill="x")
    entry_pass.pack(pady=5, fill="x")

    def guardar_cambios():
        nuevos_nombres = entry_nom.get().strip()
        nuevos_ap = entry_ap.get().strip()
        nuevo_usr = entry_usr.get().strip()
        nueva_pass = entry_pass.get().strip()

        if not nuevos_nombres or not nuevos_ap or not nuevo_usr:
            messagebox.showerror(
                "Error", "Todos los campos excepto la contraseña son obligatorios."
            )
            return

        usuario_actual.nombres = nuevos_nombres
        usuario_actual.apellidos = nuevos_ap
        usuario_actual.nombre_usuario = nuevo_usr

        if nueva_pass:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(nueva_pass.encode("utf-8"), salt)
            usuario_actual.contraseña = hashed.decode("utf-8")

        try:
            actualizar_usuario(usuario_actual)
            messagebox.showinfo("Listo", "Perfil actualizado correctamente.")
            top.destroy()
            if on_guardado:
                on_guardado()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ctk.CTkButton(
        frame, text="Guardar Cambios", command=guardar_cambios, corner_radius=8
    ).pack(pady=(15, 10))

    return top
