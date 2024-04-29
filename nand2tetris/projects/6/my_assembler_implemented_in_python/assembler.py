"""
This is a Python implementation of the Hack assembler.

Relative imports only work when the module is being run as a part of a package. 
If you try to run a script containing relative imports directly (e.g., python script.py), 
it might not work as expected. Instead, you should run the script as a module within a package 
(e.g., python -m mypackage.script
"""

from .parser import Parser, InstructionType
from .code_generator import CodeGenerator
from .utils import is_integer


class Assembler:
    def __init__(self, file_name: str):
        self.parser = Parser(file_name)
        self.code_generator = CodeGenerator()
        self.output_file = file_name.replace('.asm', '.hack')
        self.output_binary_code = []
        
                
    def assemble(self):
        while self.parser.hasMoreLines():
            instruction = self.parser.advance()
            # print(instruction)
            instruction_type = self.parser.instructionType()
            if instruction_type == InstructionType.A_INSTRUCTION:
                # @xxx
                symbol = self.parser.symbol()
                if is_integer(symbol):
                    address = int(symbol)
                elif self.parser.symbol_table.contains(symbol):
                    address = self.parser.symbol_table.getAddress(symbol)
                else:
                    raise Exception(f'Unknown symbol: {symbol}')
                binary_string = bin(address)[2:].zfill(16)
            elif instruction_type == InstructionType.C_INSTRUCTION:
                # dest=comp;jump
                dest = self.parser.dest()
                comp = self.parser.comp()
                jump = self.parser.jump()
                binary_string = self.code_generator.generate(dest, comp, jump)
            
            # # add this line just for debugging
            # binary_string += "  " + instruction
            self.output_binary_code.append(binary_string)
                
        with open(self.output_file, 'w') as f:
            for binary_string in self.output_binary_code:
                f.write(binary_string + '\n')
                

if __name__ == '__main__':
    # python -m my_assembler_python.assembler  ./max/Max.asm
    import sys
    # print(sys.argv)
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        raise Exception('Please provide a assembly file name.')
    assembler = Assembler(file_name)
    assembler.assemble()