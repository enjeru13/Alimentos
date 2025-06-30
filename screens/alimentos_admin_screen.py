import os
import shutil
from shutil import SameFileError
from datetime import datetime
from tkinter import filedialog, messagebox

import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image, ImageDraw

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
    pantalla = ctk.CTkFrame(parent, fg_color="transparent")
    pantalla.pack(expand=True, fill="both", padx=40, pady=40)

    placeholder = Image.new("RGBA", (100, 100), (240, 240, 240, 255))
    draw = ImageDraw.Draw(placeholder)
    draw.text((20, 40), "Sin imagen", fill="#AAAAAA")
    blank_img = CTkImage(
        light_image=placeholder, dark_image=placeholder, size=(100, 100)
    )

    header = ctk.CTkFrame(pantalla, corner_radius=8)
    header.pack(fill="x", pady=(20, 20), padx=20)
    header.grid_columnconfigure(0, weight=1)
    header.grid_columnconfigure(1, weight=0)

    title = ctk.CTkLabel(
        header,
        text="Gestión de Alimentos",
        font=("Segoe UI", 24, "bold"),
    )
    title.grid(row=0, column=0, sticky="ew", pady=10)

    form = ctk.CTkFrame(
        pantalla, corner_radius=8, border_width=1, border_color="#CCCCCC"
    )
    form.pack(fill="x", padx=20, pady=(0, 30))
    for i in range(4):
        form.grid_columnconfigure(i, weight=1, uniform="col")

    entry_nom = ctk.CTkEntry(form, placeholder_text="Nombre del producto", height=36)
    combo_cat = ctk.CTkComboBox(
        form, values=[c.nombre for c in listar_categorias()], height=36
    )
    entry_cal = ctk.CTkEntry(form, placeholder_text="Calorías (kcal)", height=36)
    entry_pro = ctk.CTkEntry(form, placeholder_text="Proteína (g)", height=36)
    entry_gra = ctk.CTkEntry(form, placeholder_text="Grasas (g)", height=36)
    entry_car = ctk.CTkEntry(form, placeholder_text="Carbohidratos (g)", height=36)
    entry_desc = ctk.CTkEntry(form, placeholder_text="Descripción", height=36)

    lbl_img = ctk.CTkLabel(form, image=blank_img, text="")
    lbl_img.image = blank_img

    btn_sel = ctk.CTkButton(
        form, text="Seleccionar Imagen", width=160, height=36, corner_radius=8
    )

    btn_save = ctk.CTkButton(
        form,
        text="Agregar",
        width=120,
        height=36,
        corner_radius=8,
        fg_color="#4E81AC",
        hover_color="#3B6C91",
    )
    btn_cancel = ctk.CTkButton(
        form,
        text="Cancelar",
        width=120,
        height=36,
        corner_radius=8,
        fg_color="#E74C3C",
        hover_color="#C0392B",
    )
    btn_cancel.configure(state="disabled")

    headers = ["Nombre:", "Categoría:", "Calorías:", "Proteína:"]
    for idx, txt in enumerate(headers):
        ctk.CTkLabel(form, text=txt, anchor="w").grid(
            row=0, column=idx, padx=5, pady=(10, 2), sticky="w"
        )

    entry_nom.grid(row=1, column=0, padx=5, pady=(0, 15), sticky="ew")
    combo_cat.grid(row=1, column=1, padx=5, pady=(0, 15), sticky="ew")
    entry_cal.grid(row=1, column=2, padx=5, pady=(0, 15), sticky="ew")
    entry_pro.grid(row=1, column=3, padx=5, pady=(0, 15), sticky="ew")

    subheaders = [
        ("Grasas:", 2, 0, 1),
        ("Carbohidratos:", 2, 1, 1),
        ("Descripción:", 2, 2, 2),
    ]
    for text, r, c, span in subheaders:
        ctk.CTkLabel(form, text=text, anchor="w").grid(
            row=r, column=c, columnspan=span, padx=5, pady=(0, 2), sticky="w"
        )

    entry_gra.grid(row=3, column=0, padx=5, pady=(0, 15), sticky="ew")
    entry_car.grid(row=3, column=1, padx=5, pady=(0, 15), sticky="ew")
    entry_desc.grid(row=3, column=2, columnspan=2, padx=5, pady=(0, 15), sticky="ew")

    lbl_img.grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky="w")
    btn_sel.grid(row=4, column=2, columnspan=2, padx=5, pady=10, sticky="w")

    btn_save.grid(row=5, column=2, padx=5, pady=(0, 10), sticky="ew")
    btn_cancel.grid(row=5, column=3, padx=5, pady=(0, 10), sticky="ew")

    imagen_path = {"ruta": None}
    editing = {"id": None}

    def _select_image():
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
            img.thumbnail((100, 100))
            icon = CTkImage(light_image=img, dark_image=img, size=(100, 100))
            lbl_img.configure(image=icon, text="")
            lbl_img.image = icon
        except:
            lbl_img.configure(image=blank_img, text="Imagen no disp.")

    btn_sel.configure(command=_select_image)

    def _reset_form():
        editing["id"] = None
        for w in (entry_nom, entry_cal, entry_pro, entry_gra, entry_car, entry_desc):
            w.delete(0, "end")
        combo_cat.set("Categoría")
        imagen_path["ruta"] = None
        lbl_img.configure(image=blank_img, text="")
        lbl_img.image = blank_img
        btn_save.configure(text="Agregar")
        btn_cancel.configure(state="disabled")

    def _save_or_update():
        try:
            al = Alimento(
                id_producto=editing["id"] or 0,
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
            if editing["id"]:
                actualizar_alimento(al, rol_actual)
            else:
                crear_alimento(al, rol_actual)
        except Exception as e:
            return messagebox.showerror("Error", str(e))
        _reset_form()
        _populate_list()

    btn_save.configure(command=_save_or_update)
    btn_cancel.configure(command=_reset_form)

    list_frame = ctk.CTkScrollableFrame(
        pantalla, corner_radius=8, border_width=1, border_color="#CCCCCC"
    )
    list_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))

    def _populate_list():
        combo_cat.configure(values=[c.nombre for c in listar_categorias()])
        for w in list_frame.winfo_children():
            w.destroy()

        for al in listar_alimentos():
            row = ctk.CTkFrame(list_frame, fg_color="transparent")
            row.pack(fill="x", pady=4, padx=10)
            row.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                row,
                text=f"{al.nom_producto} ({al.categoria})",
                font=("Segoe UI", 14),
                anchor="w",
            ).grid(row=0, column=0, sticky="ew")

            ctk.CTkButton(
                row,
                text="✏️ Editar",
                width=80,
                height=30,
                corner_radius=8,
                command=lambda a=al: _load_edit(a),
            ).grid(row=0, column=1, padx=5)

            ctk.CTkButton(
                row,
                text="🗑️ Eliminar",
                width=80,
                height=30,
                corner_radius=8,
                fg_color="#E74C3C",
                hover_color="#C0392B",
                command=lambda pid=al.id_producto: _delete(pid),
            ).grid(row=0, column=2, padx=5)

    def _load_edit(al: Alimento):
        lbl_img.configure(image=blank_img, text="")
        lbl_img.image = blank_img
        imagen_path["ruta"] = None

        editing["id"] = al.id_producto
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
            fld.insert(0, str(val or ""))

        entry_desc.delete(0, "end")
        entry_desc.insert(0, full.descripcion or "")

        if full.imagen_url:
            try:
                img = Image.open(full.imagen_url)
                img.thumbnail((100, 100))
                icon = CTkImage(light_image=img, dark_image=img, size=(100, 100))
                lbl_img.configure(image=icon, text="")
                lbl_img.image = icon
                imagen_path["ruta"] = full.imagen_url
            except:
                lbl_img.configure(image=blank_img, text="Error al cargar imagen")
        else:
            lbl_img.configure(image=blank_img, text="Sin imagen")
            lbl_img.image = blank_img

        btn_save.configure(text="Guardar")
        btn_cancel.configure(state="normal")

    def _delete(pid: int):
        try:
            borrar_alimento(pid, rol_actual)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        _populate_list()

    _populate_list()
    _reset_form()

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

    return pantalla
