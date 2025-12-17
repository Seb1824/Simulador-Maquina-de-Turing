def parse_input():
    # Aquí puedes definir las reglas de transición o parsear entradas
    # Por ejemplo, una lista de transiciones como tuplas (estado actual, símbolo leído, siguiente estado, símbolo escrito, movimiento)
    transitions = [
        ("q0", "0", "q0", "0", 'R'),
        ("q0", "1", "q0", "1", 'R'),
        ("q0", " ", "q_accept", " ", 'R')
    ]
    return transitions
