# screens/categorias_user_screen.py

import customtkinter as ctk
from controllers.categorias_controller import listar_categorias
from controllers.alimentos_controller import listar_alimentos_por_categoria


def crear_categorias_user_screen(parent, volver_cb):
    """
    Pantalla de categorías (solo lectura) para usuarios.
    Al hacer click en una categoría abre un Toplevel con los alimentos de esa categoría.
    volver_cb(): callback que oculta esta pantalla y muestra el menú principal.
    """
    pantalla = ctk.CTkFrame(parent)
    pantalla.pack(expand=True, fill="both")

    # — Título —
    ctk.CTkLabel(
        pantalla, text="Categorías", font=("Segoe UI", 22, "bold"),
    ).pack(pady=20)

    # — Lista scrollable de categorías —
    scroll = ctk.CTkScrollableFrame(pantalla, width=400, height=300)
    scroll.pack(padx=20, pady=10, fill="both", expand=True)

    def _show_alimentos(id_cat: int, nombre: str):
        """
        Muestra en un Toplevel la lista de alimentos de la categoría.
        Usa listar_alimentos_por_categoria() del controller.
        """
        top = ctk.CTkToplevel(pantalla)
        top.title(f"Alimentos en «{nombre}»")
        top.geometry("500x400")

        scroll2 = ctk.CTkScrollableFrame(top)
        scroll2.pack(expand=True, fill="both", padx=10, pady=10)

        alimentos = listar_alimentos_por_categoria(id_cat)
        if alimentos:
            for al in alimentos:
                txt = (
                    f"{al.nom_producto} — "
                    f"{al.calorias or 0} kcal / "
                    f"{al.proteina or 0}g P / "
                    f"{al.grasas or 0}g G"
                )
                ctk.CTkLabel(scroll2, text=txt, anchor="w", font=("Segoe UI", 12)).pack(
                    fill="x", pady=2, padx=5
                )
        else:
            ctk.CTkLabel(
                scroll2,
                text="No hay alimentos en esta categoría.",
                font=("Segoe UI", 14),
            ).pack(pady=10)

        ctk.CTkButton(
            top,
            text="Cerrar",
            command=top.destroy,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            width=100,
        ).pack(pady=(0, 20))

    # Botones para cada categoría
    for cat in listar_categorias():
        ctk.CTkButton(
            scroll,
            text=cat.nombre,
            fg_color="#3498DB",
            hover_color="#2980B9",
            anchor="w",
            command=lambda c=cat: _show_alimentos(c.id_categoria, c.nombre),
        ).pack(fill="x", padx=5, pady=3)

    # Botón Volver (solo llama al callback; la vista principal se encarga de ocultar esta pantalla)
    ctk.CTkButton(
        pantalla,
        text="Volver al Menú",
        command=volver_cb,
        fg_color="#27AE60",
        hover_color="#2ECC71",
        width=200,
    ).pack(pady=15)

    return pantalla
