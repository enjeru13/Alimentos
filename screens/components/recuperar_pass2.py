import customtkinter as ctk
from tkinter import messagebox
from controllers.usuarios_controller import completar_recuperacion
from utils.db_utils import obtener_pregunta


def abrir_recuperar_paso2(parent, usuario_id: int, pregunta: str):
    top = ctk.CTkToplevel(parent)
    top.title("Restablecer Contraseña")
    top.geometry("350x260")

    ctk.CTkLabel(top, text=pregunta, wraplength=300).pack(pady=(20, 5), padx=20)
    entry_resp = ctk.CTkEntry(top, placeholder_text="Tu respuesta")
    entry_new = ctk.CTkEntry(top, placeholder_text="Nueva contraseña", show="*")
    entry_conf = ctk.CTkEntry(top, placeholder_text="Repetir contraseña", show="*")

    for w in (entry_resp, entry_new, entry_conf):
        w.pack(pady=5, fill="x", padx=20)

    def restablecer():
        r = entry_resp.get().strip()
        n = entry_new.get().strip()
        c = entry_conf.get().strip()
        if not (r and n and c):
            messagebox.showerror("Error", "Completa todos los campos.")
            return
        if n != c:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return
        ok = completar_recuperacion(usuario_id, r, n)
        if not ok:
            messagebox.showerror("Error", "Respuesta incorrecta.")
            return
        messagebox.showinfo("Éxito", "Contraseña restablecida.")
        top.destroy()

    ctk.CTkButton(top, text="Restablecer", command=restablecer).pack(pady=20)
    return top
