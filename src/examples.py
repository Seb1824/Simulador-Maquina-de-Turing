# Módulo con ejemplos predefinidos de Máquinas de Turing

from .turing_machine import TuringMachine

def create_binary_increment():
    tm = TuringMachine(
        name="Incremento Binario",
        description="Suma 1 a un número binario"
    )
    
    # Configurar estados
    tm.configure(
        initial_state='q0',
        accept_states=['qf'],
        blank_symbol='_'
    )
    
    # Transiciones
    transitions = {
        'q0': {  # Mover al final del número
            '0': {'write': '0', 'move': 'R', 'next_state': 'q0'},
            '1': {'write': '1', 'move': 'R', 'next_state': 'q0'},
            '': {'write': '', 'move': 'L', 'next_state': 'q1'}
        },
        'q1': {  # Incrementar de derecha a izquierda
            '0': {'write': '1', 'move': 'S', 'next_state': 'qf'},
            '1': {'write': '0', 'move': 'L', 'next_state': 'q1'},
            '_': {'write': '1', 'move': 'S', 'next_state': 'qf'}
        }
    }
    
    tm.load_transitions_from_dict(transitions)
    
    return tm


def create_palindrome_checker():
    tm = TuringMachine(
        name="Detector de Palíndromos",
        description="Verifica si una cadena es palíndromo"
    )
    
    tm.configure(
        initial_state='q0',
        accept_states=['qa'],
        reject_states=['qr'],
        blank_symbol='_'
    )
    
    transitions = {
        'q0': {  # Estado inicial - marcar primer símbolo
            'a': {'write': '_', 'move': 'R', 'next_state': 'q1'},
            'b': {'write': '_', 'move': 'R', 'next_state': 'q2'},
            '': {'write': '', 'move': 'S', 'next_state': 'qa'}  # Cadena vacía es palíndromo
        },
        'q1': {  # Marcamos 'a', buscamos 'a' al final
            'a': {'write': 'a', 'move': 'R', 'next_state': 'q1'},
            'b': {'write': 'b', 'move': 'R', 'next_state': 'q1'},
            '': {'write': '', 'move': 'L', 'next_state': 'q3'}
        },
        'q2': {  # Marcamos 'b', buscamos 'b' al final
            'a': {'write': 'a', 'move': 'R', 'next_state': 'q2'},
            'b': {'write': 'b', 'move': 'R', 'next_state': 'q2'},
            '': {'write': '', 'move': 'L', 'next_state': 'q4'}
        },
        'q3': {  # Verificar que el último símbolo sea 'a'
            'a': {'write': '_', 'move': 'L', 'next_state': 'q5'},
            '': {'write': '', 'move': 'S', 'next_state': 'qa'},  # Un solo carácter
            'b': {'write': 'b', 'move': 'S', 'next_state': 'qr'}
        },
        'q4': {  # Verificar que el último símbolo sea 'b'
            'b': {'write': '_', 'move': 'L', 'next_state': 'q5'},
            '': {'write': '', 'move': 'S', 'next_state': 'qa'},  # Un solo carácter
            'a': {'write': 'a', 'move': 'S', 'next_state': 'qr'}
        },
        'q5': {  # Regresar al inicio
            'a': {'write': 'a', 'move': 'L', 'next_state': 'q5'},
            'b': {'write': 'b', 'move': 'L', 'next_state': 'q5'},
            '': {'write': '', 'move': 'R', 'next_state': 'q0'}
        }
    }
    
    tm.load_transitions_from_dict(transitions)
    
    return tm


def create_unary_addition():
    tm = TuringMachine(
        name="Suma Unaria",
        description="Suma dos números en notación unaria (111+11=11111)"
    )
    
    tm.configure(
        initial_state='q0',
        accept_states=['qf'],
        blank_symbol='_'
    )
    
    transitions = {
        'q0': {  # Buscar el signo '+'
            '1': {'write': '1', 'move': 'R', 'next_state': 'q0'},
            '+': {'write': '1', 'move': 'R', 'next_state': 'q1'},
            '': {'write': '', 'move': 'S', 'next_state': 'qf'}
        },
        'q1': {  # Ir al final del segundo número
            '1': {'write': '1', 'move': 'R', 'next_state': 'q1'},
            '': {'write': '', 'move': 'L', 'next_state': 'q2'}
        },
        'q2': {  # Borrar el último '1' del segundo número
            '1': {'write': '_', 'move': 'S', 'next_state': 'qf'}
        }
    }
    
    tm.load_transitions_from_dict(transitions)
    
    return tm


def create_binary_multiplication():
    tm = TuringMachine(
        name="Multiplicación Binaria",
        description="Multiplica dos números binarios (simplificado)"
    )
    
    tm.configure(
        initial_state='q0',
        accept_states=['qf'],
        blank_symbol='_'
    )
    
    transitions = {
        'q0': {  # Estado inicial
            '0': {'write': '0', 'move': 'R', 'next_state': 'q0'},
            '1': {'write': '1', 'move': 'R', 'next_state': 'q0'},
            '': {'write': '', 'move': 'R', 'next_state': 'q1'},
            '': {'write': '', 'move': 'S', 'next_state': 'qf'}
        },
        'q1': {  # Leer segundo número
            '0': {'write': '0', 'move': 'R', 'next_state': 'q1'},
            '1': {'write': '1', 'move': 'R', 'next_state': 'q1'},
            '': {'write': '', 'move': 'S', 'next_state': 'qf'}
        }
    }
    
    tm.load_transitions_from_dict(transitions)
    
    return tm


def create_copy_string():
    tm = TuringMachine(
        name="Copiar Cadena",
        description="Copia una cadena y la duplica con un separador"
    )
    
    tm.configure(
        initial_state='q0',
        accept_states=['qf'],
        blank_symbol='_'
    )
    
    transitions = {
        'q0': {  # Marcar primer carácter
            'a': {'write': 'A', 'move': 'R', 'next_state': 'q1'},
            'b': {'write': 'B', 'move': 'R', 'next_state': 'q2'},
            'c': {'write': 'C', 'move': 'R', 'next_state': 'q3'},
            '': {'write': '', 'move': 'S', 'next_state': 'qf'}
        },
        'q1': {  # Copiar 'a'
            'a': {'write': 'a', 'move': 'R', 'next_state': 'q1'},
            'b': {'write': 'b', 'move': 'R', 'next_state': 'q1'},
            'c': {'write': 'c', 'move': 'R', 'next_state': 'q1'},
            '_': {'write': 'a', 'move': 'L', 'next_state': 'q4'}
        },
        'q2': {  # Copiar 'b'
            'a': {'write': 'a', 'move': 'R', 'next_state': 'q2'},
            'b': {'write': 'b', 'move': 'R', 'next_state': 'q2'},
            'c': {'write': 'c', 'move': 'R', 'next_state': 'q2'},
            '_': {'write': 'b', 'move': 'L', 'next_state': 'q4'}
        },
        'q3': {  # Copiar 'c'
            'a': {'write': 'a', 'move': 'R', 'next_state': 'q3'},
            'b': {'write': 'b', 'move': 'R', 'next_state': 'q3'},
            'c': {'write': 'c', 'move': 'R', 'next_state': 'q3'},
            '_': {'write': 'c', 'move': 'L', 'next_state': 'q4'}
        },
        'q4': {  # Regresar al inicio
            'a': {'write': 'a', 'move': 'L', 'next_state': 'q4'},
            'b': {'write': 'b', 'move': 'L', 'next_state': 'q4'},
            'c': {'write': 'c', 'move': 'L', 'next_state': 'q4'},
            'A': {'write': 'a', 'move': 'R', 'next_state': 'q0'},
            'B': {'write': 'b', 'move': 'R', 'next_state': 'q0'},
            'C': {'write': 'c', 'move': 'R', 'next_state': 'q0'}
        }
    }
    
    tm.load_transitions_from_dict(transitions)
    
    return tm


# Diccionario de ejemplos 
EXAMPLES = {
    'binary_increment': {
        'name': 'Incremento Binario',
        'description': 'Suma 1 a un número binario',
        'creator': create_binary_increment,
        'default_input': '1011',
        'category': 'decidible'
    },
    'palindrome': {
        'name': 'Detector de Palíndromos',
        'description': 'Verifica si una cadena es palíndromo',
        'creator': create_palindrome_checker,
        'default_input': 'abba',
        'category': 'decidible'
    },
    'unary_addition': {
        'name': 'Suma Unaria',
        'description': 'Suma dos números en notación unaria',
        'creator': create_unary_addition,
        'default_input': '111+11',
        'category': 'computable'
    },
    'binary_multiplication': {
        'name': 'Multiplicación Binaria',
        'description': 'Multiplica dos números binarios',
        'creator': create_binary_multiplication,
        'default_input': '10*11',
        'category': 'computable'
    },
    'copy_string': {
        'name': 'Copiar Cadena',
        'description': 'Copia una cadena',
        'creator': create_copy_string,
        'default_input': 'abc',
        'category': 'computable'
    }
}


def get_example(example_name):
    if example_name in EXAMPLES:
        example_info = EXAMPLES[example_name]
        tm = example_info['creator']()
        default_input = example_info['default_input']
        return tm, default_input
    return None, None


def get_all_examples():
    #Retorna información de todos los ejemplos disponibles
    return EXAMPLES