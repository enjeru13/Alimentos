import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image


class SearchBar(ctk.CTkFrame):

    def __init__(self, parent, categorias, on_search, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_search = on_search

        cats = ["Todas"] + [c.nombre for c in categorias]
        self.combo_cat = ctk.CTkComboBox(self, values=cats, width=150)
        self.combo_cat.set("Todas")
        self.combo_cat.pack(side="left", padx=(10, 5))

        self.entry = ctk.CTkEntry(self, placeholder_text="Nombre...", width=300)
        self.entry.pack(side="left", padx=5, fill="x", expand=True)

        btn = ctk.CTkButton(self, text="Buscar", command=self._buscar)
        btn.pack(side="left", padx=10)

    def _buscar(self):
        term = self.entry.get().strip()
        cat = self.combo_cat.get()
        self.on_search(term, cat)
