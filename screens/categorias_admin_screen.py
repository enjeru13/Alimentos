# screens/categorias_admin_screen.py

import customtkinter as ctk
from controllers.categorias_controller import (
    listar_categorias,
    crear_categoria,
    actualizar_categoria,
    borrar_categoria,
)
from models.categoria import Categoria


def crear_categorias_admin_screen(parent, volver_cb):
    """
    Pantalla de CRUD de categorías para admin.
    volver_cb(): callback que oculta esta pantalla y muestra el menú principal.
    """
    pantalla = ctk.CTkFrame(parent)
    pantalla.pack(expand=True, fill="both")

    # — Título —
    ctk.CTkLabel(
        pantalla,
        text="Gestión de Categorías",
        font=("Segoe UI", 22, "bold"),
        text_color="#ECF0F1",
    ).pack(pady=20)

    # — Lista scrollable de categorías —
    lista_frame = ctk.CTkScrollableFrame(pantalla, width=400, height=300)
    lista_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # — Formulario de nueva categoría —
    form = ctk.CTkFrame(pantalla)
    form.pack(pady=10)
    entry_nombre = ctk.CTkEntry(form, placeholder_text="Nombre categoría", width=200)
    entry_nombre.grid(row=0, column=0, padx=5)
    ctk.CTkButton(
        form,
        text="Agregar",
        command=lambda: _agregar_categoria(entry_nombre, refresh_list),
        fg_color="#2980B9",
        hover_color="#3498DB",
        width=100,
    ).grid(row=0, column=1, padx=5)

    def refresh_list():
        """Recarga la lista de categorías desde el controller."""
        for w in lista_frame.winfo_children():
            w.destroy()

        for cat in listar_categorias():
            row = ctk.CTkFrame(lista_frame, fg_color="transparent")
            row.grid_columnconfigure(0, weight=1)

            # Nombre
            ctk.CTkLabel(
                row,
                text=cat.nombre,
                font=("Segoe UI", 14),
                text_color="#ECF0F1",
                anchor="w",
            ).grid(row=0, column=0, sticky="w", padx=(5, 0))

            # Editar
            ctk.CTkButton(
                row,
                text="✏️",
                width=40,
                command=lambda c=cat: _editar_categoria(c, refresh_list),
            ).grid(row=0, column=1, padx=5)

            # Borrar
            ctk.CTkButton(
                row,
                text="🗑️",
                width=40,
                fg_color="#E74C3C",
                hover_color="#C0392B",
                command=lambda idc=cat.id_categoria: _borrar_categoria(
                    idc, refresh_list
                ),
            ).grid(row=0, column=2, padx=5)

            row.pack(fill="x", pady=2, padx=5)

    def _agregar_categoria(entry, refrescar):
        """Lee el nombre, crea el model y llama al controller."""
        nombre = entry.get().strip()
        if not nombre:
            return
        crear_categoria(Categoria(id_categoria=0, nombre=nombre))
        entry.delete(0, "end")
        refrescar()

    def _editar_categoria(cat: Categoria, refrescar):
        """Abre un Toplevel para cambiar el nombre, luego actualiza."""
        top = ctk.CTkToplevel(pantalla)
        top.title("Editar Categoría")
        top.geometry("300x120")

        ent = ctk.CTkEntry(top, width=200)
        ent.insert(0, cat.nombre)
        ent.pack(pady=10)

        def _guardar():
            nuevo = ent.get().strip()
            if nuevo:
                actualizar_categoria(
                    Categoria(id_categoria=cat.id_categoria, nombre=nuevo)
                )
            top.destroy()
            refrescar()

        ctk.CTkButton(
            top,
            text="Guardar",
            command=_guardar,
            fg_color="#2980B9",
            hover_color="#3498DB",
            width=100,
        ).pack(pady=5)

    def _borrar_categoria(id_categoria: int, refrescar):
        """Llama al controller para eliminar y recarga la lista."""
        borrar_categoria(id_categoria)
        refrescar()

    # Inicializar listado
    refresh_list()

    # — Botón Volver —
    ctk.CTkButton(
        pantalla,
        text="Volver al Menú",
        command=volver_cb,  # sólo llama al callback; el main oculta esta pantalla
        fg_color="#27AE60",
        hover_color="#2ECC71",
        width=200,
    ).pack(pady=15)

    return pantalla
