"""
the parser for the assembler
"""
from enum import Enum
from .symbol_table import SymbolTable
from .utils import is_integer

class InstructionType(Enum):
    A_INSTRUCTION = 0
    C_INSTRUCTION = 1
    L_INSTRUCTION = 2
    
    
class Parser:
    """
    the parser class
    """
    def __init__(self, file_name):
        self.file_name = file_name
        self._currentInstructionIndex:int = 0
        self._currentInstruction:str = None
        self._instructions = []
        self.symbol_table = SymbolTable()
        
        # delete comments and empty lines
        with open(self.file_name) as f:
            lines = f.read().split('\n')
            for line in lines:
                if '//' in line:
                    line = line[:line.index('//')]
                line = line.strip()
                if len(line) > 0:
                    self._instructions.append(line)
        
        # delete all label decelerations (xxx), and add them to the symbol table
        instructions_without_label_decelerations = []
        for line in self._instructions:
            if line.startswith('('):
                if self.symbol_table.contains(line[1:-1]) is False:
                    self.symbol_table.addEntry(line[1:-1], len(instructions_without_label_decelerations))
            else:
                instructions_without_label_decelerations.append(line)
        
        self._instructions = instructions_without_label_decelerations        
        
        # add all variables that appear in "@xxx" to the symbol table
        # Caution: "xxx" in "@xxx" can be a variable or a label or an integer
        allocated_variable_address = 16
        for line in self._instructions:
            if line.startswith('@'):
                if is_integer(line[1:]) or self.symbol_table.contains(line[1:]):
                    continue
                # Now we can be sure that "xxx" in "@xxx" is a variable, NOT a label or an integer
                self.symbol_table.addEntry(line[1:], allocated_variable_address)
                allocated_variable_address += 1
        
        print(self._instructions)
        print(self.symbol_table.symbol_table)
               
            
    def hasMoreLines(self):
        """
        check if there are more lines to parse
        :return: True if there is a next line, False otherwise
        """
        return len(self._instructions) > self._currentInstructionIndex


    def currentInstructionIndex(self) -> int:
        """
        get the current instruction index
        :return: the current instruction index
        """
        return self._currentInstructionIndex
    
    
    def advance(self) -> str:
        """
        advance to the next line and return it
        :return: the next line
        """
        if self.hasMoreLines():
            self._currentInstruction = self._instructions[self._currentInstructionIndex]
            self._currentInstructionIndex += 1
            return self._currentInstruction
        else:
            return None
        
          
    def instructionType(self) -> InstructionType:
        """
        get the instruction type of the current line
        :return: the instruction type
        """
        if self._currentInstruction.startswith('@'):
            return InstructionType.A_INSTRUCTION
        elif self._currentInstruction.startswith('('):
            return InstructionType.L_INSTRUCTION
        else:
            return InstructionType.C_INSTRUCTION
        
    def symbol(self) -> str:
        """
        get the symbol of the current line
        :return: the symbol
        """
        if self.instructionType() == InstructionType.A_INSTRUCTION:
            # @xxx
            return self._currentInstruction[1:]
        elif self.instructionType() == InstructionType.L_INSTRUCTION:
            # (xxx)
            return self._currentInstruction[1:-1]
        else:
            return None
        
    def dest(self) -> str:
        """
        get the dest of the current line
        :return: the dest
        """
        if self.instructionType() == InstructionType.C_INSTRUCTION:
            # dest=comp;jump
            parts = self._currentInstruction.split('=')
            return parts[0].strip() if len(parts) == 2 else None
        else:
            return None
        
    def comp(self) -> str:
        """
        get the comp of the current line
        :return: the comp
        """
        if self.instructionType() == InstructionType.C_INSTRUCTION:
            # dest=comp;jump
            parts = self._currentInstruction.split('=')
            if len(parts) == 2:
                return parts[1].split(';')[0].strip()
            else:
                return parts[0].split(';')[0].strip()        
        else:
            return None
        
    def jump(self) -> str:
        """
        get the jump of the current line
        :return: the jump
        """
        if self.instructionType() == InstructionType.C_INSTRUCTION:
            # dest=comp;jump
            parts = self._currentInstruction.split(';')
            return parts[1].strip() if len(parts) == 2 else None
        else:
            return None
        