import tkinter as tk
from tkinter import ttk


def dibujar_cinta(c, s, pos, y=30):
    """Dibuja la cadena de entrada; gris = consumido, amarillo = último símbolo leído."""
    c.create_text(10, y - 14, text="Cadena de entrada", anchor="w", font=("Arial", 9))
    for k, ch in enumerate(s):
        x = 60 + k * 40
        color = "#ffe08a" if k == pos - 1 else ("#ddd" if k < pos else "white")
        c.create_rectangle(x, y, x + 40, y + 40, fill=color)
        c.create_text(x + 20, y + 20, text=ch, font=("Consolas", 16))
    if not s:
        c.create_text(60, y + 20, text="(cadena vacía ε)", anchor="w")


class Modulo(ttk.Frame):
    """Base de cada nivel: controles + reproductor de pasos.
    Cada nivel define simular(cadena) -> lista de pasos y dibujar(canvas, paso)."""
    titulo = ""
    descripcion = ""
    ejemplos = []  # (cadena, etiqueta)

    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self, text=self.titulo, font=("Arial", 14, "bold")).pack(pady=(8, 0))
        ttk.Label(self, text=self.descripcion, wraplength=900).pack()
        top = ttk.Frame(self)
        top.pack(pady=6)
        ttk.Label(top, text="Cadena:").pack(side="left")
        self.entrada = ttk.Entry(top, width=25)
        self.entrada.pack(side="left", padx=4)
        ttk.Button(top, text="Iniciar", command=self.iniciar).pack(side="left")
        ttk.Button(top, text="Paso ▶", command=self.paso).pack(side="left", padx=2)
        ttk.Button(top, text="Auto", command=self.auto).pack(side="left")
        ttk.Button(top, text="Reiniciar", command=self.iniciar).pack(side="left", padx=2)
        ex = ttk.Frame(self)
        ex.pack()
        ttk.Label(ex, text="Ejemplos:").pack(side="left")
        for cad, et in self.ejemplos:
            ttk.Button(ex, text=f"{cad or 'ε'} ({et})",
                       command=lambda c=cad: self.cargar(c)).pack(side="left", padx=2)
        self.canvas = tk.Canvas(self, width=950, height=340, bg="white")
        self.canvas.pack(pady=6)
        self.estado = ttk.Label(self, text="Escribe una cadena (o elige un ejemplo) y pulsa Iniciar.",
                                font=("Arial", 11))
        self.estado.pack()
        self.pasos, self.i, self.job = [], 0, None

    def cargar(self, cad):
        self.entrada.delete(0, "end")
        self.entrada.insert(0, cad)
        self.iniciar()

    def iniciar(self):
        if self.job:
            self.after_cancel(self.job)
            self.job = None
        self.pasos, self.i = self.simular(self.entrada.get().strip()), 0
        self.mostrar()

    def paso(self):
        if not self.pasos:
            self.iniciar()
        elif self.i < len(self.pasos) - 1:
            self.i += 1
            self.mostrar()

    def auto(self):
        if self.job:
            self.after_cancel(self.job)
            self.job = None
            return
        if not self.pasos or self.i >= len(self.pasos) - 1:
            self.iniciar()
        self._tick()

    def _tick(self):
        if self.i < len(self.pasos) - 1:
            self.i += 1
            self.mostrar()
            self.job = self.after(700, self._tick)
        else:
            self.job = None

    def mostrar(self):
        self.canvas.delete("all")
        p = self.pasos[self.i]
        self.dibujar(self.canvas, p)
        color = {True: "green", False: "red", None: "black"}[p["fin"]]
        self.estado.config(text=f"Paso {self.i}/{len(self.pasos) - 1}: {p['msg']}", foreground=color)
