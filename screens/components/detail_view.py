import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image


class DetailView(ctk.CTkFrame):
    """
    Muestra la imagen (200×200 fija) y el texto de detalle en un CTkTextbox.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # placeholder transparente para no romper la etiqueta
        pil = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
        self.blank = CTkImage(light_image=pil, dark_image=pil, size=(200, 200))

        self.img_label = ctk.CTkLabel(self, image=self.blank, text="")
        self.img_label.image = self.blank
        self.img_label.pack(side="left", padx=(0, 10), pady=5)

        self.text = ctk.CTkTextbox(self, font=("Segoe UI", 12))
        self.text.pack(side="left", fill="both", expand=True, pady=5)
        self.text.configure(state="disabled")

    def show(self, al):
        # reset
        self.img_label.configure(image=self.blank, text="")
        self.img_label.image = self.blank
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")

        # imagen fija 200×200
        if al and getattr(al, "imagen_url", None):
            try:
                pil = Image.open(al.imagen_url).resize(
                    (200, 200), Image.Resampling.LANCZOS
                )
                img = CTkImage(light_image=pil, dark_image=pil, size=(200, 200))
                self.img_label.configure(image=img, text="")
                self.img_label.image = img
            except:
                pass

        # detalle
        if not al:
            self.text.insert("end", "No se pudieron obtener los detalles.")
        else:
            detalle = (
                f"Nombre:       {al.nom_producto}\n"
                f"Categoría:    {al.categoria or '—'}\n"
                f"Calorías:     {al.calorias} kcal\n"
                f"Proteína:     {al.proteina} g\n"
                f"Grasas:       {al.grasas} g\n"
                f"Carbohidratos:{al.carbohidratos} g\n"
                f"\nDescripción:\n{al.descripcion or '—'}"
            )
            self.text.insert("end", detalle)

        self.text.configure(state="disabled")
