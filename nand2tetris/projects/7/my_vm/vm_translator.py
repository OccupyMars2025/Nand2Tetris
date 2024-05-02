from .parser import Parser
from .code_writer import CodeWriter
from .utils import *


class VMTranslator:
    def __init__(self, vm_file, assembly_file):
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
            elif current_command_type == CommandType.C_PUSH or current_command_type == CommandType.C_POP:
                segment = self.parser.arg1()
                index = self.parser.arg2()
                self.code_writer.writePushPop(current_command_type, segment, index)
            else:
                raise Exception(f'Not implemeted yet: {current_command}')
        self.code_writer.close()
        

if __name__ == '__main__':
    # python -m my_vm.vm_translator  ./StackArithmetic/SimpleAdd/SimpleAdd.vm
    # python -m my_vm.vm_translator  ./StackArithmetic/StackTest/StackTest.vm
    import sys
    if len(sys.argv) != 2:
        print('Please provide a VM file.')
        exit()
    vm_file = sys.argv[1]
    assembly_file = vm_file[:-2] + 'asm'
    VMTranslator(vm_file, assembly_file).translate()