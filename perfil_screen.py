import tkinter as tk

def crear_perfil_screen(parent, volver_callback):
    perfil_frame = tk.Frame(parent, bg="#FFFFE0")
    perfil_frame.pack(expand=True, fill="both")

    tk.Label(perfil_frame, text="Perfil del Usuario", font=("Segoe UI", 16, "bold"), bg="#FFFFE0").pack(pady=20)

    boton_volver = tk.Button(perfil_frame, text="Volver", command=volver_callback,
                              bg="#6C757D", fg="white", font=("Segoe UI", 10), relief="flat", padx=10, pady=5)
    boton_volver.pack(pady=10)

    return perfil_frame