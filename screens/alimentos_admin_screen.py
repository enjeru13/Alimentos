import os
import shutil
from shutil import SameFileError
from datetime import datetime
from tkinter import filedialog, messagebox

import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image

from models.alimento import Alimento
from controllers.alimentos_controller import (
    listar_alimentos,
    obtener_alimento,
    crear_alimento,
    actualizar_alimento,
    borrar_alimento,
)
from controllers.categorias_controller import listar_categorias

IMG_DIR = os.path.join("media", "images")


def crear_alimentos_admin_screen(parent, rol_actual, volver_cb):
    pantalla = ctk.CTkFrame(parent)
    pantalla.pack(expand=True, fill="both", padx=20, pady=20)

    ctk.CTkLabel(
        pantalla,
        text="Gestión de Alimentos",
        font=("Segoe UI", 22, "bold"),
        justify="center",
    ).pack(pady=(0, 20))

    form = ctk.CTkFrame(pantalla, corner_radius=10, fg_color=None)
    form.pack(fill="x", padx=20, pady=(0, 20))
    for i in range(4):
        form.grid_columnconfigure(i, weight=1, uniform="col")

    entry_nom = ctk.CTkEntry(form, placeholder_text="Nombre")
    combo_cat = ctk.CTkComboBox(
        form, values=[c.nombre for c in listar_categorias()], width=150
    )
    combo_cat.set("Categoría")
    entry_cal = ctk.CTkEntry(form, placeholder_text="Calorías")
    entry_pro = ctk.CTkEntry(form, placeholder_text="Proteína (g)")
    entry_gra = ctk.CTkEntry(form, placeholder_text="Grasas (g)")
    entry_car = ctk.CTkEntry(form, placeholder_text="Carbohidratos (g)")
    entry_desc = ctk.CTkEntry(form, placeholder_text="Descripción")

    lbl_img = ctk.CTkLabel(form, text="Sin imagen", width=100, height=80)
    btn_sel = ctk.CTkButton(form, text="Seleccionar Imagen", width=150)

    btn_guardar = ctk.CTkButton(form, text="Agregar", width=120)
    btn_cancelar = ctk.CTkButton(form, text="Cancelar", fg_color="#E74C3C", width=120)
    btn_cancelar.configure(state="disabled")

    ctk.CTkLabel(form, text="Nombre:", anchor="w").grid(
        row=0, column=0, padx=5, pady=(10, 2), sticky="w"
    )
    ctk.CTkLabel(form, text="Categoría:", anchor="w").grid(
        row=0, column=1, padx=5, pady=(10, 2), sticky="w"
    )
    ctk.CTkLabel(form, text="Calorías:", anchor="w").grid(
        row=0, column=2, padx=5, pady=(10, 2), sticky="w"
    )
    ctk.CTkLabel(form, text="Proteína (g):", anchor="w").grid(
        row=0, column=3, padx=5, pady=(10, 2), sticky="w"
    )

    entry_nom.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="ew")
    combo_cat.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="ew")
    entry_cal.grid(row=1, column=2, padx=5, pady=(0, 10), sticky="ew")
    entry_pro.grid(row=1, column=3, padx=5, pady=(0, 10), sticky="ew")

    ctk.CTkLabel(form, text="Grasas (g):", anchor="w").grid(
        row=2, column=0, padx=5, pady=(0, 2), sticky="w"
    )
    ctk.CTkLabel(form, text="Carbohidratos (g):", anchor="w").grid(
        row=2, column=1, padx=5, pady=(0, 2), sticky="w"
    )
    ctk.CTkLabel(form, text="Descripción:", anchor="w").grid(
        row=2, column=2, columnspan=2, padx=5, pady=(0, 2), sticky="w"
    )

    entry_gra.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="ew")
    entry_car.grid(row=3, column=1, padx=5, pady=(0, 10), sticky="ew")
    entry_desc.grid(row=3, column=2, columnspan=2, padx=5, pady=(0, 10), sticky="ew")

    lbl_img.grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky="w")
    btn_sel.grid(row=4, column=2, columnspan=2, padx=5, pady=10, sticky="w")

    btn_guardar.grid(row=5, column=2, padx=5, pady=10, sticky="ew")
    btn_cancelar.grid(row=5, column=3, padx=5, pady=10, sticky="ew")

    imagen_path = {"ruta": None}
    estado_edicion = {"id": None}

    def _seleccionar_imagen():
        file = filedialog.askopenfilename(
            filetypes=[("JPEG", "*.jpg;*.jpeg"), ("PNG", "*.png")]
        )
        if not file:
            return
        os.makedirs(IMG_DIR, exist_ok=True)
        dst = os.path.join(IMG_DIR, os.path.basename(file))
        try:
            shutil.copy(file, dst)
        except SameFileError:
            pass
        imagen_path["ruta"] = dst.replace("\\", "/")
        try:
            img = Image.open(dst)
            img.thumbnail((80, 80))
            icon = CTkImage(light_image=img, dark_image=img, size=(80, 80))
            lbl_img.configure(image=icon, text="")
            lbl_img.image = icon
        except:
            lbl_img.configure(text="Error al cargar imagen")

    btn_sel.configure(command=_seleccionar_imagen)

    def limpiar_form():
        estado_edicion["id"] = None
        for w in (entry_nom, entry_cal, entry_pro, entry_gra, entry_car, entry_desc):
            w.delete(0, "end")
        combo_cat.set("Categoría")
        imagen_path["ruta"] = None
        lbl_img.configure(image=None, text="Sin imagen")
        btn_guardar.configure(text="Agregar")
        btn_cancelar.configure(state="disabled")

    def guardar_o_editar():
        try:
            al = Alimento(
                id_producto=estado_edicion["id"] or 0,
                nom_producto=entry_nom.get().strip(),
                categoria=combo_cat.get().strip(),
                calorias=float(entry_cal.get() or 0),
                proteina=float(entry_pro.get() or 0),
                grasas=float(entry_gra.get() or 0),
                carbohidratos=float(entry_car.get() or 0),
                descripcion=entry_desc.get().strip(),
                imagen_url=imagen_path["ruta"],
                fecha_registro=datetime.now(),
            )
            if estado_edicion["id"]:
                actualizar_alimento(al, rol_actual)
            else:
                crear_alimento(al, rol_actual)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        limpiar_form()
        refrescar_lista()

    def cargar_edicion(al: Alimento):
        estado_edicion["id"] = al.id_producto
        entry_nom.delete(0, "end")
        entry_nom.insert(0, al.nom_producto)
        combo_cat.set(al.categoria or "Categoría")
        full = obtener_alimento(al.id_producto)
        for fld, val in (
            (entry_cal, full.calorias),
            (entry_pro, full.proteina),
            (entry_gra, full.grasas),
            (entry_car, full.carbohidratos),
        ):
            fld.delete(0, "end")
            fld.insert(0, str(val))
        entry_desc.delete(0, "end")
        entry_desc.insert(0, full.descripcion)
        if full.imagen_url:
            try:
                img = Image.open(full.imagen_url)
                img.thumbnail((80, 80))
                icon = CTkImage(light_image=img, dark_image=img, size=(80, 80))
                lbl_img.configure(image=icon, text="")
                lbl_img.image = icon
                imagen_path["ruta"] = full.imagen_url
            except:
                pass
        btn_guardar.configure(text="Guardar")
        btn_cancelar.configure(state="normal")

    def borrar(idp: int):
        try:
            borrar_alimento(idp, rol_actual)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        refrescar_lista()

    btn_guardar.configure(command=guardar_o_editar)
    btn_cancelar.configure(command=limpiar_form)

    lista_frame = ctk.CTkScrollableFrame(pantalla, corner_radius=10)
    lista_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))

    def refrescar_lista():
        combo_cat.configure(values=[c.nombre for c in listar_categorias()])
        for w in lista_frame.winfo_children():
            w.destroy()
        for al in listar_alimentos():
            row = ctk.CTkFrame(lista_frame, fg_color=None)
            row.grid_columnconfigure(0, weight=1)
            row.pack(fill="x", pady=4, padx=10)

            ctk.CTkLabel(
                row,
                text=f"{al.nom_producto} ({al.categoria})",
                font=("Segoe UI", 14),
                anchor="w",
            ).grid(row=0, column=0, sticky="ew")

            ctk.CTkButton(
                row, text="✏️", width=40, command=lambda a=al: cargar_edicion(a)
            ).grid(row=0, column=1, padx=5)

            ctk.CTkButton(
                row,
                text="🗑️",
                width=40,
                fg_color="#E74C3C",
                hover_color="#C0392B",
                command=lambda pid=al.id_producto: borrar(pid),
            ).grid(row=0, column=2, padx=5)

    refrescar_lista()

    ctk.CTkButton(
        pantalla, text="Volver al Menú", width=200, corner_radius=8, command=volver_cb
    ).pack(pady=(0, 10))

    return pantalla
