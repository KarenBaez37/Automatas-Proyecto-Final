DOCUMENTO DE IMPLEMENTACIÓN Y CONCEPTOS APLICADOS: SIMULADOR INTERACTIVO DE LA JERARQUÍA DE CHOMSKY

1. INTRODUCCIÓN Y OBJETIVO DEL SISTEMA
Este proyecto consiste en una aplicación de escritorio con interfaz gráfica desarrollada en Python y Tkinter para visualizar, simular y validar paso a paso el comportamiento de los modelos computacionales de los cuatro niveles de la Jerarquía de Chomsky (Niveles 3, 2, 1 y 0).

Permite probar cadenas propias o ejemplos precargados y observar transiciones de estado, memoria auxiliar (pila o cinta) y movimiento de cabezales para comprender las capacidades y límites de cada nivel.

2. ARQUITECTURA DEL SOFTWARE E IMPLEMENTACIÓN TÉCNICA
El código está organizado de forma modular:

- main.py (Panel principal y estilos): Configura la ventana principal, la paleta de colores azul y los estilos ttk, y crea un componente de pestañas (ttk.Notebook) para cambiar entre los cuatro módulos.
- base.py (Clase base Modulo y motor de pasos): Define los controles comunes (Iniciar, Paso ▶, Auto, Reiniciar), los botones de ejemplos, el lienzo gráfico (tk.Canvas) y la barra de estado inferior.
  * Simulación por pasos: Cada nivel implementa simular(cadena), que devuelve una lista de pasos con el estado actual (q), la cinta o pila, un mensaje explicativo (msg) y el estado final (fin: None en curso, True aceptada, False rechazada).
  * Reproducción: Permite avanzar manualmente con Paso ▶ o automáticamente con Auto mediante temporizadores (after).

3. CONCEPTOS TEÓRICOS E IMPLEMENTACIÓN POR NIVEL

Nivel 3 – Lenguajes Regulares: Autómata Finito Determinista (nivel3_afd.py)
- Concepto: Los lenguajes regulares (Tipo 3) son reconocidos por un Autómata Finito Determinista (AFD), definido formalmente como (Q, Σ, δ, q0, F). No usa memoria auxiliar externa; toda la información depende de su conjunto finito de estados y de leer la cadena símbolo a símbolo de izquierda a derecha.
- Implementación: Incluye dos lenguajes sobre el alfabeto {0, 1} mediante la tabla de transiciones delta:
  1) Número par de 0s: Alterna entre q0 (par, estado de aceptación) y q1 (impar) al leer 0, y se mantiene en su estado al leer 1.
  2) Termina en 01: Usa tres estados (q0, q1, q2) para seguir la secuencia final y acepta en q2.
- Visualización: Dibuja la cinta de entrada, resalta en verde el estado activo, marca con doble círculo los estados de aceptación y muestra las transiciones δ(q, a).

Nivel 2 – Lenguajes Libres de Contexto: Autómata de Pila (nivel2_pila.py)
- Concepto: Los lenguajes libres de contexto (Tipo 2) requieren memoria auxiliar de tipo LIFO (último en entrar, primero en salir), modelada por un Autómata de Pila. Esto permite contar y emparejar símbolos anidados, como en el lenguaje a^n b^n.
- Implementación: La pila inicia con el símbolo de fondo Z en el estado q0. Por cada 'a' leída en q0 se apila una 'A' (push); al leer 'b' se pasa a q1 y se desapila una 'A' (pop). Acepta si al terminar la cadena la pila queda solo con Z.
- Visualización: Muestra la cinta, el estado actual y la pila vertical indicando el tope, los elementos apilados y la base Z.

Nivel 1 – Lenguajes Sensibles al Contexto: Autómata Linealmente Acotado (nivel1_lba.py)
- Concepto: Los lenguajes sensibles al contexto (Tipo 1), como a^n b^n c^n, requieren más capacidad que una pila pero limitan su memoria a un espacio proporcional a la longitud de la entrada. El modelo asociado es el Autómata Linealmente Acotado (LBA), con cinta delimitada por fronteras izquierda y derecha y cabezal bidireccional.
- Implementación: Encierra la cadena entre los delimitadores '[' y ']'. En cada ciclo avanza buscando una 'a' sin marcar y la cambia por 'X', busca una 'b' y la cambia por 'Y', y busca una 'c' y la cambia por 'Z', regresando luego hasta '['. Acepta en qA si al no quedar más 'a' solo restan marcas Y y Z hasta ']'; en caso contrario rechaza en qR.
- Visualización: Representa la cinta acotada entre '[' y ']', los símbolos marcados (X, Y, Z) y el cabezal con su movimiento bidireccional.

Nivel 0 – Lenguajes Recursivamente Enumerables: Máquina de Turing (nivel0_turing.py)
- Concepto: Los lenguajes de Tipo 0 corresponden a la Máquina de Turing, modelo general de cómputo con una cinta extendible en ambas direcciones con símbolos blancos (_), capacidad de leer, escribir y moverse a izquierda (L), derecha (R) o quedarse (S), y estado de aceptación.
- Implementación: Representa la cinta como un diccionario {posición: símbolo} usando '_' para celdas vacías. Incluye dos programas:
  1) Aceptar 0^n 1^n: Marca ceros con X y unos con Y moviendo el cabezal entre extremos hasta llegar a qA.
  2) Suma unaria (1^a+1^b): Recorre los unos, convierte '+' en '1', llega al blanco final, retrocede una posición y borra un '1' para dejar el resultado en unario.
- Visualización: Muestra una ventana de celdas alrededor del cabezal con sus índices, el alfabeto de la cinta, el estado activo y el cabezal de lectura/escritura.

4. PRUEBAS Y VALIDACIÓN
La interfaz incluye ejemplos directos en cada módulo para comprobar aceptación y rechazo:
- Nivel 3 (Par de 0s): '1001' y '110' aceptan; '0' y '10' rechazan.
- Nivel 3 (Termina en 01): '0101' y '101' aceptan; '110' y '010' rechazan.
- Nivel 2 (a^n b^n): 'aabb', 'aaabbb' y 'ε' aceptan; 'aab' y 'abab' rechazan.
- Nivel 1 (a^n b^n c^n): 'abc' y 'aabbcc' aceptan; 'aabbc' y 'abcabc' rechazan.
- Nivel 0 (0^n 1^n): '0011' acepta; '001' y '0111' rechazan.
- Nivel 0 (Suma unaria): '11+111' produce '11111' (5) y '1+1' produce '11' (2).
