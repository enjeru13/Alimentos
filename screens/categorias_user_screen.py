import customtkinter as ctk
from tkinter import messagebox

from controllers.categorias_controller import listar_categorias
from controllers.alimentos_controller import listar_alimentos_por_categoria


def crear_categorias_user_screen(parent, volver_cb):
    pantalla = ctk.CTkFrame(parent)
    pantalla.pack(expand=True, fill="both", padx=20, pady=20)
    pantalla.bind_class("CTkButton", "<Return>", lambda e: e.widget.invoke())

    ctk.CTkLabel(pantalla, text="Categorías", font=("Segoe UI", 22, "bold")).pack(
        pady=(0, 10)
    )

    ctk.CTkButton(
        pantalla,
        text="Refrescar",
        width=120,
        corner_radius=8,
        command=lambda: _populate(),
    ).pack(pady=(0, 15))

    scroll = ctk.CTkScrollableFrame(pantalla, width=300, height=350, corner_radius=10)
    scroll.pack(expand=True, fill="both", padx=20, pady=(0, 20))

    def _show_alimentos(id_cat: int, nombre: str):
        top = ctk.CTkToplevel(pantalla)
        top.title(f"Alimentos en «{nombre}»")
        top.geometry("500x400")

        sc2 = ctk.CTkScrollableFrame(top, corner_radius=10)
        sc2.pack(expand=True, fill="both", padx=10, pady=10)

        alimentos = listar_alimentos_por_categoria(id_cat)
        if alimentos:
            for al in alimentos:
                txt = (
                    f"{al.nom_producto} — "
                    f"{al.calorias or 0} kcal / "
                    f"{al.proteina or 0}g P / "
                    f"{al.grasas or 0}g G"
                )
                ctk.CTkLabel(sc2, text=txt, anchor="w", font=("Segoe UI", 12)).pack(
                    fill="x", padx=5, pady=2
                )
        else:
            ctk.CTkLabel(
                sc2, text="No hay alimentos en esta categoría.", font=("Segoe UI", 14)
            ).pack(pady=20)

        ctk.CTkButton(
            top, text="Cerrar", width=100, corner_radius=8, command=top.destroy
        ).pack(pady=(0, 15))

    def _populate():
        cats = listar_categorias()
        print("DEBUG: listar_categorias() ->", cats)

        for w in scroll.winfo_children():
            w.destroy()

        if not cats:
            ctk.CTkLabel(
                scroll, text="No hay categorías disponibles.", font=("Segoe UI", 14)
            ).pack(pady=20)
            return

        for cat in cats:
            ctk.CTkButton(
                scroll,
                text=cat.nombre,
                width=250,
                corner_radius=8,
                anchor="w",
                command=lambda c=cat: _show_alimentos(c.id_categoria, c.nombre),
            ).pack(fill="x", padx=10, pady=6)

    _populate()

    ctk.CTkButton(
        pantalla, text="Volver al Menú", width=200, corner_radius=8, command=volver_cb
    ).pack(side="bottom", pady=(0, 10))

    return pantalla
