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
    pantalla.pack(expand=True, fill="both")

    ctk.CTkLabel(
        pantalla,
        text="Gestión de Alimentos (Admin)",
        font=("Segoe UI", 22, "bold"),
    ).pack(pady=15)

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
    btn_cancelar = ctk.CTkButton(form, text="Cancelar", fg_color="#E74C3C", width=120)
    btn_cancelar.configure(state="disabled")

    entry_nom.grid(row=0, column=0, padx=5, pady=5)
    combo_cat.grid(row=0, column=1, padx=5, pady=5)
    entry_cal.grid(row=1, column=0, padx=5, pady=5)
    entry_pro.grid(row=1, column=1, padx=5, pady=5)
    entry_gra.grid(row=1, column=2, padx=5, pady=5)
    entry_car.grid(row=1, column=3, padx=5, pady=5)
    entry_desc.grid(row=2, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
    btn_guardar.grid(row=2, column=3, padx=5, pady=5)
    btn_cancelar.grid(row=2, column=4, padx=5, pady=5)

    lbl_img_preview = ctk.CTkLabel(form, text="Sin imagen", width=100)
    lbl_img_preview.grid(row=3, column=0, columnspan=2, pady=5, sticky="w")

    imagen_path = {"ruta": None}

    def _seleccionar_imagen():
        file = filedialog.askopenfilename(
            filetypes=[("JPEG", "*.jpg;*.jpeg"), ("PNG", "*.png")]
        )
        if not file:
            return

        os.makedirs(IMG_DIR, exist_ok=True)
        src = os.path.abspath(file)
        dst = os.path.abspath(os.path.join(IMG_DIR, os.path.basename(file)))

        if src != dst:
            try:
                shutil.copy(src, dst)
            except SameFileError:
                pass

        imagen_path["ruta"] = dst.replace("\\", "/")

        try:
            pil = Image.open(dst)
            pil.thumbnail((80, 80))
            icon = CTkImage(light_image=pil, dark_image=pil, size=(80, 80))
            lbl_img_preview.configure(image=icon, text="")
            lbl_img_preview.image = icon
        except:
            lbl_img_preview.configure(text="Error al cargar imagen")

    btn_sel = ctk.CTkButton(
        form,
        text="Seleccionar Imagen",
        width=150,
        command=_seleccionar_imagen,
    )
    btn_sel.grid(row=3, column=2, padx=5, pady=5)

    estado_edicion = {"id": None}

    def limpiar_form():
        estado_edicion["id"] = None
        entry_nom.delete(0, "end")
        combo_cat.set("Categoría")
        entry_cal.delete(0, "end")
        entry_pro.delete(0, "end")
        entry_gra.delete(0, "end")
        entry_car.delete(0, "end")
        entry_desc.delete(0, "end")
        imagen_path["ruta"] = None
        lbl_img_preview.configure(image=None, text="Sin imagen")
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
        except PermissionError as pe:
            messagebox.showerror("Permisos", str(pe))
            return
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
        entry_cal.delete(0, "end")
        entry_cal.insert(0, str(full.calorias))
        entry_pro.delete(0, "end")
        entry_pro.insert(0, str(full.proteina))
        entry_gra.delete(0, "end")
        entry_gra.insert(0, str(full.grasas))
        entry_car.delete(0, "end")
        entry_car.insert(0, str(full.carbohidratos))
        entry_desc.delete(0, "end")
        entry_desc.insert(0, full.descripcion)

        if full.imagen_url:
            try:
                pil = Image.open(full.imagen_url)
                pil.thumbnail((80, 80))
                icon = CTkImage(light_image=pil, dark_image=pil, size=(80, 80))
                lbl_img_preview.configure(image=icon, text="")
                lbl_img_preview.image = icon
                imagen_path["ruta"] = full.imagen_url
            except:
                pass

        btn_guardar.configure(text="Guardar")
        btn_cancelar.configure(state="normal")

    def borrar(idp: int):
        try:
            borrar_alimento(idp, rol_actual)
        except PermissionError as pe:
            messagebox.showerror("Permisos", str(pe))
            return
        refrescar_lista()

    def mostrar_detalle(idp: int):
        al = obtener_alimento(idp)
        if not al:
            messagebox.showerror("Error", "No se pudieron obtener los detalles.")
            return

        top = ctk.CTkToplevel(pantalla)
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

    btn_guardar.configure(command=guardar_o_editar)
    btn_cancelar.configure(command=limpiar_form)

    lista_frame = ctk.CTkScrollableFrame(pantalla, width=600, height=300)
    lista_frame.pack(padx=20, pady=10, fill="both", expand=True)

    def refrescar_lista():
        for w in lista_frame.winfo_children():
            w.destroy()
        combo_cat.configure(values=[c.nombre for c in listar_categorias()])

        for al in listar_alimentos():
            row = ctk.CTkFrame(lista_frame, fg_color="transparent")
            row.grid_columnconfigure(0, weight=1)

            ctk.CTkButton(
                row,
                text=f"{al.nom_producto} ({al.categoria})",
                fg_color="transparent",
                hover_color="#2980B9",
                anchor="w",
                command=lambda pid=al.id_producto: mostrar_detalle(pid),
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

            row.pack(fill="x", pady=2, padx=10)

    refrescar_lista()

    ctk.CTkButton(
        pantalla,
        text="Volver al Menú",
        command=volver_cb,
        fg_color="#27AE60",
        hover_color="#2ECC71",
        width=200,
    ).pack(pady=10)

    return pantalla
