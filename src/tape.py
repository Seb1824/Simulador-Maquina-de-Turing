#Módulo para manejar la cinta de la Máquina de Turing

class Tape:

    #Representa la cinta infinita de la Máquina de Turing

    def __init__(self, initial_content=None, blank_symbol='_'):
        #Inicializa la cinta
        self.blank_symbol = blank_symbol
        
        if initial_content:
            # Agregar espacios en blanco alrededor del contenido inicial
            self.tape = [blank_symbol] * 10 + list(initial_content) + [blank_symbol] * 10
            self.head_position = 10  # Posición inicial en el contenido
        else:
            self.tape = [blank_symbol] * 20
            self.head_position = 10
    
    def read(self):
        #Lee el símbolo en la posición actual del cabezal
        return self.tape[self.head_position]
    
    def write(self, symbol):

        #Escribe un símbolo en la posición actual
        self.tape[self.head_position] = symbol
    
    def move_left(self):
        #Mueve el cabezal una posición a la izquierda
        self.head_position -= 1
        
        # Extender la cinta si es necesario
        if self.head_position < 0:
            self.tape.insert(0, self.blank_symbol)
            self.head_position = 0
    
    def move_right(self):
        #Mueve el cabezal una posición a la derecha
        self.head_position += 1
        
        # Extender la cinta si es necesario
        if self.head_position >= len(self.tape):
            self.tape.append(self.blank_symbol)
    
    def get_tape_content(self):
        #Retorna el contenido actual de la cinta
        return self.tape.copy()
    
    def get_head_position(self):
        #Retorna la posición actual del cabezal
        return self.head_position
    
    def get_visible_tape(self, window_size=20):
        #Retorna una ventana visible de la cinta centrada en el cabezal
        half_window = window_size // 2
        start = max(0, self.head_position - half_window)
        end = min(len(self.tape), self.head_position + half_window)
        
        # Asegurar que siempre tengamos el tamaño de ventana completo
        if end - start < window_size:
            if start == 0:
                end = min(len(self.tape), start + window_size)
            else:
                start = max(0, end - window_size)
        
        visible = self.tape[start:end]
        relative_pos = self.head_position - start
        
        return visible, relative_pos, start
    
    def reset(self, initial_content=None):
        # Reinicia la cinta a su estado inicial
        if initial_content:
            self.tape = [self.blank_symbol] * 10 + list(initial_content) + [self.blank_symbol] * 10
        else:
            self.tape = [self.blank_symbol] * 20
        self.head_position = 10
    
    def __str__(self):
        #Representación en string de la cinta
        tape_str = ''.join(self.tape)
        pointer = ' ' * self.head_position + '^'
        return f"{tape_str}\n{pointer}"
    
    def __repr__(self):
        return f"Tape(position={self.head_position}, content={self.tape})"