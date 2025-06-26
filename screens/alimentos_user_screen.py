# screens/alimentos_user_screen.py

import customtkinter as ctk
from controllers.alimentos_controller import listar_alimentos, obtener_alimento


def crear_alimentos_user_screen(parent, volver_cb):
    """
    Pantalla de lista de alimentos (solo lectura) para usuarios.
    volver_cb(): callback que oculta esta pantalla y muestra el menú principal.
    """
    pantalla = ctk.CTkFrame(parent)
    pantalla.pack(expand=True, fill="both")

    # — Título —
    ctk.CTkLabel(
        pantalla,
        text="Lista de Alimentos",
        font=("Segoe UI", 22, "bold"),
        text_color="#ECF0F1",
    ).pack(pady=20)

    # — Lista scrollable —
    lista_frame = ctk.CTkScrollableFrame(pantalla, width=600, height=400)
    lista_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # 1) Obtenemos la lista desde el controller
    alimentos = listar_alimentos()
    if alimentos:
        for al in alimentos:
            btn = ctk.CTkButton(
                lista_frame,
                text=f"{al.nom_producto} ({al.categoria or '—'})",
                fg_color="#3498DB",
                hover_color="#2980B9",
                anchor="w",
                # 2) Llamamos al controller para detallar
                command=lambda pid=al.id_producto: _mostrar_detalles(pid),
            )
            btn.pack(fill="x", padx=5, pady=3)
    else:
        ctk.CTkLabel(
            lista_frame,
            text="No hay alimentos registrados.",
            font=("Segoe UI", 14),
        ).pack(pady=10)

    # — Botón Volver —
    ctk.CTkButton(
        pantalla,
        text="Volver al Menú",
        command=volver_cb,  # 3) Llamamos directamente al callback
        fg_color="#27AE60",
        hover_color="#2ECC71",
        width=200,
    ).pack(pady=15)

    return pantalla


def _mostrar_detalles(id_producto: int):
    """
    Muestra un CTkToplevel con todos los datos del alimento,
    usando obtener_alimento() del controller.
    """
    al = obtener_alimento(id_producto)
    if not al:
        return

    top = ctk.CTkToplevel()
    top.title(f"Detalles de {al.nom_producto}")
    top.geometry("450x350")

    form = ctk.CTkFrame(top)
    form.pack(padx=20, pady=20, fill="both", expand=True)

    campos = [
        ("Nombre", al.nom_producto),
        ("Categoría", al.categoria or "—"),
        ("Calorías", f"{al.calorias} kcal"),
        ("Proteína", f"{al.proteina} g"),
        ("Grasas", f"{al.grasas} g"),
        ("Carbohidratos", f"{al.carbohidratos} g"),
        ("Descripción", al.descripcion or "—"),
    ]

    for i, (etq, val) in enumerate(campos):
        ctk.CTkLabel(
            form, text=f"{etq}:", anchor="e", width=120, font=("Segoe UI", 12, "bold")
        ).grid(row=i, column=0, padx=(0, 10), pady=5, sticky="e")

        if etq == "Descripción":
            ctk.CTkLabel(
                form,
                text=val,
                anchor="w",
                justify="left",
                font=("Segoe UI", 12),
                wraplength=280,
            ).grid(row=i, column=1, padx=(0, 10), pady=5, sticky="w")
        else:
            ctk.CTkLabel(
                form,
                text=val,
                anchor="w",
                width=220,
                font=("Segoe UI", 12),
            ).grid(row=i, column=1, padx=(0, 10), pady=5, sticky="w")

    ctk.CTkButton(
        top,
        text="Cerrar",
        command=top.destroy,
        fg_color="#E74C3C",
        hover_color="#C0392B",
        width=100,
    ).pack(pady=(0, 20))
