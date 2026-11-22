from base import Modulo


class Nivel1(Modulo):
    titulo = "Nivel 1 – Dependientes del contexto (Autómata Linealmente Acotado): aⁿbⁿcⁿ"
    descripcion = ("La cinta está limitada por los delimitadores [ y ]. El cabezal va y viene: marca una a (X), "
                   "una b (Y) y una c (Z) por ciclo y regresa a [. Alfabeto: {a, b, c}.")
    ejemplos = [("aabbcc", "acepta"), ("abc", "acepta"), ("aabbc", "rechaza"), ("abcabc", "rechaza"), ("", "vacía")]

    def simular(self, s):
        if any(ch not in "abc" for ch in s):
            return [{"cinta": list("[" + s + "]"), "h": 0, "q": "-", "fin": False,
                     "msg": "La cadena solo puede contener a, b, c → RECHAZADA"}]
        t, h, F = list("[" + s + "]"), 0, []

        def reg(q, msg, fin=None):
            F.append({"cinta": t[:], "h": h, "q": q, "msg": msg, "fin": fin})

        def mover(d, q, msg):
            nonlocal h
            h += d
            reg(q, msg)

        def ir(d, perm, q):
            while t[h] in perm:
                mover(d, q, "Avanza " + ("→" if d > 0 else "←"))

        def rechazar(motivo):
            reg("qR", "RECHAZADA: " + motivo, False)
            return F

        reg("q0", "Cabezal sobre el delimitador izquierdo [")
        while True:
            mover(1, "q0", "Busca la siguiente 'a' sin marcar")
            ir(1, "X", "q0")
            if t[h] != "a":
                ir(1, "YZ", "q4")
                if t[h] == "]":
                    reg("qA", "Solo quedan X, Y, Z hasta ]: ACEPTADA", True)
                    return F
                return rechazar("sobran símbolos sin emparejar")
            t[h] = "X"
            reg("q1", "Marca a → X")
            mover(1, "q1", "Busca una 'b'")
            ir(1, "aY", "q1")
            if t[h] != "b":
                return rechazar("falta una 'b'")
            t[h] = "Y"
            reg("q2", "Marca b → Y")
            mover(1, "q2", "Busca una 'c'")
            ir(1, "bZ", "q2")
            if t[h] != "c":
                return rechazar("falta una 'c'")
            t[h] = "Z"
            reg("q3", "Marca c → Z; regresa al delimitador [")
            ir(-1, "abcXYZ", "q3")

    def dibujar(self, c, f):
        t, n = f["cinta"], len(f["cinta"])
        w = min(60, 900 // n)
        c.create_text(10, 30, text="Cinta acotada (delimitadores [ y ])", anchor="w", font=("Arial", 9))
        for k, sim in enumerate(t):
            x = 25 + k * w
            col = "#ffe08a" if k == f["h"] else ("#bbb" if sim in "[]" else ("#cfe8cf" if sim in "XYZ" else "white"))
            c.create_rectangle(x, 60, x + w, 60 + w, fill=col, width=2 if sim in "[]" else 1)
            c.create_text(x + w / 2, 60 + w / 2, text=sim, font=("Consolas", 16, "bold"))
        hx = 25 + f["h"] * w + w / 2
        c.create_polygon(hx, 70 + w, hx - 12, 95 + w, hx + 12, 95 + w, fill="red")
        c.create_text(hx, 110 + w, text=f"cabezal ({f['q']})", font=("Arial", 11, "bold"))
        c.create_text(25, 250, anchor="w", font=("Arial", 10),
                      text="Movimiento bidireccional: →/← entre [ y ]. X, Y, Z = símbolos ya emparejados.")
