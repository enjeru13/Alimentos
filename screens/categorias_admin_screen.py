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
    pantalla = ctk.CTkFrame(parent, fg_color="transparent")
    pantalla.pack(expand=True, fill="both", padx=40, pady=40)

    header = ctk.CTkFrame(pantalla, corner_radius=8)
    header.pack(fill="x", pady=(20, 20), padx=20)
    header.grid_columnconfigure(0, weight=1)
    header.grid_columnconfigure(1, weight=0)

    title = ctk.CTkLabel(
        header,
        text="Gestión de Categorías",
        font=("Segoe UI", 24, "bold"),
    )
    title.grid(row=0, column=0, sticky="ew", pady=10)

    form = ctk.CTkFrame(
        pantalla, corner_radius=8, border_width=1, border_color="#CCCCCC"
    )
    form.pack(fill="x", padx=20, pady=(0, 30))
    form.grid_columnconfigure(0, weight=0)
    form.grid_columnconfigure(1, weight=1)
    form.grid_columnconfigure(2, weight=0)
    form.grid_columnconfigure(3, weight=0)

    ctk.CTkLabel(form, text="Nombre:", anchor="w").grid(
        row=0, column=0, padx=(10, 15), pady=10, sticky="w"
    )
    entry_nombre = ctk.CTkEntry(
        form, placeholder_text="Nombre de categoría", width=180, height=36
    )
    entry_nombre.grid(row=0, column=1, padx=(0, 20), pady=10, sticky="ew")

    btn_save = ctk.CTkButton(
        form,
        text="Agregar",
        width=120,
        height=36,
        corner_radius=8,
        fg_color="#4E81AC",
        hover_color="#3B6C91",
    )
    btn_save.grid(row=0, column=2, padx=(0, 10), pady=10)

    btn_cancel = ctk.CTkButton(
        form,
        text="Cancelar",
        width=120,
        height=36,
        corner_radius=8,
        fg_color="#E74C3C",
        hover_color="#C0392B",
    )
    btn_cancel.grid(row=0, column=3, padx=(0, 10), pady=10)
    btn_cancel.configure(state="disabled")

    estado = {"id": None}

    def _reset_form():
        estado["id"] = None
        entry_nombre.delete(0, "end")
        btn_save.configure(text="Agregar")
        btn_cancel.configure(state="disabled")

    def _on_save():
        nombre = entry_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Atención", "El nombre no puede quedar vacío.")
            return
        cat = Categoria(id_categoria=estado["id"] or 0, nombre=nombre)
        try:
            if estado["id"]:
                actualizar_categoria(cat, rol_actual)
            else:
                crear_categoria(cat, rol_actual)
        except PermissionError as pe:
            messagebox.showerror("Permisos", str(pe))
            return
        _reset_form()
        _populate_list()

    btn_save.configure(command=_on_save)
    btn_cancel.configure(command=_reset_form)

    lista_frame = ctk.CTkScrollableFrame(
        pantalla, corner_radius=8, border_width=1, border_color="#CCCCCC"
    )
    lista_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))

    def _populate_list():
        for w in lista_frame.winfo_children():
            w.destroy()

        cats = listar_categorias()
        if not cats:
            ctk.CTkLabel(
                lista_frame,
                text="No hay categorías.",
                font=("Segoe UI", 14),
                anchor="center",
            ).pack(pady=20)
            return

        for cat in cats:
            row = ctk.CTkFrame(lista_frame, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=6)
            row.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(row, text=cat.nombre, font=("Segoe UI", 14), anchor="w").grid(
                row=0, column=0, sticky="ew", padx=(5, 0)
            )

            ctk.CTkButton(
                row,
                text="✏️ Editar",
                width=100,
                height=36,
                corner_radius=8,
                fg_color="#4E81AC",
                hover_color="#3B6C91",
                command=lambda c=cat: _on_edit(c),
            ).grid(row=0, column=1, padx=8)

            ctk.CTkButton(
                row,
                text="🗑️ Eliminar",
                width=100,
                height=36,
                corner_radius=8,
                fg_color="#E74C3C",
                hover_color="#C0392B",
                command=lambda idc=cat.id_categoria: _on_delete(idc),
            ).grid(row=0, column=2, padx=8)

    def _on_edit(cat: Categoria):
        estado["id"] = cat.id_categoria
        entry_nombre.delete(0, "end")
        entry_nombre.insert(0, cat.nombre)
        btn_save.configure(text="Guardar")
        btn_cancel.configure(state="normal")

    def _on_delete(idc: int):
        if not messagebox.askyesno("Confirmar", "¿Eliminar esta categoría?"):
            return
        try:
            borrar_categoria(idc, rol_actual)
        except PermissionError as pe:
            messagebox.showerror("Permisos", str(pe))
        _populate_list()

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

    _reset_form()
    _populate_list()
    return pantalla
