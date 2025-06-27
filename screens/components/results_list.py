import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image


class ResultsList(ctk.CTkScrollableFrame):
    """
    Lista de resultados. Recibe lista de alimentos (obj con id_producto,
    nom_producto e imagen_url), y llama a on_select(id) al pinchar.
    """

    def __init__(self, parent, on_select, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_select = on_select

    def update(self, items):
        # Limpiar
        for w in self.winfo_children():
            w.destroy()

        # Mostrar cada alimento
        for al in items:
            icon = None
            if getattr(al, "imagen_url", None):
                try:
                    pil = Image.open(al.imagen_url)
                    pil.thumbnail((30, 30))
                    icon = CTkImage(light_image=pil, dark_image=pil, size=(30, 30))
                except:
                    icon = None

            btn = ctk.CTkButton(
                self,
                text=f"  {al.nom_producto}",
                image=icon,
                compound="left",
                fg_color="#3498DB",
                hover_color="#2980B9",
                anchor="w",
                command=lambda pid=al.id_producto: self.on_select(pid),
            )
            btn.image_ref = icon
            btn.pack(fill="x", padx=5, pady=3)
