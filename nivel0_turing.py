from tkinter import ttk
from base import Modulo

# (estado, símbolo) -> (nuevo estado, símbolo a escribir, movimiento)
ZERO_UNO = {
    ("q0", "0"): ("q1", "X", "R"), ("q0", "Y"): ("q3", "Y", "R"), ("q0", "_"): ("qA", "_", "S"),
    ("q1", "0"): ("q1", "0", "R"), ("q1", "Y"): ("q1", "Y", "R"), ("q1", "1"): ("q2", "Y", "L"),
    ("q2", "0"): ("q2", "0", "L"), ("q2", "Y"): ("q2", "Y", "L"), ("q2", "X"): ("q0", "X", "R"),
    ("q3", "Y"): ("q3", "Y", "R"), ("q3", "_"): ("qA", "_", "S"),
}
SUMA = {
    ("q0", "1"): ("q0", "1", "R"), ("q0", "+"): ("q1", "1", "R"),
    ("q1", "1"): ("q1", "1", "R"), ("q1", "_"): ("q2", "_", "L"),
    ("q2", "1"): ("qA", "_", "S"),
}
PROGRAMAS = {
    "Aceptar 0ⁿ1ⁿ": ZERO_UNO,
    "Suma unaria (1^a+1^b)": SUMA,
}


class Nivel0(Modulo):
    titulo = "Nivel 0 – Máquina de Turing"
    descripcion = ("Cinta infinita a ambos lados (símbolo blanco _). Programa 1: acepta 0ⁿ1ⁿ. "
                   "Programa 2: suma unaria, p. ej. 11+111 → 11111 (5).")
    ejemplos = [("0011", "0ⁿ1ⁿ ok"), ("001", "0ⁿ1ⁿ no"), ("11+111", "suma"), ("1+1", "suma")]

    def __init__(self, master):
        super().__init__(master)
        fila = ttk.Frame(self)
        fila.pack(before=self.canvas)
        ttk.Label(fila, text="Programa:").pack(side="left")
        self.prog = ttk.Combobox(fila, values=list(PROGRAMAS), state="readonly", width=24)
        self.prog.current(0)
        self.prog.pack(side="left", padx=4)
        self.prog.bind("<<ComboboxSelected>>", lambda e: self.iniciar())

    def simular(self, s):
        tabla = PROGRAMAS[self.prog.get()]
        cinta = {i: ch for i, ch in enumerate(s)}
        q, h, F = "q0", 0, []

        def reg(msg, fin=None):
            F.append({"cinta": dict(cinta), "h": h, "q": q, "msg": msg, "fin": fin})

        reg("Estado inicial q0, cabezal en el primer símbolo")
        for _ in range(500):
            if q == "qA":
                break
            sim = cinta.get(h, "_")
            if (q, sim) not in tabla:
                reg(f"Sin transición para ({q}, {sim}) → RECHAZADA", False)
                return F
            q, esc, mov = tabla[(q, sim)]
            if esc == "_":
                cinta.pop(h, None)
            else:
                cinta[h] = esc
            h += {"R": 1, "L": -1, "S": 0}[mov]
            reg(f"Leyó '{sim}': escribe '{esc}', mueve {mov}, nuevo estado {q}")
        if q == "qA":
            res = "".join(cinta[k] for k in sorted(cinta))
            reg(f"Estado de aceptación qA. Cinta final: {res or 'vacía'} → ACEPTADA", True)
        else:
            reg("Se superó el límite de 500 pasos → RECHAZADA", False)
        return F

    def dibujar(self, c, f):
        tabla = PROGRAMAS[self.prog.get()]
        alfabeto = sorted({k[1] for k in tabla} | {v[1] for v in tabla.values()})
        c.create_text(10, 20, anchor="w", font=("Arial", 10),
                      text=f"Alfabeto de la cinta: {{{', '.join(alfabeto)}}}   (_ = blanco)")
        c.create_text(10, 45, anchor="w", font=("Arial", 14, "bold"), text=f"Estado activo: {f['q']}",
                      fill="green" if f["q"] == "qA" else "black")
        for i in range(17):
            pos = f["h"] - 8 + i
            x = 50 + i * 50
            c.create_rectangle(x, 100, x + 50, 150, fill="#ffe08a" if i == 8 else "white")
            c.create_text(x + 25, 125, text=f["cinta"].get(pos, "_"), font=("Consolas", 18, "bold"))
            c.create_text(x + 25, 165, text=str(pos), font=("Arial", 8), fill="gray")
        c.create_polygon(475, 180, 463, 205, 487, 205, fill="red")
        c.create_text(475, 220, text="cabezal de lectura/escritura", font=("Arial", 10, "bold"))
        c.create_text(475, 280, text="← la cinta se extiende indefinidamente en ambas direcciones →", fill="gray")
