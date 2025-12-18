"""
Simulador de Máquina de Turing
Paquete principal con todos los componentes
"""

from .turing_machine import TuringMachine
from .tape import Tape
from .transition import Transition, TransitionFunction
from .examples import get_example, get_all_examples, EXAMPLES
from .parser import parse_turing_machine_file, validate_turing_machine_file, TuringMachineParser

__version__ = "1.0.0"
__author__ = "Tu Nombre"

__all__ = [
    'TuringMachine',
    'Tape',
    'Transition',
    'TransitionFunction',
    'get_example',
    'get_all_examples',
    'EXAMPLES',
    'parse_turing_machine_file',
    'validate_turing_machine_file',
    'TuringMachineParser'
]