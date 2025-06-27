# screens/alimentos_user_screen.py

import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import messagebox
from PIL import Image

from controllers.alimentos_controller import listar_alimentos, obtener_alimento


def crear_alimentos_user_screen(parent, volver_cb):
    """
    Pantalla de lista de alimentos (solo lectura) para usuarios.
    Muestra miniaturas en la lista y detalle en ventana scrollable.
    """
    pantalla = ctk.CTkFrame(parent)
    pantalla.pack(expand=True, fill="both")

    # — Título —
    ctk.CTkLabel(
        pantalla,
        text="Lista de Alimentos",
        font=("Segoe UI", 22, "bold"),
    ).pack(pady=20)

    # — Lista scrollable de botones —
    lista_frame = ctk.CTkScrollableFrame(pantalla, width=600, height=400)
    lista_frame.pack(padx=20, pady=10, fill="both", expand=True)

    def _populate():
        for w in lista_frame.winfo_children():
            w.destroy()

        alimentos = listar_alimentos()
        if not alimentos:
            ctk.CTkLabel(
                lista_frame,
                text="No hay alimentos registrados.",
                font=("Segoe UI", 14),
            ).pack(pady=10)
            return

        for al in alimentos:
            img_icon = None
            if al.imagen_url:
                try:
                    pil = Image.open(al.imagen_url)
                    pil.thumbnail((30, 30))
                    img_icon = CTkImage(light_image=pil, dark_image=pil, size=(30, 30))
                except:
                    img_icon = None

            btn = ctk.CTkButton(
                lista_frame,
                text=f"  {al.nom_producto}",
                image=img_icon,
                compound="left",
                fg_color="#3498DB",
                hover_color="#2980B9",
                anchor="w",
                command=lambda pid=al.id_producto: _mostrar_detalles(pid),
            )
            btn.image_ref = img_icon
            btn.pack(fill="x", padx=5, pady=3)

    def _mostrar_detalles(id_producto: int):
        al = obtener_alimento(id_producto)
        if not al:
            return messagebox.showerror("Error", "No se pudieron obtener los detalles.")

        top = ctk.CTkToplevel(pantalla)
        top.title(al.nom_producto)
        top.geometry("750x500")

        # Frame scrollable para todo el contenido
        scroll = ctk.CTkScrollableFrame(top, width=730, height=480)
        scroll.pack(padx=10, pady=10, fill="both", expand=True)

        # — Imagen fija 200×200 —
        if al.imagen_url:
            try:
                pil = Image.open(al.imagen_url)
                pil = pil.resize((200, 200), Image.Resampling.LANCZOS)
                img_preview = CTkImage(light_image=pil, dark_image=pil, size=(200, 200))
                lbl_img = ctk.CTkLabel(scroll, image=img_preview, text="")
                lbl_img.image = img_preview
                lbl_img.pack(pady=(0, 10))
            except:
                ctk.CTkLabel(scroll, text="Error al cargar imagen").pack(pady=(0, 10))
        else:
            ctk.CTkLabel(scroll, text="Sin imagen", font=("Segoe UI", 12)).pack(
                pady=(0, 10)
            )

        # — Texto de detalles —
        detalle_text = (
            f"Nombre:       {al.nom_producto}\n\n"
            f"Categoría:    {al.categoria or '—'}\n\n"
            f"Calorías:     {al.calorias} kcal\n\n"
            f"Proteína:     {al.proteina} g\n\n"
            f"Grasas:       {al.grasas} g\n\n"
            f"Carbohidratos:{al.carbohidratos} g\n\n"
            f"Descripción:\n{al.descripcion or '—'}\n"
        )
        ctk.CTkLabel(
            scroll,
            text=detalle_text,
            font=("Segoe UI", 12),
            wraplength=700,
            justify="left",
        ).pack(fill="x", pady=(0, 20))

        # — Botón Cerrar —
        ctk.CTkButton(
            scroll,
            text="Cerrar",
            command=top.destroy,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            width=100,
        ).pack(pady=(0, 10))

    # Inicializa la lista
    _populate()

    # — Botón Volver al menú —
    ctk.CTkButton(
        pantalla,
        text="Volver al Menú",
        command=volver_cb,
        fg_color="#27AE60",
        hover_color="#2ECC71",
        width=200,
    ).pack(pady=15)

    return pantalla
