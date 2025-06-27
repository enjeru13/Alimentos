import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import messagebox
from PIL import Image

from controllers.alimentos_controller import listar_alimentos, obtener_alimento


def crear_alimentos_user_screen(parent, volver_cb):
    pantalla = ctk.CTkFrame(parent)
    pantalla.pack(expand=True, fill="both", padx=20, pady=20)
    pantalla.bind_class("CTkButton", "<Return>", lambda e: e.widget.invoke())

    ctk.CTkLabel(pantalla, text="Alimentos", font=("Segoe UI", 22, "bold")).pack(
        pady=(0, 15)
    )

    panel = ctk.CTkFrame(pantalla, fg_color="transparent")
    panel.pack(expand=True, fill="both")

    lista_frame = ctk.CTkScrollableFrame(panel, corner_radius=10)
    lista_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

    detail_frame = ctk.CTkFrame(panel, corner_radius=10)
    detail_frame.pack(side="right", fill="both", expand=True)

    blank = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    blank_img = CTkImage(light_image=blank, dark_image=blank, size=(200, 200))
    img_label = ctk.CTkLabel(detail_frame, image=blank_img, text="")
    img_label.image = blank_img
    img_label.pack(pady=(20, 10))

    text_label = ctk.CTkLabel(
        detail_frame,
        text="Selecciona un alimento para ver detalles",
        wraplength=280,
        justify="left",
    )
    text_label.pack(fill="both", expand=True, padx=10, pady=(0, 20))

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
            img_label.image = blank_img

        detalle = (
            f"Nombre:       {al.nom_producto}\n\n"
            f"Categoría:    {al.categoria or '—'}\n\n"
            f"Calorías:     {al.calorias} kcal\n\n"
            f"Proteína:     {al.proteina} g\n\n"
            f"Grasas:       {al.grasas} g\n\n"
            f"Carbohidratos:{al.carbohidratos} g\n\n"
            f"Descripción:\n{al.descripcion or '—'}"
        )
        text_label.configure(text=detalle)

    def _populate():
        for w in lista_frame.winfo_children():
            w.destroy()

        datos = listar_alimentos()
        if not datos:
            ctk.CTkLabel(
                lista_frame, text="No hay alimentos registrados.", font=("Segoe UI", 14)
            ).pack(pady=20)
            return

        for al in datos:
            icon = None
            if al.imagen_url:
                try:
                    pil = Image.open(al.imagen_url)
                    pil.thumbnail((30, 30))
                    icon = CTkImage(light_image=pil, dark_image=pil, size=(30, 30))
                except:
                    icon = None

            btn = ctk.CTkButton(
                lista_frame,
                text=f"  {al.nom_producto}",
                image=icon,
                compound="left",
                anchor="w",
                width=1,
                corner_radius=8,
                command=lambda pid=al.id_producto: _mostrar_detalles(pid),
            )
            btn.image_ref = icon
            btn.pack(fill="x", pady=4, padx=4)

    _populate()

    ctk.CTkButton(
        pantalla, text="Volver al Menú", width=200, corner_radius=8, command=volver_cb
    ).pack(side="bottom", pady=(5, 5))

    ctk.CTkButton(
        pantalla, text="Refrescar", width=100, corner_radius=8, command=_populate
    ).pack(side="bottom", pady=(5, 10))

    return pantalla
