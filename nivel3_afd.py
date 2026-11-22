from tkinter import ttk
from base import Modulo, dibujar_cinta

LENGUAJES = {
    "Número par de 0s": {
        "estados": ["q0", "q1"], "acepta": ["q0"],
        "delta": {"q0": {"0": "q1", "1": "q0"}, "q1": {"0": "q0", "1": "q1"}},
    },
    "Termina en 01": {
        "estados": ["q0", "q1", "q2"], "acepta": ["q2"],
        "delta": {"q0": {"0": "q1", "1": "q0"},
                  "q1": {"0": "q1", "1": "q2"},
                  "q2": {"0": "q1", "1": "q0"}},
    },
}


class Nivel3(Modulo):
    titulo = "Nivel 3 – Lenguajes regulares (Autómata Finito Determinista)"
    descripcion = "Elige el lenguaje; el autómata procesa la cadena símbolo a símbolo. Alfabeto: {0, 1}."
    ejemplos = [("1001", "prueba"), ("110", "prueba"), ("0101", "prueba"), ("", "vacía")]

    def __init__(self, master):
        super().__init__(master)
        fila = ttk.Frame(self)
        fila.pack(before=self.canvas)
        ttk.Label(fila, text="Lenguaje:").pack(side="left")
        self.lang = ttk.Combobox(fila, values=list(LENGUAJES), state="readonly", width=20)
        self.lang.current(0)
        self.lang.pack(side="left", padx=4)
        self.lang.bind("<<ComboboxSelected>>", lambda e: self.iniciar())

    def simular(self, s):
        L = LENGUAJES[self.lang.get()]
        q, F = "q0", []

        def reg(pos, msg, fin=None):
            F.append({"q": q, "pos": pos, "s": s, "msg": msg, "fin": fin})

        reg(0, "Estado inicial q0")
        for k, ch in enumerate(s):
            if ch not in L["delta"][q]:
                reg(k + 1, f"Símbolo '{ch}' fuera del alfabeto → RECHAZADA", False)
                return F
            nq = L["delta"][q][ch]
            msg = f"Lee '{ch}': δ({q},{ch}) = {nq}"
            q = nq
            reg(k + 1, msg)
        ok = q in L["acepta"]
        reg(len(s), f"Fin de la cadena en {q}: " + ("ACEPTADA" if ok else "RECHAZADA"), ok)
        return F

    def dibujar(self, c, f):
        L = LENGUAJES[self.lang.get()]
        dibujar_cinta(c, f["s"], f["pos"])
        y = 170
        c.create_text(40, y - 55, text="Autómata (verde = estado actual, doble círculo = aceptación)",
                      anchor="w", font=("Arial", 9))
        for k, q in enumerate(L["estados"]):
            x = 150 + k * 250
            c.create_oval(x - 35, y - 35, x + 35, y + 35, width=2,
                          fill="#7fd67f" if q == f["q"] else "white")
            if q in L["acepta"]:
                c.create_oval(x - 28, y - 28, x + 28, y + 28)
            c.create_text(x, y, text=q, font=("Arial", 14, "bold"))
            if k == 0:
                c.create_line(60, y, x - 35, y, arrow="last", width=2)
        for k, (q, t) in enumerate(L["delta"].items()):
            c.create_text(150 + k * 250, 235, anchor="n", font=("Consolas", 11),
                          text="\n".join(f"δ({q},{a}) = {n}" for a, n in t.items()))
