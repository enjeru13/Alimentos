import json
import customtkinter as ctk
from customtkinter import CTkSwitch

from controllers.alimentos_controller import (
    buscar_alimentos,
    listar_alimentos,
    listar_alimentos_por_categoria,
    obtener_alimento,
)
from controllers.categorias_controller import listar_categorias
from screens.components.search_bar import SearchBar
from screens.components.results_list import ResultsList
from screens.components.detail_view import DetailView
from screens.alimentos_user_screen import crear_alimentos_user_screen
from screens.alimentos_admin_screen import crear_alimentos_admin_screen
from screens.categorias_user_screen import crear_categorias_user_screen
from screens.categorias_admin_screen import crear_categorias_admin_screen

CONFIG_PATH = "config.json"


class MainScreen(ctk.CTkFrame):
    def __init__(self, parent, usuario, rol, mostrar_perfil_cb):
        super().__init__(parent, fg_color="transparent")
        self.usuario = usuario
        self.rol = rol
        self.mostrar_perfil_cb = mostrar_perfil_cb
        self._cfg = json.load(open(CONFIG_PATH, "r"))

        self.pack(expand=True, fill="both", padx=20, pady=20)

        self._build_ui()

    def _build_ui(self):
        sidebar = ctk.CTkFrame(self, width=200, corner_radius=10)
        sidebar.pack(side="left", fill="y", padx=(0, 10), pady=0)
        sidebar.pack_propagate(False)

        ctk.CTkLabel(
            sidebar,
            text=f"Bienvenido,\n{self.usuario}",
            font=("Segoe UI", 16, "bold"),
            justify="center",
        ).pack(pady=(20, 30), padx=10)

        for txt, cmd in [
            ("Alimentos", self._open_alimentos),
            ("Categorías", self._open_categorias),
            ("Ver Perfil", self.mostrar_perfil_cb),
        ]:
            ctk.CTkButton(
                sidebar, text=txt, width=160, corner_radius=8, command=cmd
            ).pack(pady=8)

        self.theme_switch = CTkSwitch(
            sidebar, text="Modo Oscuro", command=self._toggle_theme
        )
        if ctk.get_appearance_mode() == "Dark":
            self.theme_switch.select()
        else:
            self.theme_switch.deselect()
        self.theme_switch.pack(side="bottom", pady=20)

        body = ctk.CTkFrame(self, corner_radius=10)
        body.pack(side="right", expand=True, fill="both", padx=(10, 0), pady=0)

        cats = listar_categorias()
        self.search_bar = SearchBar(body, cats, self._on_search)
        self.search_bar.pack(fill="x", pady=(0, 20), padx=10)

        self.results_list = ResultsList(body, self._on_select, width=400, height=200)
        self.results_list.pack(fill="both", expand=True, pady=(0, 20), padx=10)

        self.detail_view = DetailView(body)
        self.detail_view.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _toggle_theme(self):
        modo = "Dark" if self.theme_switch.get() else "Light"
        ctk.set_appearance_mode(modo)
        tema = "dark-blue" if modo == "Dark" else "blue"
        ctk.set_default_color_theme(tema)
        self._cfg.update({"appearance": modo, "color_theme": tema})
        json.dump(self._cfg, open(CONFIG_PATH, "w"), indent=2)

    def _open_alimentos(self):
        if self.rol == "admin":
            f = crear_alimentos_admin_screen(self.master, self.rol, self._replace_self)
        else:
            f = crear_alimentos_user_screen(self.master, self._replace_self)
        self._replace_with(f)

    def _open_categorias(self):
        if self.rol == "admin":
            f = crear_categorias_admin_screen(self.master, self.rol, self._replace_self)
        else:
            f = crear_categorias_user_screen(self.master, self._replace_self)
        self._replace_with(f)

    def _replace_with(self, frame):
        for w in self.master.winfo_children():
            w.pack_forget()
        frame.pack(expand=True, fill="both")

    def _replace_self(self):
        for w in self.master.winfo_children():
            w.pack_forget()
        self.pack(expand=True, fill="both", padx=20, pady=20)

    def _on_search(self, term, sel_cat):
        if sel_cat != "Todas":
            idc = next(
                (c.id_categoria for c in listar_categorias() if c.nombre == sel_cat),
                None,
            )
            items = listar_alimentos_por_categoria(idc) if idc else []
            if term:
                items = [a for a in items if term.lower() in a.nom_producto.lower()]
        else:
            items = buscar_alimentos(term) if term else listar_alimentos()
        self.results_list.update(items)

    def _on_select(self, idp):
        al = obtener_alimento(idp)
        self.detail_view.show(al)
