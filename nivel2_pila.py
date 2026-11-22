from base import Modulo, dibujar_cinta


class Nivel2(Modulo):
    titulo = "Nivel 2 – Lenguajes libres de contexto (Autómata de Pila): aⁿbⁿ"
    descripcion = "Cada 'a' apila una A; cada 'b' desapila una A. Se acepta si la pila queda solo con Z."
    ejemplos = [("aabb", "acepta"), ("aaabbb", "acepta"), ("aab", "rechaza"), ("abab", "rechaza"), ("", "vacía")]

    def simular(self, s):
        q, pila, F = "q0", ["Z"], []

        def reg(pos, msg, fin=None):
            F.append({"q": q, "pos": pos, "s": s, "pila": pila[:], "msg": msg, "fin": fin})

        reg(0, "Inicio: la pila solo tiene el símbolo de fondo Z")
        for k, ch in enumerate(s):
            if ch == "a" and q == "q0":
                pila.append("A")
                reg(k + 1, "Lee 'a': apila A (push)")
            elif ch == "b" and pila[-1] == "A":
                pila.pop()
                q = "q1"
                reg(k + 1, "Lee 'b': desapila A (pop)")
            else:
                reg(k + 1, f"Lee '{ch}': no hay transición válida → RECHAZADA", False)
                return F
        ok = pila == ["Z"]
        reg(len(s), "Cadena consumida y pila vacía (solo Z): ACEPTADA" if ok
            else "Cadena consumida pero sobran A en la pila: RECHAZADA", ok)
        return F

    def dibujar(self, c, f):
        dibujar_cinta(c, f["s"], f["pos"])
        c.create_oval(100, 160, 180, 240, width=2, fill="#7fd67f")
        c.create_text(140, 200, text=f["q"], font=("Arial", 14, "bold"))
        c.create_text(140, 255, text="Estado actual")
        c.create_text(700, 100, text="PILA (LIFO)", font=("Arial", 11, "bold"))
        base_y = 320
        for k, sim in enumerate(f["pila"]):
            y = base_y - (k + 1) * 32
            top = k == len(f["pila"]) - 1
            c.create_rectangle(660, y, 740, y + 32, fill="#ffe08a" if top else ("#ccc" if sim == "Z" else "#9ecbff"))
            c.create_text(700, y + 16, text=sim, font=("Consolas", 14, "bold"))
        c.create_text(760, base_y - len(f["pila"]) * 32 + 16, text="← tope", anchor="w")
