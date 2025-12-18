# Módulo principal de la Máquina de Turing

from .tape import Tape
from .transition import TransitionFunction
import copy


class TuringMachine:
    # Implementación completa de una Máquina de Turing
 
    def __init__(self, name="Máquina de Turing", description=""):
        #Inicializa la Máquina de Turing
        self.name = name
        self.description = description
        
        # Componentes de la MT
        self.tape = None
        self.transition_function = TransitionFunction()
        self.current_state = None
        self.initial_state = None
        self.accept_states = set()
        self.reject_states = set()
        self.blank_symbol = '_'
        
        # Control de ejecución
        self.step_count = 0
        self.is_halted = False
        self.is_accepted = False
        self.is_rejected = False
        self.history = []
        
        # Configuración
        self.max_steps = 10000  # Prevenir bucles infinitos
    
    def configure(self, initial_state, accept_states, reject_states=None, blank_symbol='_'):
        #Configura los estados de la máquina   
        self.initial_state = initial_state
        self.current_state = initial_state
        self.accept_states = set(accept_states) if isinstance(accept_states, list) else {accept_states}
        self.reject_states = set(reject_states) if reject_states else set()
        self.blank_symbol = blank_symbol
    
    def load_tape(self, initial_content):
        #Carga la cinta con contenido inicial
        if isinstance(initial_content, str):
            initial_content = list(initial_content)
        
        self.tape = Tape(initial_content, self.blank_symbol)
    
    def add_transition(self, current_state, read_symbol, write_symbol, move_direction, next_state):
        #Agrega una transición a la máquina
        self.transition_function.add_transition(
            current_state, read_symbol, write_symbol, move_direction, next_state
        )
    
    def load_transitions_from_dict(self, transitions_dict):
        #Carga transiciones desde un diccionario
        self.transition_function.load_from_dict(transitions_dict)
    
    def step(self):
        #Ejecuta un paso de la máquina
        if self.is_halted:
            return False
        
        # Guardar estado actual en historial
        self._save_to_history()
        
        # Leer símbolo actual
        current_symbol = self.tape.read()
        
        # Buscar transición
        transition = self.transition_function.get_transition(self.current_state, current_symbol)
        
        if transition is None:
            # No hay transición definida - la máquina se detiene
            self.is_halted = True
            
            # Verificar si está en estado de aceptación o rechazo
            if self.current_state in self.accept_states:
                self.is_accepted = True
            elif self.current_state in self.reject_states:
                self.is_rejected = True
            
            return False
        
        # Ejecutar transición
        self.tape.write(transition.write_symbol)
        
        if transition.move_direction == 'L':
            self.tape.move_left()
        elif transition.move_direction == 'R':
            self.tape.move_right()
        # 'S' (Stay) no mueve el cabezal
        
        self.current_state = transition.next_state
        self.step_count += 1
        
        # Verificar estados finales
        if self.current_state in self.accept_states:
            self.is_halted = True
            self.is_accepted = True
            return False
        elif self.current_state in self.reject_states:
            self.is_halted = True
            self.is_rejected = True
            return False
        
        # Prevenir bucles infinitos
        if self.step_count >= self.max_steps:
            self.is_halted = True
            return False
        
        return True
    
    def run(self, max_steps=None):
        #Ejecuta la máquina hasta que se detenga
        if max_steps:
            self.max_steps = max_steps
        
        while not self.is_halted:
            can_continue = self.step()
            if not can_continue:
                break
        
        if self.is_accepted:
            return 'accepted'
        elif self.is_rejected:
            return 'rejected'
        elif self.step_count >= self.max_steps:
            return 'timeout'
        else:
            return 'halted'
    
    def reset(self, keep_tape_content=False):
        #Reinicia la máquina a su estado inicial
        if keep_tape_content and self.history:
            # Restaurar contenido inicial de la cinta
            initial_tape = self.history[0]['tape']
            self.tape.reset(initial_tape[10:initial_tape.index(self.blank_symbol, 10)])
        
        self.current_state = self.initial_state
        self.step_count = 0
        self.is_halted = False
        self.is_accepted = False
        self.is_rejected = False
        self.history = []
    
    def _save_to_history(self):
        #Guarda el estado actual en el historial
        state_snapshot = {
            'step': self.step_count,
            'state': self.current_state,
            'tape': self.tape.get_tape_content(),
            'head_position': self.tape.get_head_position(),
            'symbol': self.tape.read()
        }
        self.history.append(state_snapshot)
    
    def get_status(self):
        #Retorna el estado actual de la máquina
        return {
            'name': self.name,
            'current_state': self.current_state,
            'step_count': self.step_count,
            'is_halted': self.is_halted,
            'is_accepted': self.is_accepted,
            'is_rejected': self.is_rejected,
            'tape_content': self.tape.get_tape_content() if self.tape else [],
            'head_position': self.tape.get_head_position() if self.tape else 0,
            'current_symbol': self.tape.read() if self.tape else None
        }
    
    def get_result_string(self):
        #Retorna una descripción del resultado
        if not self.is_halted:
            return "En ejecución..."
        elif self.is_accepted:
            return "ACEPTADO ✓"
        elif self.is_rejected:
            return "RECHAZADO ✗"
        elif self.step_count >= self.max_steps:
            return "TIMEOUT (excedió pasos máximos)"
        else:
            return "DETENIDO"
    
    def __str__(self):
        return f"TuringMachine(name='{self.name}', state={self.current_state}, steps={self.step_count})"
    
    def __repr__(self):
        return str(self)