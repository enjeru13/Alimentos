import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import messagebox
from PIL import Image, ImageDraw

from controllers.alimentos_controller import listar_alimentos, obtener_alimento


def crear_alimentos_user_screen(parent, volver_cb):
    pantalla = ctk.CTkFrame(parent, fg_color="transparent")
    pantalla.pack(expand=True, fill="both", padx=40, pady=40)

    header = ctk.CTkFrame(pantalla, corner_radius=8)
    header.pack(fill="x", pady=(20, 0), padx=20)

    title_lbl = ctk.CTkLabel(
        header, text="Catálogo de Alimentos", font=("Segoe UI", 24, "bold")
    )
    title_lbl.pack(expand=True, pady=10)

    content = ctk.CTkFrame(pantalla, corner_radius=8)
    content.pack(expand=True, fill="both", padx=20, pady=(20, 20))

    list_frame = ctk.CTkScrollableFrame(content, corner_radius=8, border_width=1)
    list_frame.pack(side="left", fill="y", pady=10, padx=(20, 20))
    list_frame.configure(width=250)

    detail_frame = ctk.CTkFrame(
        content,
        corner_radius=8,
        border_width=1,
    )
    detail_frame.pack(side="right", expand=True, fill="both", pady=10, padx=(20, 20))

    blank = Image.new("RGBA", (200, 200), (240, 240, 240, 255))
    draw = ImageDraw.Draw(blank)
    draw.text((60, 90), "No Img", fill="#AAAAAA")
    blank_img = CTkImage(light_image=blank, dark_image=blank, size=(200, 200))

    img_label = ctk.CTkLabel(detail_frame, image=blank_img, text="")
    img_label.image = blank_img
    img_label.pack(pady=(20, 10))

    text_label = ctk.CTkLabel(
        detail_frame,
        text="Selecciona un alimento para ver detalles",
        font=("Segoe UI", 14),
        wraplength=400,
        justify="left",
    )
    text_label.pack(fill="both", expand=True, padx=20, pady=(20, 20))

    def _clear_detail():
        img_label.configure(image=blank_img, text="")
        text_label.configure(text="Selecciona un alimento para ver detalles")

    def _mostrar_detalles(pid):
        al = obtener_alimento(pid)
        if not al:
            return messagebox.showerror("Error", "No se pudieron obtener los detalles.")

        if al.imagen_url:
            try:
                pil = Image.open(al.imagen_url).resize(
                    (200, 200), Image.Resampling.LANCZOS
                )
                img = CTkImage(light_image=pil, dark_image=pil, size=(200, 200))
                img_label.configure(image=img, text="")
                img_label.image = img
            except:
                img_label.configure(text="Error al cargar imagen", image=blank_img)
        else:
            img_label.configure(text="Sin imagen", image=blank_img)

        detalle = (
            f"Nombre:       {al.nom_producto}\n"
            f"Categoría:    {al.categoria or '—'}\n"
            f"Calorías:     {al.calorias} kcal\n"
            f"Proteína:     {al.proteina} g\n"
            f"Grasas:       {al.grasas} g\n"
            f"Carbohidratos:{al.carbohidratos} g\n\n"
            f"Descripción:\n{al.descripcion or '—'}"
        )
        text_label.configure(text=detalle)

    def _populate_list():
        for w in list_frame.winfo_children():
            w.destroy()

        datos = listar_alimentos()
        if not datos:
            ctk.CTkLabel(
                list_frame,
                text="No hay alimentos registrados.",
                font=("Segoe UI", 14),
            ).pack(pady=20)
            return

        for al in datos:
            icon = None
            if al.imagen_url:
                try:
                    thumb = Image.open(al.imagen_url)
                    thumb.thumbnail((30, 30))
                    icon = CTkImage(light_image=thumb, dark_image=thumb, size=(30, 30))
                except:
                    icon = None

            btn = ctk.CTkButton(
                list_frame,
                text=f"  {al.nom_producto}",
                image=icon,
                compound="left",
                anchor="w",
                width=220,
                height=36,
                corner_radius=8,
                command=lambda pid=al.id_producto: _mostrar_detalles(pid),
            )
            btn.image_ref = icon
            btn.pack(fill="x", pady=4, padx=4)

    footer = ctk.CTkFrame(pantalla, fg_color="transparent")
    footer.pack(fill="x", pady=(0, 20), padx=20)

    ctk.CTkButton(
        footer,
        text="← Volver al Menú",
        width=160,
        height=36,
        corner_radius=8,
        command=volver_cb,
    ).pack(side="left")

    _populate_list()
    _clear_detail()

    return pantalla
