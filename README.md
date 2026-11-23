# Jerarquía de Chomsky – Simulador de Autómatas

Aplicación con interfaz gráfica (Python + Tkinter) con un módulo interactivo por cada nivel de la Jerarquía de Chomsky.

## Requisitos y ejecución
- Python 3.8 o superior (Tkinter viene incluido; no hay que instalar nada más).
- Clonar y ejecutar:
```
git clone https://github.com/KarenBaez37/Automatas-Proyecto-Final.git
cd Automatas-Proyecto-Final
python main.py
```

## Uso
Elige una pestaña (módulo), escribe una cadena o pulsa un botón de **Ejemplos**, y usa **Iniciar**, **Paso ▶** (avanza un paso), **Auto** (animación) o **Reiniciar**.

## Módulos y cadenas de prueba
| Nivel | Modelo | Lenguaje | Acepta | Rechaza |
|---|---|---|---|---|
| 3 | AFD | Par de 0s / Termina en 01 (alfabeto {0,1}) | `1001`, `110` (par de 0s) · `0101`, `101` (termina en 01) | `0`, `10` (par de 0s) · `110`, `010` (termina en 01) |
| 2 | Autómata de pila | aⁿbⁿ | `aabb`, `aaabbb`, `ε` | `aab`, `abab` |
| 1 | LBA | aⁿbⁿcⁿ | `abc`, `aabbcc` | `aabbc`, `abcabc` |
| 0 | Máquina de Turing | 0ⁿ1ⁿ / suma unaria | `0011` · `11+111` (resultado 11111) | `001`, `0111` |

## Archivos
- `main.py`: panel principal con los cuatro módulos.
- `base.py`: controles y reproductor de pasos compartidos.
- `nivel3_afd.py`, `nivel2_pila.py`, `nivel1_lba.py`, `nivel0_turing.py`: un módulo por nivel.


# Jerarquía de Chomsky – Simulador Interactivo de Autómatas

Aplicación de escritorio desarrollada en **Python** con interfaz gráfica (**Tkinter**) para visualizar, simular y validar el comportamiento paso a paso de modelos computacionales correspondientes a los cuatro niveles de la **Jerarquía de Chomsky**.

## Requisitos e instalación

- **Python 3.8 o superior** (incluye `tkinter` de forma estándar en Windows; no requiere instalar librerías externas).

### Ejecutar desde GitHub
```bash
git clone [https://github.com/KarenBaez37/Automatas-Proyecto-Final.git](https://github.com/KarenBaez37/Automatas-Proyecto-Final.git)
cd Automatas-Proyecto-Final
python main.py
