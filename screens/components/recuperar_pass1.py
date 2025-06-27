import customtkinter as ctk
from tkinter import messagebox
from controllers.usuarios_controller import iniciar_recuperacion


def abrir_recuperar_paso1(parent, on_success):
    top = ctk.CTkToplevel(parent)
    top.title("Recuperar Contraseña")
    top.geometry("350x200")

    ctk.CTkLabel(top, text="Usuario o Email:").pack(pady=(20, 5))
    entry_usr = ctk.CTkEntry(top)
    entry_usr.pack(pady=5, fill="x", padx=20)

    def siguiente():
        usuario = entry_usr.get().strip()
        q = iniciar_recuperacion(usuario)
        if not q:
            return messagebox.showerror(
                "Error", "Usuario/Email no encontrado o sin pregunta."
            )
        top.destroy()
        on_success(usuario, q)

    ctk.CTkButton(top, text="Siguiente", command=siguiente).pack(pady=20)
    return top
