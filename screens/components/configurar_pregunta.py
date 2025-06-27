import customtkinter as ctk
from tkinter import messagebox
from controllers.usuarios_controller import set_pregunta_seguridad


def abrir_configurar_pregunta(parent, usuario, on_guardado=None):
    top = ctk.CTkToplevel(parent)
    top.title("Configurar pregunta de seguridad")
    top.geometry("350x260")

    ctk.CTkLabel(top, text="Pregunta de seguridad:").pack(pady=(20, 5))
    entry_preg = ctk.CTkEntry(top)
    entry_preg.pack(pady=5, fill="x", padx=20)

    ctk.CTkLabel(top, text="Respuesta:").pack(pady=(10, 5))
    entry_resp = ctk.CTkEntry(top)
    entry_resp.pack(pady=5, fill="x", padx=20)

    def guardar():
        preg = entry_preg.get().strip()
        resp = entry_resp.get().strip().lower()
        if not preg or len(resp) < 4:
            return messagebox.showerror(
                "Error", "Pregunta vacía o respuesta muy corta."
            )
        set_pregunta_seguridad(usuario, preg, resp)
        messagebox.showinfo("Listo", "Pregunta guardada.")
        top.destroy()
        if on_guardado:
            on_guardado()

    ctk.CTkButton(top, text="Guardar", command=guardar).pack(pady=20)
    return top
