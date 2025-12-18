# Aplicación Streamlit para el Simulador de Máquina de Turing

import streamlit as st
import pandas as pd
import time
import graphviz
from src.turing_machine import TuringMachine
from src.examples import get_example, get_all_examples
from src.parser import parse_turing_machine_file, validate_turing_machine_file

# Configuración de la página
st.set_page_config(
    page_title="Simulador Máquina de Turing",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
    }
    .status-accepted {
        background-color: #28a745;
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    .status-rejected {
        background-color: #dc3545;
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    .status-running {
        background-color: #007bff;
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    .status-halted {
        background-color: #ffc107;
        color: black;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    .tape-cell {
        display: inline-block;
        width: 50px;
        height: 50px;
        border: 2px solid #333;
        text-align: center;
        line-height: 50px;
        margin: 2px;
        font-family: monospace;
        font-size: 20px;
        font-weight: bold;
    }
    .tape-head {
        background-color: #ff6b6b;
        border-color: #ff0000;
        color: white;
    }
    .upload-section {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border: 2px dashed #666;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    # Inicializa las variables de sesión
    if 'tm' not in st.session_state:
        st.session_state.tm = None
    if 'is_running' not in st.session_state:
        st.session_state.is_running = False
    if 'selected_example' not in st.session_state:
        st.session_state.selected_example = 'binary_increment'
    if 'custom_input' not in st.session_state:
        st.session_state.custom_input = ''
    if 'mode' not in st.session_state:
        st.session_state.mode = 'examples'  # 'examples' o 'custom'
    if 'uploaded_file_content' not in st.session_state:
        st.session_state.uploaded_file_content = None


def create_state_graph(tm):
    # Crea el grafo de estados de la Máquina de Turing
    dot = graphviz.Digraph(comment='Máquina de Turing')
    dot.attr(rankdir='LR', size='8,5')
    
    # Configuración visual
    dot.attr('node', shape='circle', style='filled', fillcolor='lightblue')
    
    # Obtener todos los estados
    all_transitions = tm.transition_function.get_all_transitions()
    states = set()
    
    for trans in all_transitions:
        states.add(trans.current_state)
        states.add(trans.next_state)
    
    # Agregar nodos
    for state in states:
        if state == tm.initial_state:
            # Estado inicial (con flecha de entrada)
            dot.node(state, state, shape='circle', fillcolor='lightgreen', style='filled')
            dot.node('start', '', shape='none')
            dot.edge('start', state)
        elif state in tm.accept_states:
            # Estado de aceptación (doble círculo)
            dot.node(state, state, shape='doublecircle', fillcolor='lightgreen', style='filled')
        elif state in tm.reject_states:
            # Estado de rechazo
            dot.node(state, state, shape='doublecircle', fillcolor='salmon', style='filled')
        else:
            # Estado normal
            dot.node(state, state)
        
        # Resaltar estado actual
        if state == tm.current_state and not tm.is_halted:
            dot.node(state, state, fillcolor='yellow', style='filled')
    
    # Agregar transiciones
    transition_labels = {}
    
    for trans in all_transitions:
        edge_key = (trans.current_state, trans.next_state)
        label = f"{trans.read_symbol} → {trans.write_symbol}, {trans.move_direction}"
        
        if edge_key in transition_labels:
            transition_labels[edge_key] += f"\\n{label}"
        else:
            transition_labels[edge_key] = label
    
    for (src, dst), label in transition_labels.items():
        if src == dst:
            # Auto-loop
            dot.edge(src, dst, label=label, color='blue')
        else:
            dot.edge(src, dst, label=label)
    
    return dot


def render_tape(tm, window_size=20):
    # Renderiza la cinta de la máquina con el cabezal destacado
    if tm is None or tm.tape is None:
        st.warning("No hay cinta cargada")
        return
    
    visible, relative_pos, start_offset = tm.tape.get_visible_tape(window_size)
    
    # Crear HTML para la cinta
    tape_html = '<div style="display: flex; justify-content: center; flex-wrap: wrap;">'
    
    for i, symbol in enumerate(visible):
        cell_class = "tape-cell"
        if i == relative_pos:
            cell_class += " tape-head"
        
        tape_html += f'<div class="{cell_class}">{symbol if symbol != "_" else "⎵"}</div>'
    
    tape_html += '</div>'
    
    # Mostrar posición del cabezal
    tape_html += f'<div style="text-align: center; margin-top: 10px; color: #ff0000; font-weight: bold;">▲ Cabezal (Posición: {tm.tape.get_head_position()})</div>'
    
    st.markdown(tape_html, unsafe_allow_html=True)


def render_status(tm):
    # Renderiza el estado actual de la máquina
    if tm is None:
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Estado Actual", tm.current_state)
    
    with col2:
        st.metric("Posición Cabezal", tm.tape.get_head_position())
    
    with col3:
        st.metric("Pasos Ejecutados", tm.step_count)
    
    with col4:
        status_text = tm.get_result_string()
        if tm.is_accepted:
            st.markdown(f'<div class="status-accepted">{status_text}</div>', unsafe_allow_html=True)
        elif tm.is_rejected:
            st.markdown(f'<div class="status-rejected">{status_text}</div>', unsafe_allow_html=True)
        elif tm.is_halted:
            st.markdown(f'<div class="status-halted">{status_text}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="status-running">EJECUTANDO...</div>', unsafe_allow_html=True)


def render_transition_table(tm):
    # Renderiza la tabla de transiciones
    if tm is None:
        return
    
    transitions = tm.transition_function.get_all_transitions()
    
    if not transitions:
        st.warning("No hay transiciones definidas")
        return
    
    data = []
    current_symbol = tm.tape.read() if tm.tape else None
    
    for trans in transitions:
        is_current = (trans.current_state == tm.current_state and 
                     trans.read_symbol == current_symbol and 
                     not tm.is_halted)
        
        data.append({
            '🎯': '→' if is_current else '',
            'Estado Actual': trans.current_state,
            'Lee': trans.read_symbol,
            'Escribe': trans.write_symbol,
            'Mueve': trans.move_direction,
            'Siguiente Estado': trans.next_state
        })
    
    df = pd.DataFrame(data)
    
    # Aplicar estilo
    def highlight_current(row):
        if row['🎯'] == '→':
            return ['background-color: yellow'] * len(row)
        return [''] * len(row)
    
    styled_df = df.style.apply(highlight_current, axis=1)
    st.dataframe(styled_df, use_container_width=True, hide_index=True)


def generate_example_file():
    # Genera un archivo de ejemplo para descarga
    example_content = """# Máquina de Turing - Archivo de Ejemplo
# Este es un ejemplo de incremento binario

[METADATA]
name: Incremento Binario Personalizado
description: Suma 1 a un número binario

[CONFIG]
initial_state: q0
accept_states: qf
reject_states: 
blank_symbol: _

[ALPHABET]
input: 0, 1
tape: 0, 1, _

[TRANSITIONS]
# Formato: current_state, read_symbol -> write_symbol, move_direction, next_state
# Mover al final del número
q0, 0 -> 0, R, q0
q0, 1 -> 1, R, q0
q0, _ -> _, L, q1
# Incrementar de derecha a izquierda
q1, 1 -> 0, L, q1
q1, 0 -> 1, S, qf
q1, _ -> 1, S, qf

[INPUT]
1011
"""
    return example_content


def main():
    # Función principal de la aplicación
    initialize_session_state()
    
    # Título
    st.title("🖥️ Simulador de Máquina de Turing")
    st.markdown("---")
    
    # Sidebar - Controles
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        # Selector de modo
        mode = st.radio(
            "Modo de Operación",
            options=['examples', 'custom'],
            format_func=lambda x: "📚 Ejemplos Predefinidos" if x == 'examples' else "📁 Cargar Archivo Personalizado",
            key='mode_selector'
        )
        
        st.session_state.mode = mode
        
        st.markdown("---")
        
        # MODO: EJEMPLOS PREDEFINIDOS
        if mode == 'examples':
            examples = get_all_examples()
            example_names = {key: info['name'] for key, info in examples.items()}
            
            selected = st.selectbox(
                "Seleccionar Ejemplo",
                options=list(example_names.keys()),
                format_func=lambda x: example_names[x],
                key='example_selector'
            )
            
            if selected != st.session_state.selected_example:
                st.session_state.selected_example = selected
                st.session_state.is_running = False
            
            # Mostrar descripción
            st.info(examples[selected]['description'])
            st.caption(f"**Categoría:** {examples[selected]['category'].upper()}")
            
            # Input personalizado
            st.markdown("---")
            st.subheader("📝 Entrada")
            
            default_input = examples[selected]['default_input']
            custom_input = st.text_input(
                "Cadena de entrada",
                value=default_input,
                help="Ingrese la cadena a procesar"
            )
            
            # Botón para cargar máquina
            if st.button("🔄 Cargar Máquina", use_container_width=True, type="primary"):
                tm, _ = get_example(selected)
                if tm:
                    tm.load_tape(custom_input)
                    st.session_state.tm = tm
                    st.session_state.is_running = False
                    st.success("✅ Máquina cargada correctamente")
                else:
                    st.error("❌ Error al cargar la máquina")
        
        # MODO: CARGAR ARCHIVO PERSONALIZADO
        else:
            st.subheader("📁 Cargar Archivo")
            
            # Botón para descargar ejemplo
            example_file = generate_example_file()
            st.download_button(
                label="📥 Descargar Archivo de Ejemplo",
                data=example_file,
                file_name="ejemplo_maquina_turing.txt",
                mime="text/plain",
                use_container_width=True
            )
            
            st.markdown("---")
            
            # Upload de archivo
            uploaded_file = st.file_uploader(
                "Seleccione un archivo .txt",
                type=['txt'],
                help="Cargue un archivo con la definición de la Máquina de Turing"
            )
            
            if uploaded_file is not None:
                try:
                    # Leer contenido del archivo
                    file_content = uploaded_file.read().decode('utf-8')
                    st.session_state.uploaded_file_content = file_content
                    
                    # Validar archivo
                    is_valid, errors = validate_turing_machine_file(file_content)
                    
                    if not is_valid:
                        st.error("❌ El archivo tiene errores:")
                        for error in errors:
                            st.write(f"- {error}")
                    else:
                        st.success("✅ Archivo válido")
                        
                        # Mostrar preview del archivo
                        with st.expander("👁️ Ver contenido del archivo"):
                            st.code(file_content, language='text')
                        
                        # Botón para cargar la máquina
                        if st.button("🔄 Cargar Máquina desde Archivo", use_container_width=True, type="primary"):
                            try:
                                tm, input_string = parse_turing_machine_file(file_content)
                                
                                if tm:
                                    if input_string:
                                        tm.load_tape(input_string)
                                    else:
                                        tm.load_tape('_')  # Cinta vacía por defecto
                                    
                                    st.session_state.tm = tm
                                    st.session_state.is_running = False
                                    st.success(f"✅ Máquina '{tm.name}' cargada correctamente")
                                    st.rerun()
                                else:
                                    st.error("❌ Error al crear la máquina")
                            except Exception as e:
                                st.error(f"❌ Error al parsear el archivo: {str(e)}")
                
                except Exception as e:
                    st.error(f"❌ Error al leer el archivo: {str(e)}")
            
            # Información sobre el formato
            with st.expander("ℹ️ Formato del Archivo"):
                st.markdown("""
                **Secciones requeridas:**
                - `[CONFIG]` - Configuración de estados
                - `[TRANSITIONS]` - Definición de transiciones
                
                **Secciones opcionales:**
                - `[METADATA]` - Nombre y descripción
                - `[ALPHABET]` - Alfabetos de entrada y cinta
                - `[INPUT]` - Cadena de entrada por defecto
                
                **Ejemplo de transición:**
                ```
                q0, 1 -> 0, R, q1
                ```
                Significa: En estado q0, si lee 1, escribe 0, mueve a la derecha (R), va a q1
                
                **Direcciones válidas:**
                - `L` = Left (Izquierda)
                - `R` = Right (Derecha)
                - `S` = Stay (Quedarse/No mover)
                """)
        
        # Controles de ejecución (comunes para ambos modos)
        st.markdown("---")
        st.subheader("🎮 Controles")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("▶️ Ejecutar Todo", use_container_width=True, type="primary"):
                if st.session_state.tm:
                    result = st.session_state.tm.run(max_steps=1000)
                    st.rerun()
        
        with col2:
            if st.button("⏭️ Paso", use_container_width=True):
                if st.session_state.tm and not st.session_state.tm.is_halted:
                    st.session_state.tm.step()
                    st.rerun()
        
        if st.button("🔄 Reiniciar", use_container_width=True):
            if st.session_state.tm:
                st.session_state.tm.reset(keep_tape_content=True)
                st.session_state.is_running = False
                st.rerun()
        
        # Velocidad de ejecución
        st.markdown("---")
        speed = st.slider(
            "Velocidad (pasos/seg)",
            min_value=1,
            max_value=10,
            value=2,
            help="Velocidad de ejecución automática"
        )
        
        # Información adicional
        st.markdown("---")
        st.markdown("### ℹ️ Información")
        st.markdown("""
        **Símbolos especiales:**
        - `_` : Espacio en blanco
        - `⎵` : Espacio en blanco (visual)
        
        **Movimientos:**
        - `L` : Left (Izquierda)
        - `R` : Right (Derecha)
        - `S` : Stay (Quedarse/No mover)
        """)
    
    # Área principal
    if st.session_state.tm is None:
        st.info("👈 Seleccione un ejemplo o cargue un archivo para comenzar")
        
        # Mostrar instrucciones
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📚 Ejemplos Predefinidos")
            st.markdown("""
            1. Seleccione el modo "Ejemplos Predefinidos"
            2. Elija un ejemplo del menú
            3. Modifique la entrada si lo desea
            4. Presione "Cargar Máquina"
            5. Use los controles para ejecutar
            """)
        
        with col2:
            st.markdown("### 📁 Archivo Personalizado")
            st.markdown("""
            1. Descargue el archivo de ejemplo
            2. Modifique según sus necesidades
            3. Seleccione el modo "Cargar Archivo"
            4. Suba su archivo .txt
            5. Presione "Cargar Máquina desde Archivo"
            """)
        
        return
    
    tm = st.session_state.tm
    
    # Mostrar información de la máquina cargada
    st.info(f"**Máquina cargada:** {tm.name} - {tm.description}")
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Visualización", "🔗 Grafo de Estados", "📋 Transiciones", "📚 Historial"])
    
    with tab1:
        st.subheader("Estado Actual de la Máquina")
        render_status(tm)
        
        st.markdown("---")
        st.subheader("Cinta de la Máquina")
        render_tape(tm, window_size=25)
        
        # Información adicional
        if tm.tape:
            with st.expander("ℹ️ Información de la Cinta"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Símbolo actual:**", tm.tape.read())
                    st.write("**Longitud de la cinta:**", len(tm.tape.get_tape_content()))
                with col2:
                    st.write("**Estado:**", tm.current_state)
                    st.write("**Resultado:**", tm.get_result_string())
    
    with tab2:
        st.subheader("Grafo de Estados de la Máquina de Turing")
        
        try:
            graph = create_state_graph(tm)
            st.graphviz_chart(graph)
            
            # Leyenda
            with st.expander("📖 Leyenda del Grafo"):
                st.markdown("""
                - **Verde claro**: Estado inicial
                - **Doble círculo verde**: Estado de aceptación
                - **Doble círculo rojo**: Estado de rechazo
                - **Amarillo**: Estado actual (durante ejecución)
                - **Flecha azul**: Auto-transición (loop)
                - **Etiquetas**: `símbolo_leído → símbolo_escrito, dirección`
                """)
        except Exception as e:
            st.error(f"Error al generar el grafo: {str(e)}")
            st.info("Asegúrese de tener Graphviz instalado en su sistema")
    
    with tab3:
        st.subheader("Tabla de Transiciones")
        render_transition_table(tm)
        
        # Estadísticas
        with st.expander("📊 Estadísticas"):
            transitions = tm.transition_function.get_all_transitions()
            states = tm.transition_function.get_states()
            symbols = tm.transition_function.get_symbols()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Estados", len(states))
            with col2:
                st.metric("Total de Símbolos", len(symbols))
            with col3:
                st.metric("Total de Transiciones", len(transitions))
    
    with tab4:
        st.subheader("Historial de Ejecución")
        
        if tm.history:
            history_data = []
            for i, snapshot in enumerate(tm.history):
                history_data.append({
                    'Paso': snapshot['step'],
                    'Estado': snapshot['state'],
                    'Posición': snapshot['head_position'],
                    'Símbolo': snapshot['symbol']
                })
            
            df_history = pd.DataFrame(history_data)
            st.dataframe(df_history, use_container_width=True, hide_index=True)
            
            # Botón para exportar historial
            csv = df_history.to_csv(index=False)
            st.download_button(
                label="📥 Descargar Historial (CSV)",
                data=csv,
                file_name="historial_turing.csv",
                mime="text/csv"
            )
        else:
            st.info("No hay historial disponible. Ejecute la máquina para ver el historial.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>Simulador de Máquina de Turing - Laboratorio N°12</p>
        <p>Desarrollado para el curso de Teoría de la Computación</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()