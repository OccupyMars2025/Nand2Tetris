from .utils import *

class CodeWriter:
    def __init__(self, output_file: str):
        self.output_file = open(output_file, 'w')


    def writeArithmetic(self, command: str):
        # add the original VM command as a comment
        self.output_file.write('// ' + command + '\n')
        # store the 2nd operand in D register
        self.output_file.write('@SP\n')
        self.output_file.write('M=M-1\n')
        self.output_file.write('A=M\n')
        self.output_file.write('D=M\n')
        # get the 1st operand in M register
        self.output_file.write('@SP\n')
        self.output_file.write('A=M-1\n')
        # compute the result
        self.output_file.write(arithmetic_logical_assembly_commands[command] + '\n')
        
        
    def writePushPop(self, command: CommandType, segment: str, index: int):
        # add the original VM command as a comment
        if command == CommandType.C_PUSH:
            self.output_file.write('// ' + f'push {segment} {index}\n')
        elif command == CommandType.C_POP:
            self.output_file.write('// ' + f'pop {segment} {index}\n')
        else:
            raise Exception(f'Unsupported yet: {command} {segment} {index}')
        
        if (command == CommandType.C_PUSH) and (segment == 'constant'):
            # push constant value to stack
            self.output_file.write('@' + str(index) + '\n')
            self.output_file.write('D=A\n')
            self.output_file.write('@SP\n')
            self.output_file.write('A=M\n')
            self.output_file.write('M=D\n')
            self.output_file.write('@SP\n')
            self.output_file.write('M=M+1\n')
        else:
            raise Exception(f'Unsupported yet: {command} {segment} {index}')


    def close(self):
        self.output_file.write('// add an infinite loop to keep the program running\n')
        self.output_file.write('(END)\n')
        self.output_file.write('@END\n')
        self.output_file.write('0;JMP\n')
        self.output_file.close()

