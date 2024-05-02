from .utils import *
import os

class CodeWriter:
    def __init__(self, output_file: str):
        self.output_file = output_file
        # self._filename_without_extension is used in the method _accessStaticSegment()
        self._filename_without_extension = os.path.splitext(os.path.basename(output_file))[0]
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
        
              
    def _accessLCL_ARG_THIS_THAT_Segment(self, segment: str, index: int):
        """
        reference: Memory Segments Mapping, page 191 in the book,
        the value you want is in the M register
        """
        self.output.append(f'@{index}\n')
        self.output.append('D=A\n')
        if segment == 'local':
            self.output.append('@LCL\n')
        elif segment == 'argument':
            self.output.append('@ARG\n')
        elif segment == 'this':
            self.output.append('@THIS\n')
        elif segment == 'that':
            self.output.append('@THAT\n')
        else:
            raise Exception('Unsupported yet')
        self.output.append(f'A=D+M\n')
    
    
    def _accessPointerSegment(self, index: int):
        """
        reference: Memory Segments Mapping, page 191 in the book,
        the value you want is in the M register
        """
        if index == 0:
            self.output.append('@THIS\n')
        elif index == 1:
            self.output.append('@THAT\n')
        else:
            raise Exception('Unsupported yet')
        
        
    def _accessTempSegment(self, index: int):
        """
        reference: Memory Segments Mapping, page 192 in the book,
        the value you want is in the M register
        """
        if index < 0 or index > 7:
            raise Exception('index out of range')
        # calcuate 5+index
        self.output.append('@5\n')
        self.output.append('D=A\n')
        self.output.append(f'@{index}\n')
        self.output.append('A=D+A\n')
        
    def _accessConstantSegment(self, index: int):
        """
        reference: Memory Segments Mapping, page 192 in the book,
        Caution: store the value in the D register
        """
        if index < 0 or index > 2**15-1:
            raise Exception('index out of range')
        self.output.append(f'@{index}\n')
        self.output.append('D=A\n')
        
        
    def _accessStaticSegment(self, index: int):
        """
        reference: Memory Segments Mapping, page 192 in the book,
        I just rely on the assembler to decide where to store the static variable,
        the value you want is in the M register
        """
        self.output.append(f'@{self._filename_without_extension}.static.{index}\n')
            
    
    def _accessMemoerySegment(self, segment: str, index: int):
        """
        reference: Memory Segments Mapping, page 192 in the book,
        if segment == 'constant':
            the value you want is in the D register
        else:
            the value you want is in the M register
        """
        if segment in {'local', 'argument', 'this', 'that'}:
            self._accessLCL_ARG_THIS_THAT_Segment(segment, index)
        elif segment == 'pointer':
            self._accessPointerSegment(index)
        elif segment == 'temp':
            self._accessTempSegment(index)
        elif segment == 'constant':
            self._accessConstantSegment(index)
        elif segment == 'static':
            self._accessStaticSegment(index)
        
        
    def _pushOntoStack(self):
        """
        push D onto stack
        """
        self.output.append('@SP\n')
        self.output.append('A=M\n')
        self.output.append('M=D\n')
        self.output.append('@SP\n')
        self.output.append('M=M+1\n')
        
    
    def _popFromStack(self):
        """
        pop the top value from stack, 
        the value you want is in the D register
        """
        self.output.append('@SP\n')
        self.output.append('M=M-1\n')
        self.output.append('A=M\n')
        self.output.append('D=M\n')
        
     
    def writePushPop(self, command: CommandType, segment: str, index: int):
        """
        reference: Memory Segments Mapping, page 191 in the book
        """
        if command == CommandType.C_PUSH:
            self.output.append('// ' + f'push {segment} {index}\n')
            # push:
            # 1. access the segment, get M
            # 2. D = M
            # 3. push D onto stack
            self._accessMemoerySegment(segment, index)
            if segment != 'constant':
                self.output.append('D=M\n')
            self._pushOntoStack()
        elif command == CommandType.C_POP:
            self.output.append('// ' + f'pop {segment} {index}\n')
            # ======================================================
            # Caution: If I want to use a generalized implemnetation for all kinds of segments,
            # I need to use the memory locations R13-R15 for temporary storage which are not used by any memory segment,
            # because I run out of registers. (The hardware only provides D, A, M)
            # Maybe this implementation can be simplified further.
            # ======================================================
            # pop:
            #  pop the top value from stack, now the value you want is in D
            #  @R13
            #  M = D 
            # (now we have stored the poped value in R13)
            #  access the segment(get M)
            #  D = A
            #  @R14
            #  M = D
            # (now we have stored the destination address in R14)
            #  @R13
            #  D = M
            #  @R14
            #  A = M
            #  M = D
            if segment == 'constant':
                raise Exception(f'Unsupported yet: {command} {segment} {index}')
            self._popFromStack()
            self.output.append('@R13\n')
            self.output.append('M=D\n')
            
            self._accessMemoerySegment(segment, index)
            
            self.output.append('D=A\n')
            self.output.append('@R14\n')
            self.output.append('M=D\n')
            self.output.append('@R13\n')
            self.output.append('D=M\n')
            self.output.append('@R14\n')
            self.output.append('A=M\n')
            self.output.append('M=D\n')
        else:
            raise Exception(f'Unsupported yet: {command} {segment} {index}')
           
            
            
    def close(self):
        self.output.append('// add an infinite loop to keep the program running\n')
        self.output.append('(END)\n')
        self.output.append('@END\n')
        self.output.append('0;JMP\n')
        with open(self.output_file, 'w') as f:
            f.writelines(self.output)

