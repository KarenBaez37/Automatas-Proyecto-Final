import tkinter as tk
from tkinter import ttk
from nivel0_turing import Nivel0
from nivel1_lba import Nivel1
from nivel2_pila import Nivel2
from nivel3_afd import Nivel3

# Paleta de colores azules
BG_APP = "#EFF6FF"       # Azul hielo muy suave para el fondo
BG_HEADER = "#1E3A8A"    # Azul marino profundo para la cabecera
BG_CARD = "#FFFFFF"      # Blanco para contenedores y lienzos
ACCENT = "#2563EB"       # Azul vibrante para botones y pestañas activas
ACCENT_HOVER = "#1D4ED8" # Azul más oscuro al pasar el mouse
TAB_INACTIVE = "#DBEAFE" # Azul claro para pestañas inactivas
TEXT_DARK = "#0F172A"    # Texto principal oscuro
TEXT_MUTED = "#475569"   # Texto secundario

root = tk.Tk()
root.title("Jerarquía de Chomsky – Simulador de Autómatas")
root.geometry("1040x730")
root.configure(bg=BG_APP)

# Configuración de estilos ttk
style = ttk.Style(root)
style.theme_use("clam")

style.configure(".", background=BG_APP, foreground=TEXT_DARK, font=("Segoe UI", 10))
style.configure("TFrame", background=BG_APP)
style.configure("TLabel", background=BG_APP, foreground=TEXT_DARK, font=("Segoe UI", 10))

# Estilo de pestañas (Notebook)
style.configure("TNotebook", background=BG_APP, borderwidth=0, tabmargins=[4, 6, 4, 0])
style.configure(
    "TNotebook.Tab",
    background=TAB_INACTIVE,
    foreground=BG_HEADER,
    padding=[16, 8],
    font=("Segoe UI", 10, "bold"),
    borderwidth=0,
)
style.map(
    "TNotebook.Tab",
    background=[("selected", ACCENT), ("active", "#BFDBFE")],
    foreground=[("selected", "#FFFFFF"), ("active", BG_HEADER)],
)

# Estilo de botones
style.configure(
    "TButton",
    background=ACCENT,
    foreground="#FFFFFF",
    font=("Segoe UI", 9, "bold"),
    padding=[12, 6],
    borderwidth=0,
)
style.map(
    "TButton",
    background=[("active", ACCENT_HOVER), ("pressed", BG_HEADER)],
    foreground=[("active", "#FFFFFF")],
)

# Estilo de entradas y combobox
style.configure("TEntry", fieldbackground="#FFFFFF", padding=5)
style.configure("TCombobox", fieldbackground="#FFFFFF", padding=5)

# Cabecera superior azul
header = tk.Frame(root, bg=BG_HEADER, pady=14, padx=20)
header.pack(fill="x")

tk.Label(
    header,
    text="Jerarquía de Chomsky — Simulador Interactivo",
    bg=BG_HEADER,
    fg="#FFFFFF",
    font=("Segoe UI", 16, "bold"),
).pack(anchor="w")

tk.Label(
    header,
    text="Visualización y validación paso a paso de modelos computacionales (Niveles 3, 2, 1 y 0)",
    bg=BG_HEADER,
    fg="#BFDBFE",
    font=("Segoe UI", 9),
).pack(anchor="w", pady=(2, 0))

# Contenedor de pestañas
nb = ttk.Notebook(root)
nb.pack(fill="both", expand=True, padx=14, pady=12)

for nombre, clase in [
    ("Nivel 3: Regular (AFD)", Nivel3),
    ("Nivel 2: Libre de contexto (Pila)", Nivel2),
    ("Nivel 1: Sensible al contexto (LBA)", Nivel1),
    ("Nivel 0: Máquina de Turing", Nivel0),
]:
    nb.add(clase(nb), text=nombre)

# Barra inferior discreta
footer = tk.Label(
    root,
    text="Selecciona un nivel en las pestañas superiores • Ingresa una cadena o usa los ejemplos precargados",
    bg="#DBEAFE",
    fg=BG_HEADER,
    font=("Segoe UI", 8),
    pady=5,
)
footer.pack(fill="x", side="bottom")

root.mainloop()
