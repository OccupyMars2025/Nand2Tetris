import os 

from .parser import Parser
from .code_writer import CodeWriter
from .utils import *


class VMTranslator:
    def __init__(self, vm_source: str, assembly_file: str):
        self.code_writer = CodeWriter(assembly_file)
        self.vm_source = vm_source
        
    
    def translate(self):
        if os.path.isfile(self.vm_source):
            assert os.path.splitext(self.vm_source)[1] == '.vm'
            self._translateSingleVMFile(self.vm_source)
            self.code_writer.close()
        elif os.path.isdir(self.vm_source):
            for file in os.listdir(self.vm_source):
                if not file.endswith('.vm'): continue
                file = self.vm_source + '/' + file
                print(file)
                self._translateSingleVMFile(file)
            self.code_writer.close()
        else:
            raise Exception(f'Invalid VM file or directory: {self.vm_source}')
        
        
    def _translateSingleVMFile(self, single_vm_file: str):
        self.parser = Parser(single_vm_file)
        self.code_writer.setFileName(single_vm_file)
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
            elif current_command_type == CommandType.C_CALL:
                function_name = self.parser.arg1()
                num_args = self.parser.arg2()
                self.code_writer.writeCall(function_name, num_args)
            else:
                raise Exception(f'Not implemeted yet: {current_command}')
        

if __name__ == '__main__':
    # python -m my_vm_complete_version.vm_translator  ./ProgramFlow/BasicLoop/BasicLoop.vm
    # python -m my_vm_complete_version.vm_translator  ./ProgramFlow/FibonacciSeries/FibonacciSeries.vm
    # python -m my_vm_complete_version.vm_translator  ./FunctionCalls/SimpleFunction/SimpleFunction.vm
    import sys
    import os
    if len(sys.argv) != 2:
        print('Please provide a VM file.')
        exit()
    vm_source = sys.argv[1]
    if os.path.isfile(vm_source):
        assembly_file = os.path.splitext(vm_source)[0] + ".asm"
    elif os.path.isdir(vm_source):
        assembly_file = vm_source + '/' + os.path.basename(vm_source) + ".asm"
    VMTranslator(vm_source, assembly_file).translate()