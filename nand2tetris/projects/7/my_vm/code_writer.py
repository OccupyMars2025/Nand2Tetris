from .utils import *

class CodeWriter:
    def __init__(self, output_file: str):
        self.output_file = output_file
        self.output = []


    def writeArithmetic(self, command: str):
        # add the original VM command as a comment
        self.output.append('// ' + command + '\n')
        
        if command in BINARY_OPEARATORS:
            # get the 2nd operand from the top of the stack and store it in D register
            self.output.append('@SP\n')
            self.output.append('M=M-1\n')
            self.output.append('A=M\n')
            self.output.append('D=M\n')
            # get the 1st operand from the top of the stack and you can refer to it using the M register
            # Caution: I actually don't decrease the stack pointer here when getting the 1st operand
            self.output.append('@SP\n')
            self.output.append('A=M-1\n')
        elif command in UNARY_OPEARATORS:
            # get the 1st operand from the top of the stack and you can refer to it using the M register
            self.output.append('@SP\n')
            self.output.append('A=M-1\n')
        else:
            raise Exception(f'Unsupported yet: {command}')
        
        # compute the result, store it in the M register
        if command in SIMPLE_ARITHMETIC_LOGICAL_ASSEMBLY_COMMANDS:
            self.output.append(SIMPLE_ARITHMETIC_LOGICAL_ASSEMBLY_COMMANDS[command] + '\n')
        elif command == 'eq':
            # if M == D:
            #     M = -1  (-1 means true)
            # else:
            #     M = 0
            self.output.append('D=M-D\n')
            self.output.append('M=-1\n')
            current_id_of_eq_command = len(self.output)
            self.output.append(f'@END_EQUAL_ID_{current_id_of_eq_command}\n')
            self.output.append('D;JEQ\n')
            ## ======== Caution: you need to assign SP-1 to A register "again" in case the A register has been modified by the previous command, 
            # if the A register has been modified by the previous command, then the M register contains some unkown value, so we need to assign SP-1 to A register again
            self.output.append('@SP\n')
            self.output.append('A=M-1\n')
            ## =========
            self.output.append('M=0\n')
            self.output.append(f'(END_EQUAL_ID_{current_id_of_eq_command})\n')
        elif command == 'gt':
            # if M > D:
            #     M = -1  (-1 means true)
            # else:
            #     M = 0
            self.output.append('D=M-D\n')
            self.output.append('M=-1\n')
            current_id_of_gt_command = len(self.output)
            self.output.append(f'@END_GT_ID_{current_id_of_gt_command}\n')
            self.output.append('D;JGT\n')
            ## ======== Caution: you need to assign SP-1 to A register "again" in case the A register has been modified by the previous command, 
            # if the A register has been modified by the previous command, then the M register contains some unkown value, so we need to assign SP-1 to A register again
            self.output.append('@SP\n')
            self.output.append('A=M-1\n')
            ## =========
            self.output.append('M=0\n')
            self.output.append(f'(END_GT_ID_{current_id_of_gt_command})\n')
        elif command == 'lt':
            # if M < D:
            #     M = -1  (-1 means true)
            # else:
            #     M = 0
            self.output.append('D=M-D\n')
            self.output.append('M=-1\n')
            current_id_of_lt_command = len(self.output)
            self.output.append(f'@END_LT_ID_{current_id_of_lt_command}\n')
            self.output.append('D;JLT\n')
            ## ======== Caution: you need to assign SP-1 to A register "again" in case the A register has been modified by the previous command, 
            # if the A register has been modified by the previous command, then the M register contains some unkown value, so we need to assign SP-1 to A register again
            self.output.append('@SP\n')
            self.output.append('A=M-1\n')
            ## =========            
            self.output.append('M=0\n')
            self.output.append(f'(END_LT_ID_{current_id_of_lt_command})\n')
        else:
            raise Exception(f'Unsupported yet: {command}')
        

    def writePushPop(self, command: CommandType, segment: str, index: int):
        # add the original VM command as a comment
        if command == CommandType.C_PUSH:
            self.output.append('// ' + f'push {segment} {index}\n')
        elif command == CommandType.C_POP:
            self.output.append('// ' + f'pop {segment} {index}\n')
        else:
            raise Exception(f'Unsupported yet: {command} {segment} {index}')
        
        if (command == CommandType.C_PUSH) and (segment == 'constant'):
            # push constant value to stack
            self.output.append('@' + str(index) + '\n')
            self.output.append('D=A\n')
            self.output.append('@SP\n')
            self.output.append('A=M\n')
            self.output.append('M=D\n')
            self.output.append('@SP\n')
            self.output.append('M=M+1\n')
        else:
            raise Exception(f'Unsupported yet: {command} {segment} {index}')


    def close(self):
        self.output.append('// add an infinite loop to keep the program running\n')
        self.output.append('(END)\n')
        self.output.append('@END\n')
        self.output.append('0;JMP\n')
        with open(self.output_file, 'w') as f:
            f.writelines(self.output)

