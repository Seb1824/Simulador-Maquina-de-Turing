"""
Parser para cargar Máquinas de Turing desde archivos de texto
"""

import re
from .turing_machine import TuringMachine


class TuringMachineParser:
    def __init__(self):
        self.sections = {
            'metadata': {},
            'config': {},
            'alphabet': {},
            'transitions': [],
            'input': ''
        }
        self.current_section = None
    
    def parse_file(self, file_content):
        try:
            lines = file_content.split('\n')
            self._parse_lines(lines)
            return self._create_machine()
        except Exception as e:
            raise ValueError(f"Error al parsear el archivo: {str(e)}")
    
    def _parse_lines(self, lines):
        """Procesa las líneas del archivo"""
        for line in lines:
            line = line.strip()
            
            # Ignorar líneas vacías y comentarios
            if not line or line.startswith('#'):
                continue
            
            # Detectar secciones
            if line.startswith('[') and line.endswith(']'):
                section_name = line[1:-1].lower()
                self.current_section = section_name
                continue
            
            # Procesar contenido según la sección
            self._process_line(line)
    
    def _process_line(self, line):
        """Procesa una línea según la sección actual"""
        if self.current_section == 'metadata':
            self._parse_metadata(line)
        elif self.current_section == 'config':
            self._parse_config(line)
        elif self.current_section == 'alphabet':
            self._parse_alphabet(line)
        elif self.current_section == 'transitions':
            self._parse_transition(line)
        elif self.current_section == 'input':
            self._parse_input(line)
    
    def _parse_metadata(self, line):
        """Parsea metadata: name, description"""
        if ':' in line:
            key, value = line.split(':', 1)
            self.sections['metadata'][key.strip()] = value.strip()
    
    def _parse_config(self, line):
        """Parsea configuración: estados iniciales, finales, etc."""
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            if key in ['accept_states', 'reject_states']:
                # Convertir a lista
                self.sections['config'][key] = [s.strip() for s in value.split(',')]
            else:
                self.sections['config'][key] = value
    
    def _parse_alphabet(self, line):
        """Parsea alfabetos de entrada y cinta"""
        if ':' in line:
            key, value = line.split(':', 1)
            symbols = [s.strip() for s in value.split(',')]
            self.sections['alphabet'][key.strip()] = symbols
    
    def _parse_transition(self, line):
        """
        Parsea una transición
        Formato: current_state, read_symbol -> write_symbol, move_direction, next_state
        """
        try:
            # Dividir por '->'
            if '->' not in line:
                return
            
            left, right = line.split('->')
            
            # Parte izquierda: current_state, read_symbol
            left_parts = [p.strip() for p in left.split(',')]
            if len(left_parts) != 2:
                return
            
            current_state, read_symbol = left_parts
            
            # Parte derecha: write_symbol, move_direction, next_state
            right_parts = [p.strip() for p in right.split(',')]
            if len(right_parts) != 3:
                return
            
            write_symbol, move_direction, next_state = right_parts
            
            # Validar dirección
            if move_direction.upper() not in ['L', 'R', 'S']:
                raise ValueError(f"Dirección inválida: {move_direction}. Use 'L' (Left), 'R' (Right) o 'S' (Stay)")
            
            self.sections['transitions'].append({
                'current_state': current_state,
                'read_symbol': read_symbol,
                'write_symbol': write_symbol,
                'move_direction': move_direction.upper(),
                'next_state': next_state
            })
        except Exception as e:
            raise ValueError(f"Error al parsear transición '{line}': {str(e)}")
    
    def _parse_input(self, line):
        """Parsea la cadena de entrada"""
        self.sections['input'] += line
    
    def _create_machine(self):
        """Crea la Máquina de Turing a partir de los datos parseados"""
        if 'initial_state' not in self.sections['config']:
            raise ValueError("Falta especificar initial_state en [CONFIG]")
        
        if not self.sections['transitions']:
            raise ValueError("No se definieron transiciones en [TRANSITIONS]")
        
        # Crear máquina
        name = self.sections['metadata'].get('name', 'Máquina Personalizada')
        description = self.sections['metadata'].get('description', '')
        
        tm = TuringMachine(name=name, description=description)
        
        # Configurar estados
        initial_state = self.sections['config']['initial_state']
        accept_states = self.sections['config'].get('accept_states', [])
        reject_states = self.sections['config'].get('reject_states', [])
        blank_symbol = self.sections['config'].get('blank_symbol', '_')
        
        tm.configure(
            initial_state=initial_state,
            accept_states=accept_states,
            reject_states=reject_states,
            blank_symbol=blank_symbol
        )
        
        # Agregar transiciones
        for trans in self.sections['transitions']:
            tm.add_transition(
                current_state=trans['current_state'],
                read_symbol=trans['read_symbol'],
                write_symbol=trans['write_symbol'],
                move_direction=trans['move_direction'],
                next_state=trans['next_state']
            )
        
        # Obtener input
        input_string = self.sections['input'].strip()
        
        return tm, input_string
    
    def validate_file(self, file_content):
        """
        Valida que el archivo tenga el formato correcto
        """
        errors = []
        
        # Verificar secciones requeridas
        required_sections = ['[CONFIG]', '[TRANSITIONS]']
        for section in required_sections:
            if section not in file_content:
                errors.append(f"Falta la sección requerida: {section}")
        
        # Verificar campos en CONFIG
        if '[CONFIG]' in file_content:
            if 'initial_state:' not in file_content:
                errors.append("Falta especificar 'initial_state' en [CONFIG]")
        
        return len(errors) == 0, errors


def parse_turing_machine_file(file_content):
    parser = TuringMachineParser()
    return parser.parse_file(file_content)


def validate_turing_machine_file(file_content):
    parser = TuringMachineParser()
    return parser.validate_file(file_content)