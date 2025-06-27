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
    pantalla = ctk.CTkFrame(parent)
    pantalla.pack(expand=True, fill="both", padx=20, pady=20)

    ctk.CTkLabel(
        pantalla,
        text="Gestión de Categorías",
        font=("Segoe UI", 24, "bold"),
        justify="center",
    ).pack(pady=(0, 20))

    form = ctk.CTkFrame(pantalla, corner_radius=10)
    form.pack(fill="x", padx=20, pady=(0, 20))
    form.grid_columnconfigure(0, weight=1)
    form.grid_columnconfigure(1, weight=0)

    ctk.CTkLabel(form, text="Nombre:", anchor="w").grid(
        row=0, column=0, padx=(10, 5), pady=10, sticky="w"
    )
    entry_nombre = ctk.CTkEntry(form, placeholder_text="Nombre de categoría")
    entry_nombre.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="ew")

    def _agregar_categoria():
        nombre = entry_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Atención", "El nombre no puede estar vacío.")
            return
        try:
            crear_categoria(Categoria(id_categoria=0, nombre=nombre), rol_actual)
        except PermissionError as pe:
            messagebox.showerror("Permisos", str(pe))
        else:
            entry_nombre.delete(0, "end")
            refresh_list()

    ctk.CTkButton(
        form, text="Agregar", width=100, corner_radius=8, command=_agregar_categoria
    ).grid(row=0, column=2, padx=(0, 10), pady=10)

    lista_frame = ctk.CTkScrollableFrame(pantalla, corner_radius=10)
    lista_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))

    def _editar_categoria(cat: Categoria):
        top = ctk.CTkToplevel(pantalla)
        top.title("Editar Categoría")
        top.geometry("300x120")
        top.transient(pantalla)

        ent = ctk.CTkEntry(top, width=200)
        ent.insert(0, cat.nombre)
        ent.pack(pady=(20, 10))

        def _guardar():
            nuevo = ent.get().strip()
            if not nuevo:
                return
            try:
                actualizar_categoria(
                    Categoria(id_categoria=cat.id_categoria, nombre=nuevo), rol_actual
                )
            except PermissionError as pe:
                messagebox.showerror("Permisos", str(pe))
            else:
                top.destroy()
                refresh_list()

        ctk.CTkButton(
            top, text="Guardar", width=100, corner_radius=8, command=_guardar
        ).pack(pady=(0, 15))

    def _borrar_categoria(idc: int):
        if messagebox.askyesno("Confirmar", "¿Eliminar esta categoría?"):
            try:
                borrar_categoria(idc, rol_actual)
            except PermissionError as pe:
                messagebox.showerror("Permisos", str(pe))
            else:
                refresh_list()

    def refresh_list():
        cats = listar_categorias()
        print("DEBUG listar_categorias() ->", cats)

        for w in lista_frame.winfo_children():
            w.destroy()

        if not cats:
            ctk.CTkLabel(
                lista_frame,
                text="No hay categorías disponibles.",
                font=("Segoe UI", 14),
                anchor="center",
            ).pack(pady=20)
            return

        for cat in cats:
            row = ctk.CTkFrame(lista_frame, corner_radius=5)
            row.pack(fill="x", padx=10, pady=4)
            row.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(row, text=cat.nombre, font=("Segoe UI", 14), anchor="w").grid(
                row=0, column=0, sticky="ew", padx=(5, 0)
            )

            ctk.CTkButton(
                row,
                text="✏️",
                width=40,
                corner_radius=8,
                command=lambda c=cat: _editar_categoria(c),
            ).grid(row=0, column=1, padx=5)

            ctk.CTkButton(
                row,
                text="🗑️",
                width=40,
                corner_radius=8,
                fg_color="#E74C3C",
                hover_color="#C0392B",
                command=lambda idc=cat.id_categoria: _borrar_categoria(idc),
            ).grid(row=0, column=2, padx=5)

    refresh_list()

    ctk.CTkButton(
        pantalla, text="Volver al Menú", width=200, corner_radius=8, command=volver_cb
    ).pack(pady=(0, 10))

    return pantalla
