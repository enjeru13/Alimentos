# screens/main_screen.py

import customtkinter as ctk

from controllers.alimentos_controller import buscar_alimentos, obtener_alimento
from screens.alimentos_user_screen import crear_alimentos_user_screen
from screens.alimentos_admin_screen import crear_alimentos_admin_screen
from screens.categorias_user_screen import crear_categorias_user_screen
from screens.categorias_admin_screen import crear_categorias_admin_screen


def _clear_and_show_frame(parent, frame):
    """
    Oculta todos los widgets de 'parent' y muestra únicamente 'frame'.
    (Reemplaza la función anterior mostrar_pantalla para evitar colisiones de nombre.)
    """
    for w in parent.winfo_children():
        w.pack_forget()
    frame.pack(expand=True, fill="both")


def crear_main_screen(parent, usuario_actual, rol_actual, mostrar_perfil_cb):
    """
    Construye la ventana principal:
      – Menú lateral con botones de navegación.
      – Área de búsqueda y detalle de alimentos.
    Todo el acceso a datos se hace a través de los controllers.
    """
    pantalla = ctk.CTkFrame(parent)
    pantalla.pack(expand=True, fill="both")

    # ── Barra lateral ───────────────────────────────────────────────────────
    sidebar = ctk.CTkFrame(pantalla, width=200, corner_radius=10)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    ctk.CTkLabel(
        sidebar,
        text=f"Bienvenido, {usuario_actual}",
        font=("Segoe UI", 16, "bold"),
        text_color="#ECF0F1",
    ).pack(pady=(20, 10))

    # Botón "Inicio" vuelve a esta misma pantalla
    ctk.CTkButton(
        sidebar,
        text="Inicio",
        width=200,
        command=lambda: _clear_and_show_frame(parent, pantalla),
    ).pack(pady=5)

    # Botón "Alimentos" elige versión admin o user
    ctk.CTkButton(
        sidebar,
        text="Alimentos",
        width=200,
        command=lambda: _clear_and_show_frame(
            parent,
            (
                crear_alimentos_admin_screen
                if rol_actual == "admin"
                else crear_alimentos_user_screen
            )(
                parent,
                lambda: _clear_and_show_frame(
                    parent,
                    crear_main_screen(
                        parent, usuario_actual, rol_actual, mostrar_perfil_cb
                    ),
                ),
            ),
        ),
    ).pack(pady=5)

    # Botón "Categorías" idem
    ctk.CTkButton(
        sidebar,
        text="Categorías",
        width=200,
        command=lambda: _clear_and_show_frame(
            parent,
            (
                crear_categorias_admin_screen
                if rol_actual == "admin"
                else crear_categorias_user_screen
            )(
                parent,
                lambda: _clear_and_show_frame(
                    parent,
                    crear_main_screen(
                        parent, usuario_actual, rol_actual, mostrar_perfil_cb
                    ),
                ),
            ),
        ),
    ).pack(pady=5)

    # Botón Perfil
    ctk.CTkButton(
        sidebar, text="Ver Perfil", width=200, command=mostrar_perfil_cb
    ).pack(pady=10)

    # ── Área principal ───────────────────────────────────────────────────────
    body = ctk.CTkFrame(pantalla)
    body.pack(expand=True, fill="both", padx=10, pady=10)

    # Búsqueda
    search_frame = ctk.CTkFrame(body)
    search_frame.pack(fill="x", pady=(0, 10))
    ctk.CTkLabel(search_frame, text="Buscar Alimento:", font=("Segoe UI", 12)).pack(
        side="left", padx=10
    )
    entry = ctk.CTkEntry(search_frame, font=("Segoe UI", 12), width=300)
    entry.pack(side="left", padx=5, fill="x", expand=True)
    ctk.CTkButton(search_frame, text="Buscar", command=lambda: _buscar()).pack(
        side="left", padx=10
    )

    # Resultados
    resultados_frame = ctk.CTkScrollableFrame(body, width=400, height=200)
    resultados_frame.pack(pady=5, padx=10, fill="both", expand=True)

    # Detalles
    detalles = ctk.CTkTextbox(body, font=("Segoe UI", 12), width=400, height=150)
    detalles.pack(pady=(10, 5), padx=10, fill="x")
    detalles.configure(state="disabled")

    def _buscar():
        # Limpia resultados anteriores
        for w in resultados_frame.winfo_children():
            w.destroy()

        # Utiliza buscar_alimentos del controller (no DB directa)
        resultados = buscar_alimentos(entry.get())
        if not resultados:
            ctk.CTkLabel(
                resultados_frame, text="No hay resultados.", font=("Segoe UI", 12)
            ).pack(pady=10)
            return

        for al in resultados:
            btn = ctk.CTkButton(
                resultados_frame,
                text=f"{al.nom_producto} ({al.categoria or '—'})",
                fg_color="#3498DB",
                hover_color="#2980B9",
                anchor="w",
                command=lambda pid=al.id_producto: _mostrar_detalle(pid),
            )
            btn.pack(fill="x", padx=5, pady=2)

    def _mostrar_detalle(id_prod: int):
        # Obtiene datos con obtener_alimento del controller
        al = obtener_alimento(id_prod)
        detalles.configure(state="normal")
        detalles.delete("1.0", "end")
        if al:
            detalles.insert(
                "end",
                f"Nombre:       {al.nom_producto}\n"
                f"Categoría:    {al.categoria or '—'}\n"
                f"Calorías:     {al.calorias} kcal\n"
                f"Proteína:     {al.proteina} g\n"
                f"Grasas:       {al.grasas} g\n"
                f"Carbohidratos:{al.carbohidratos} g\n"
                f"Descripción:\n{al.descripcion}\n",
            )
        else:
            detalles.insert("end", "No se pudieron obtener los detalles.\n")
        detalles.configure(state="disabled")

    return pantalla
