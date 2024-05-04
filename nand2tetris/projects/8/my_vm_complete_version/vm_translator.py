from .parser import Parser
from .code_writer import CodeWriter
from .utils import *


class VMTranslator:
    def __init__(self, vm_file: str, assembly_file: str):
        self.parser = Parser(vm_file)
        self.code_writer = CodeWriter(assembly_file)
        
        
    def translate(self):
        while self.parser.hasMoreLines():
            current_command = self.parser.advance() 
            if ('' == current_command) or (current_command is None):
                continue
            current_command_type = self.parser.commandType()
            if current_command_type == CommandType.C_ARITHMETIC:
                self.code_writer.writeArithmetic(current_command)
            elif current_command_type in {CommandType.C_PUSH, CommandType.C_POP}:
                segment = self.parser.arg1()
                index = self.parser.arg2()
                self.code_writer.writePushPop(current_command_type, segment, index)
            elif current_command_type == CommandType.C_LABEL:
                label = self.parser.arg1()
                self.code_writer.writeLabel(label)
            elif current_command_type == CommandType.C_GOTO:
                label = self.parser.arg1()
                self.code_writer.writeGoto(label)
            elif current_command_type == CommandType.C_IF:
                label = self.parser.arg1()
                self.code_writer.writeIf(label)
            elif current_command_type == CommandType.C_FUNCTION:
                function_name = self.parser.arg1()
                num_locals = self.parser.arg2()
                self.code_writer.writeFunction(function_name, num_locals)
            elif current_command_type == CommandType.C_RETURN:
                self.code_writer.writeReturn()
            else:
                raise Exception(f'Not implemeted yet: {current_command}')
        self.code_writer.close()
        

if __name__ == '__main__':
    # python -m my_vm_complete_version.vm_translator  ./ProgramFlow/BasicLoop/BasicLoop.vm
    # python -m my_vm_complete_version.vm_translator  ./ProgramFlow/FibonacciSeries/FibonacciSeries.vm
    import sys
    import os
    if len(sys.argv) != 2:
        print('Please provide a VM file.')
        exit()
    vm_file = sys.argv[1]
    assembly_file = os.path.splitext(vm_file)[0] + '.asm'
    VMTranslator(vm_file, assembly_file).translate()