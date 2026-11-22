import tkinter as tk
from tkinter import ttk
from nivel0_turing import Nivel0
from nivel1_lba import Nivel1
from nivel2_pila import Nivel2
from nivel3_afd import Nivel3

root = tk.Tk()
root.title("Jerarquía de Chomsky - Simulador de Autómatas")
root.geometry("1000x700")
ttk.Label(root, text="Jerarquía de Chomsky – Panel principal (elige un módulo)",
          font=("Arial", 16, "bold")).pack(pady=8)
nb = ttk.Notebook(root)
nb.pack(fill="both", expand=True, padx=8, pady=8)
for nombre, clase in [("Nivel 3: Regular (AFD)", Nivel3), ("Nivel 2: Libre de contexto (Pila)", Nivel2),
                      ("Nivel 1: Sensible al contexto (LBA)", Nivel1), ("Nivel 0: Máquina de Turing", Nivel0)]:
    nb.add(clase(nb), text=nombre)
root.mainloop()
