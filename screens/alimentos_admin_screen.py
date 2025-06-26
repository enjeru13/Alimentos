# screens/alimentos_admin_screen.py

import customtkinter as ctk
from datetime import datetime

from models.alimento import Alimento
from controllers.alimentos_controller import (
    listar_alimentos,
    obtener_alimento,
    crear_alimento,
    actualizar_alimento,
    borrar_alimento,
)
from controllers.categorias_controller import listar_categorias


def crear_alimentos_admin_screen(parent, volver_cb):
    """
    Pantalla de CRUD de alimentos para admin.
    volver_cb(): callback que oculta esta pantalla y muestra el menú principal.
    """
    pantalla = ctk.CTkFrame(parent)
    pantalla.pack(expand=True, fill="both")

    # ── TÍTULO ──────────────────────────────────────────────────────────────
    ctk.CTkLabel(
        pantalla,
        text="Gestión de Alimentos (Admin)",
        font=("Segoe UI", 22, "bold"),
        text_color="#ECF0F1",
    ).pack(pady=15)

    # ── FORMULARIO CRUD ────────────────────────────────────────────────────
    form = ctk.CTkFrame(pantalla)
    form.pack(pady=10, padx=20, fill="x")

    entry_nom = ctk.CTkEntry(form, placeholder_text="Nombre", width=200)
    combo_cat = ctk.CTkComboBox(
        form, values=[c.nombre for c in listar_categorias()], width=150
    )
    combo_cat.set("Categoría")
    entry_cal = ctk.CTkEntry(form, placeholder_text="Calorías", width=80)
    entry_pro = ctk.CTkEntry(form, placeholder_text="Proteína (g)", width=80)
    entry_gra = ctk.CTkEntry(form, placeholder_text="Grasas (g)", width=80)
    entry_car = ctk.CTkEntry(form, placeholder_text="Carbohidratos (g)", width=80)
    entry_desc = ctk.CTkEntry(form, placeholder_text="Descripción", width=300)

    btn_guardar = ctk.CTkButton(form, text="Agregar", width=120)
    btn_cancel = ctk.CTkButton(form, text="Cancelar", width=120, fg_color="#E74C3C")
    btn_cancel.configure(state="disabled")

    # Grid layout
    entry_nom.grid(row=0, column=0, padx=5, pady=5)
    combo_cat.grid(row=0, column=1, padx=5, pady=5)
    entry_cal.grid(row=1, column=0, padx=5, pady=5)
    entry_pro.grid(row=1, column=1, padx=5, pady=5)
    entry_gra.grid(row=1, column=2, padx=5, pady=5)
    entry_car.grid(row=1, column=3, padx=5, pady=5)
    entry_desc.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
    btn_guardar.grid(row=2, column=3, padx=5, pady=5)
    btn_cancel.grid(row=2, column=4, padx=5, pady=5)

    # Estado de edición
    estado_edicion = {"id": None}

    def limpiar_form():
        """Resetea el formulario a modo 'Agregar'."""
        estado_edicion["id"] = None
        entry_nom.delete(0, "end")
        combo_cat.set("Categoría")
        entry_cal.delete(0, "end")
        entry_pro.delete(0, "end")
        entry_gra.delete(0, "end")
        entry_car.delete(0, "end")
        entry_desc.delete(0, "end")
        btn_guardar.configure(text="Agregar")
        btn_cancel.configure(state="disabled")

    def guardar_o_editar():
        """Llama al controller para crear o actualizar según el estado."""
        nom = entry_nom.get().strip()
        cat = combo_cat.get().strip()
        cal = float(entry_cal.get() or 0)
        pro = float(entry_pro.get() or 0)
        gra = float(entry_gra.get() or 0)
        car = float(entry_car.get() or 0)
        des = entry_desc.get().strip()

        # Construye el dataclass Alimento
        al = Alimento(
            id_producto=estado_edicion["id"] or 0,
            nom_producto=nom,
            categoria=cat,
            calorias=cal,
            proteina=pro,
            grasas=gra,
            carbohidratos=car,
            descripcion=des,
            fecha_registro=datetime.now(),  # opcional: captura timestamp
        )

        if estado_edicion["id"]:
            actualizar_alimento(al)
        else:
            crear_alimento(al)

        limpiar_form()
        refrescar_lista()

    def cargar_edicion(al: Alimento):
        """
        Carga datos en el form para edición.
        """
        estado_edicion["id"] = al.id_producto
        entry_nom.delete(0, "end")
        entry_nom.insert(0, al.nom_producto)
        combo_cat.set(al.categoria or "Categoría")

        # Carga macros y descripción
        full = obtener_alimento(al.id_producto)
        entry_cal.delete(0, "end")
        entry_cal.insert(0, full.calorias)
        entry_pro.delete(0, "end")
        entry_pro.insert(0, full.proteina)
        entry_gra.delete(0, "end")
        entry_gra.insert(0, full.grasas)
        entry_car.delete(0, "end")
        entry_car.insert(0, full.carbohidratos)
        entry_desc.delete(0, "end")
        entry_desc.insert(0, full.descripcion)

        btn_guardar.configure(text="Guardar")
        btn_cancel.configure(state="normal")

    def borrar(pid: int):
        """Elimina un alimento y refresca la lista."""
        borrar_alimento(pid)
        refrescar_lista()

    def mostrar_detalle(pid: int):
        """
        Muestra un CTkToplevel con los datos del alimento,
        usando obtener_alimento del controller.
        """
        al = obtener_alimento(pid)
        if not al:
            return

        top = ctk.CTkToplevel()
        top.title(al.nom_producto)
        top.geometry("450x350")

        frm = ctk.CTkFrame(top)
        frm.pack(padx=20, pady=20, fill="both", expand=True)

        info = (
            f"Nombre:       {al.nom_producto}\n"
            f"Categoría:    {al.categoria}\n"
            f"Calorías:     {al.calorias} kcal\n"
            f"Proteína:     {al.proteina} g\n"
            f"Grasas:       {al.grasas} g\n"
            f"Carbohidratos:{al.carbohidratos} g\n"
            f"Descripción:\n{al.descripcion}\n"
        )
        txt = ctk.CTkTextbox(frm, font=("Segoe UI", 12), wrap="word")
        txt.insert("0.0", info)
        txt.configure(state="disabled")
        txt.pack(fill="both", expand=True, pady=(0, 20))

        ctk.CTkButton(
            top,
            text="Cerrar",
            command=top.destroy,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            width=100,
        ).pack(pady=(0, 10))

    # Vinculaciones de botones
    btn_guardar.configure(command=guardar_o_editar)
    btn_cancel.configure(command=limpiar_form)

    # ── LISTA CON CRUD ───────────────────────────────────────────────────────
    lista_frame = ctk.CTkScrollableFrame(pantalla, width=600, height=300)
    lista_frame.pack(padx=20, pady=10, fill="both", expand=True)

    def refrescar_lista():
        """Refresca el listado de alimentos y los botones de acción."""
        for w in lista_frame.winfo_children():
            w.destroy()

        # Actualiza combo de categorías
        combo_cat.configure(values=[c.nombre for c in listar_categorias()])

        for al in listar_alimentos():
            row = ctk.CTkFrame(lista_frame, fg_color="transparent")
            row.grid_columnconfigure(0, weight=1)

            ctk.CTkButton(
                row,
                text=f"{al.nom_producto} ({al.categoria})",
                fg_color="transparent",
                text_color="#ECF0F1",
                hover_color="#2980B9",
                anchor="w",
                command=lambda pid=al.id_producto: mostrar_detalle(pid),
            ).grid(row=0, column=0, sticky="ew")

            ctk.CTkButton(
                row,
                text="✏️",
                width=40,
                command=lambda a=al: cargar_edicion(a),
            ).grid(row=0, column=1, padx=5)

            ctk.CTkButton(
                row,
                text="🗑️",
                width=40,
                fg_color="#E74C3C",
                command=lambda pid=al.id_producto: borrar(pid),
            ).grid(row=0, column=2, padx=5)

            row.pack(fill="x", pady=2, padx=10)

    refrescar_lista()

    # ── BOTÓN VOLVER ────────────────────────────────────────────────────────
    # Ahora invoca solo el callback; el main se encarga de ocultar esta pantalla.
    ctk.CTkButton(
        pantalla,
        text="Volver al Menú",
        command=volver_cb,
        fg_color="#27AE60",
        hover_color="#2ECC71",
        width=200,
    ).pack(pady=10)

    return pantalla
