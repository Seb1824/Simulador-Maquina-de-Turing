# Simulador de Máquina de Turing

Aplicación web (Streamlit) para definir y ejecutar Máquinas de Turing. Permite cargar ejemplos predefinidos, usar archivos personalizados y visualizar cinta, tabla de transiciones, grafo de estados e historial de ejecución.

## Requisitos
- Python 3.10+ (recomendado)
- Dependencias: `streamlit`, `pandas`, `graphviz`
- Graphviz instalado en el sistema (añade su `bin` al `PATH` en Windows) para renderizar el grafo de estados.

Instalación típica:
```bash
python -m venv venv
.\venv\Scripts\activate      # Windows
pip install streamlit pandas graphviz
```

## Ejecutar la app
```bash
streamlit run app.py
```
Se abrirá en el navegador (por defecto http://localhost:8501).

## Estructura breve
- `app.py`: interfaz Streamlit y lógica de interacción.
- `src/turing_machine.py`: núcleo de la MT (cinta, pasos, estados).
- `src/tape.py`: implementación de la cinta.
- `src/transition.py`: modelo y carga de transiciones.
- `src/parser.py`: parser/validador de archivos `.txt` de MT.
- `src/examples.py`: ejemplos predefinidos (`decidible`, `computable`, `indecidible`).
- `ejemplos/*.txt`: definiciones listas para probar.

## Ejemplos incluidos
En la UI (modo “Ejemplos Predefinidos”):
- Incremento Binario (`decidible`)
- Detector de Palíndromos (`decidible`)
- Suma Unaria, Multiplicación Binaria, Copiar Cadena (`computable`)
- Bucle Infinito (`indecidible`: ilustra no-terminación/timeout)

## Uso rápido
1. Selecciona modo:
   - **Ejemplos Predefinidos**: elige un ejemplo y carga la máquina con la entrada deseada.
   - **Cargar Archivo**: sube un `.txt` con la definición; la app valida y carga la MT.
2. Controles: ejecutar todo, paso a paso, reiniciar y ajustar velocidad.
3. Visualizaciones: cinta con cabezal, grafo de estados (Graphviz), tabla de transiciones e historial exportable a CSV.

## Formato de archivo personalizado (`.txt`)
Secciones principales:
```
[CONFIG]
initial_state: q0
accept_states: qf
reject_states: qr
blank_symbol: _

[TRANSITIONS]
# current_state, read_symbol -> write_symbol, move_direction, next_state
q0, 1 -> 0, R, q1
q1, _ -> _, S, qf

[INPUT]
1011
```
Direcciones válidas: `L` (Left), `R` (Right), `S` (Stay).

## Notas
- El límite de pasos por defecto previene bucles infinitos; un timeout indica posible no-terminación.
- Si no se instala Graphviz, el grafo de estados no se podrá renderizar.***
