#Módulo para manejar las transiciones de la Máquina de Turing

class Transition:
    #Representa una transición individual en la Máquina de Turing

    def __init__(self, current_state, read_symbol, write_symbol, move_direction, next_state):
        #Inicializa una transición
        self.current_state = current_state
        self.read_symbol = read_symbol
        self.write_symbol = write_symbol
        self.move_direction = move_direction.upper()
        self.next_state = next_state
        
        # Validar dirección
        if self.move_direction not in ['L', 'R', 'S']:
            raise ValueError(f"Dirección inválida: {move_direction}. Use 'L' (Left), 'R' (Right) o 'S' (Stay)")
    
    def __str__(self):
        return f"δ({self.current_state}, {self.read_symbol}) = ({self.next_state}, {self.write_symbol}, {self.move_direction})"
    
    def __repr__(self):
        return f"Transition({self.current_state}, {self.read_symbol}, {self.write_symbol}, {self.move_direction}, {self.next_state})"
    
    def to_dict(self):
        #Convierte la transición a diccionario
        return {
            'current_state': self.current_state,
            'read_symbol': self.read_symbol,
            'write_symbol': self.write_symbol,
            'move_direction': self.move_direction,
            'next_state': self.next_state
        }


class TransitionFunction:
    #Función de transición completa de la Máquina de Turing
    
    def __init__(self):
        #Inicializa la función de transición vacía
        # Estructura: {(estado, símbolo): Transition}
        self.transitions = {}
    
    def add_transition(self, current_state, read_symbol, write_symbol, move_direction, next_state):
        #Agrega una transición a la función
        transition = Transition(current_state, read_symbol, write_symbol, move_direction, next_state)
        key = (current_state, read_symbol)
        self.transitions[key] = transition
    
    def get_transition(self, current_state, read_symbol):
        #Obtiene la transición para un estado y símbolo dados
        key = (current_state, read_symbol)
        return self.transitions.get(key, None)
    
    def has_transition(self, current_state, read_symbol):
        #Verifica si existe una transición para el estado y símbolo dados
        key = (current_state, read_symbol)
        return key in self.transitions
    
    def get_all_transitions(self):
        #Retorna todas las transiciones como lista
        return list(self.transitions.values())
    
    def get_states(self):
        #Retorna el conjunto de todos los estados
        states = set()
        for transition in self.transitions.values():
            states.add(transition.current_state)
            states.add(transition.next_state)
        return states
    
    def get_symbols(self):
        #Retorna el conjunto de todos los símbolos
        symbols = set()
        for transition in self.transitions.values():
            symbols.add(transition.read_symbol)
            symbols.add(transition.write_symbol)
        return symbols
    
    def to_table(self):
        #Convierte las transiciones a una tabla legible
        table = []
        for transition in self.transitions.values():
            table.append(transition.to_dict())
        return table
    
    def load_from_dict(self, transitions_dict):
        #Carga transiciones desde un diccionario
        self.transitions.clear()
        
        for state, symbol_dict in transitions_dict.items():
            for symbol, trans_data in symbol_dict.items():
                self.add_transition(
                    current_state=state,
                    read_symbol=symbol,
                    write_symbol=trans_data['write'],
                    move_direction=trans_data['move'],
                    next_state=trans_data['next_state']
                )
    
    def __str__(self):
        result = "Función de Transición:\n"
        for transition in self.transitions.values():
            result += f"  {transition}\n"
        return result
    
    def __repr__(self):
        return f"TransitionFunction(transitions={len(self.transitions)})"