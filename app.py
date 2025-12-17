import streamlit as st
from turing_machine import TuringMachine
from parser import parse_input

# Función principal de Streamlit
def run_simulator():
    st.title("Simulador de Máquina de Turing")
    
    tape_input = st.text_input("Introduce la cadena de entrada:", "0101")
    max_steps = st.slider("Máximo número de pasos:", 1, 1000, 100)
    
    # Procesamos las reglas de la máquina de Turing desde una entrada o archivo
    transitions = parse_input()
    
    # Inicializamos la máquina de Turing
    machine = TuringMachine(tape=tape_input)
    for state, symbol, next_state, write_symbol, move in transitions:
        machine.set_transition(state, symbol, next_state, write_symbol, move)
    
    if st.button("Ejecutar Máquina de Turing"):
        result, final_state = machine.run(max_steps)
        st.write(f"Cadena final: {result}")
        st.write(f"Estado final: {final_state}")
        st.text("Cinta actual: " + ''.join(machine.tape))

# Ejecutar el simulador
if __name__ == "__main__":
    run_simulator()
