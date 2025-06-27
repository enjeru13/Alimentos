import customtkinter as ctk
from tkinter import messagebox

from models.categoria import Categoria
from controllers.categorias_controller import (
    listar_categorias,
    crear_categoria,
    actualizar_categoria,
    borrar_categoria,
)


def crear_categorias_admin_screen(parent, rol_actual, volver_cb):
    """
    Pantalla CRUD de categorías para admin.
    Args:
      parent: contenedor CTk
      rol_actual: 'admin' o 'user'
      volver_cb: callback para volver al menú principal
    """
    pantalla = ctk.CTkFrame(parent)
    pantalla.pack(expand=True, fill="both")

    # — Título —
    ctk.CTkLabel(
        pantalla,
        text="Gestión de Categorías",
        font=("Segoe UI", 22, "bold"),
    ).pack(pady=20)

    # — Lista scrollable —
    lista_frame = ctk.CTkScrollableFrame(pantalla, width=400, height=300)
    lista_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # — Formulario —
    form = ctk.CTkFrame(pantalla)
    form.pack(pady=10)
    entry_nombre = ctk.CTkEntry(form, placeholder_text="Nombre categoría", width=200)
    entry_nombre.grid(row=0, column=0, padx=5)
    ctk.CTkButton(
        form,
        text="Agregar",
        fg_color="#2980B9",
        hover_color="#3498DB",
        width=100,
        command=lambda: _agregar_categoria(),
    ).grid(row=0, column=1, padx=5)

    def refresh_list():
        """Recarga el listado de categorías."""
        for w in lista_frame.winfo_children():
            w.destroy()

        for cat in listar_categorias():
            row = ctk.CTkFrame(lista_frame, fg_color="transparent")
            row.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                row,
                text=cat.nombre,
                font=("Segoe UI", 14),
                text_color="#ECF0F1",
                anchor="w",
            ).grid(row=0, column=0, sticky="w", padx=(5, 0))

            ctk.CTkButton(
                row,
                text="✏️",
                width=40,
                command=lambda c=cat: _editar_categoria(c),
            ).grid(row=0, column=1, padx=5)

            ctk.CTkButton(
                row,
                text="🗑️",
                width=40,
                fg_color="#E74C3C",
                hover_color="#C0392B",
                command=lambda idc=cat.id_categoria: _borrar_categoria(idc),
            ).grid(row=0, column=2, padx=5)

            row.pack(fill="x", pady=2, padx=5)

    def _agregar_categoria():
        """Crea una nueva categoría (solo admin)."""
        nombre = entry_nombre.get().strip()
        if not nombre:
            return

        try:
            crear_categoria(Categoria(id_categoria=0, nombre=nombre), rol_actual)
        except PermissionError as pe:
            messagebox.showerror("Permisos", str(pe))
            return

        entry_nombre.delete(0, "end")
        refresh_list()

    def _editar_categoria(cat: Categoria):
        """Abre Toplevel para renombrar categoría (solo admin)."""
        top = ctk.CTkToplevel(pantalla)
        top.title("Editar Categoría")
        top.geometry("300x120")

        ent = ctk.CTkEntry(top, width=200)
        ent.insert(0, cat.nombre)
        ent.pack(pady=10)

        def guardar_y_cerrar():
            nuevo = ent.get().strip()
            if not nuevo:
                return
            try:
                actualizar_categoria(
                    Categoria(id_categoria=cat.id_categoria, nombre=nuevo), rol_actual
                )
            except PermissionError as pe:
                messagebox.showerror("Permisos", str(pe))
                return

            top.destroy()
            refresh_list()

        ctk.CTkButton(
            top,
            text="Guardar",
            fg_color="#2980B9",
            hover_color="#3498DB",
            width=100,
            command=guardar_y_cerrar,
        ).pack(pady=5)

    def _borrar_categoria(idc: int):
        """Elimina la categoría (solo admin)."""
        try:
            borrar_categoria(idc, rol_actual)
        except PermissionError as pe:
            messagebox.showerror("Permisos", str(pe))
            return
        refresh_list()

    # Inicializamos listado
    refresh_list()

    # — Volver —
    ctk.CTkButton(
        pantalla,
        text="Volver al Menú",
        command=volver_cb,
        fg_color="#27AE60",
        hover_color="#2ECC71",
        width=200,
    ).pack(pady=15)

    return pantalla
