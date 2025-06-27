import customtkinter as ctk
from tkinter import messagebox

from controllers.categorias_controller import listar_categorias
from controllers.alimentos_controller import listar_alimentos_por_categoria


def crear_categorias_user_screen(parent, volver_cb):
    pantalla = ctk.CTkFrame(parent, fg_color="transparent")
    pantalla.pack(expand=True, fill="both", padx=40, pady=40)
    pantalla.bind_class("CTkButton", "<Return>", lambda e: e.widget.invoke())

    header = ctk.CTkFrame(pantalla, corner_radius=8)
    header.pack(fill="x", pady=(20, 20), padx=20)

    title_lbl = ctk.CTkLabel(header, text="Categorias", font=("Segoe UI", 24, "bold"))
    title_lbl.pack(expand=True, pady=10)

    content = ctk.CTkFrame(pantalla, corner_radius=8)
    content.pack(expand=True, fill="both", padx=20, pady=(0, 20))

    scroll = ctk.CTkScrollableFrame(
        content,
        corner_radius=8,
        border_width=1,
    )
    scroll.pack(fill="both", expand=True, padx=10, pady=10)

    def _show_alimentos(id_cat: int, nombre: str):
        top = ctk.CTkToplevel(pantalla)
        top.title(f"Alimentos en {nombre}")
        top.geometry("500x400")
        sc2 = ctk.CTkScrollableFrame(top, corner_radius=8)
        sc2.pack(expand=True, fill="both", padx=20, pady=20)

        alimentos = listar_alimentos_por_categoria(id_cat)
        if alimentos:
            for al in alimentos:
                txt = (
                    f"{al.nom_producto} — "
                    f"{al.calorias or 0} kcal / "
                    f"{al.proteina or 0}g P / "
                    f"{al.grasas or 0}g G"
                )
                ctk.CTkLabel(sc2, text=txt, font=("Segoe UI", 12), anchor="w").pack(
                    fill="x", padx=10, pady=4
                )
        else:
            ctk.CTkLabel(
                sc2, text="No hay alimentos en esta categoría.", font=("Segoe UI", 14)
            ).pack(pady=20)

        ctk.CTkButton(
            top,
            text="Cerrar",
            width=100,
            height=32,
            corner_radius=8,
            command=top.destroy,
        ).pack(pady=(0, 20))

    def _populate():
        for w in scroll.winfo_children():
            w.destroy()

        cats = listar_categorias()
        if not cats:
            ctk.CTkLabel(
                scroll, text="No hay categorías disponibles.", font=("Segoe UI", 14)
            ).pack(pady=20)
            return

        for cat in cats:
            btn = ctk.CTkButton(
                scroll,
                text=cat.nombre,
                width=250,
                height=36,
                corner_radius=8,
                anchor="w",
                command=lambda c=cat: _show_alimentos(c.id_categoria, c.nombre),
            )
            btn.pack(fill="x", padx=10, pady=6)

    footer = ctk.CTkFrame(pantalla, fg_color="transparent")
    footer.pack(fill="x", padx=20, pady=(0, 20))

    ctk.CTkButton(
        footer,
        text="← Volver al Menú",
        width=160,
        height=36,
        corner_radius=8,
        command=volver_cb,
    ).pack(side="left")

    _populate()
    return pantalla
