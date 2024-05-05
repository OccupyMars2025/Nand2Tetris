from .utils import *
import os

class CodeWriter:
    def __init__(self, output_file: str):
        self.output_file = output_file
        self.output = []
        # set SP=261
        self.output.append('// set SP=261\n')
        self.output.append('@261\n')
        self.output.append('D=A\n')
        self.output.append('@SP\n')
        self.output.append('M=D\n')
        # call Sys.init
        self.output.append('// call Sys.init\n')
        self.output.append('@Sys.init\n')
        self.output.append('0;JMP\n')
        self._filename_dot_function_name = ''
        self._vm_source_filename_without_extension = ''


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
            self.output.append(f'@{self._filename_dot_function_name}$END_EQUAL_ID_{current_id_of_eq_command}\n')
            self.output.append('D;JEQ\n')
            ## ======== Caution: you need to assign SP-1 to A register "again" in case the A register has been modified by the previous command, 
            # if the A register has been modified by the previous command, then the M register contains some unkown value, so we need to assign SP-1 to A register again
            self.output.append('@SP\n')
            self.output.append('A=M-1\n')
            ## =========
            self.output.append('M=0\n')
            self.output.append(f'({self._filename_dot_function_name}$END_EQUAL_ID_{current_id_of_eq_command})\n')
        elif command == 'gt':
            # if M > D:
            #     M = -1  (-1 means true)
            # else:
            #     M = 0
            self.output.append('D=M-D\n')
            self.output.append('M=-1\n')
            current_id_of_gt_command = len(self.output)
            self.output.append(f'@{self._filename_dot_function_name}$END_GT_ID_{current_id_of_gt_command}\n')
            self.output.append('D;JGT\n')
            ## ======== Caution: you need to assign SP-1 to A register "again" in case the A register has been modified by the previous command, 
            # if the A register has been modified by the previous command, then the M register contains some unkown value, so we need to assign SP-1 to A register again
            self.output.append('@SP\n')
            self.output.append('A=M-1\n')
            ## =========
            self.output.append('M=0\n')
            self.output.append(f'({self._filename_dot_function_name}$END_GT_ID_{current_id_of_gt_command})\n')
        elif command == 'lt':
            # if M < D:
            #     M = -1  (-1 means true)
            # else:
            #     M = 0
            self.output.append('D=M-D\n')
            self.output.append('M=-1\n')
            current_id_of_lt_command = len(self.output)
            self.output.append(f'@{self._filename_dot_function_name}$END_LT_ID_{current_id_of_lt_command}\n')
            self.output.append('D;JLT\n')
            ## ======== Caution: you need to assign SP-1 to A register "again" in case the A register has been modified by the previous command, 
            # if the A register has been modified by the previous command, then the M register contains some unkown value, so we need to assign SP-1 to A register again
            self.output.append('@SP\n')
            self.output.append('A=M-1\n')
            ## =========            
            self.output.append('M=0\n')
            self.output.append(f'({self._filename_dot_function_name}$END_LT_ID_{current_id_of_lt_command})\n')
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
        self.output.append(f'@{self._vm_source_filename_without_extension}.{index}\n')
            
    
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
        
        
    # Caution: this method is not used !
    def setFileName(self, vm_source_filename: str):
        """
        Set the name of the vm source file without extension which you are parsing.
        Caution: this method must be called before parsing the vm source file.
        """
        vm_source_filename = os.path.basename(vm_source_filename)
        if '.' in vm_source_filename:
            self._vm_source_filename_without_extension = os.path.splitext(vm_source_filename)[0]
        else:
            self._vm_source_filename_without_extension = vm_source_filename
            
     
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
           
    
    def writeLabel(self, label: str):
        """
        (fileName.functionName$label)
        """
        self.output.append(f"// label {label}\n")
        self.output.append(f'({self._filename_dot_function_name}${label})\n')
        
    
    def writeGoto(self, label: str):
        """
        @fileName.functionName$label
        0;JMP
        """
        self.output.append(f"// goto {label}\n")
        self.output.append(f'@{self._filename_dot_function_name}${label}\n')
        self.output.append('0;JMP\n')
        
    
    def writeIf(self, label: str):
        """
        @SP
        M=M-1
        A=M
        D=M
        @fileName.functionName$label
        D;JNE
        """
        self.output.append(f"// if-goto {label}\n")
        self.output.append('@SP\n')
        self.output.append('M=M-1\n')
        self.output.append('A=M\n')
        self.output.append('D=M\n')
        self.output.append(f'@{self._filename_dot_function_name}${label}\n')
        self.output.append('D;JNE\n')
        
         
    def writeFunction(self, function_name: str, num_locals: int):
        """
        (filename.functionName)
        repeat num_locals times: (you can use R13-R15 for temporary storage)
            push constant 0
            
        function_name: the argument often has the form "filename.functionName"
        """
        self._filename_dot_function_name = function_name
        self.output.append(f'// function {function_name} {num_locals}\n')
        self.output.append(f'({self._filename_dot_function_name})\n')
        # store num_locals in R13
        self.output.append(f'@{num_locals}\n')
        self.output.append('D=A\n')
        self.output.append('@R13\n')
        self.output.append('M=D\n')
        
        # I specify the label name. Hope it will not conflict with other label names that are generated by writeLabel()
        # TODO: How to avoid the conflict?
        loop_label = f'{self._filename_dot_function_name}$LOOP_TO_INITIALIZE_LOCAL_VARIABLES_WITH_ID_{len(self.output)}'
       
        # loop_label
        self.output.append(f'({loop_label})\n')
        # check if num_locals > 0
        self.output.append('@R13\n')
        self.output.append('D=M\n')
        self.output.append(f'@{loop_label}_END\n')
        self.output.append('D;JLE\n')
        #   push constant 0
        self.output.append('@SP\n')
        self.output.append('A=M\n')
        self.output.append('M=0\n')
        self.output.append('@SP\n')
        self.output.append('M=M+1\n')
        # num_locals -= 1
        self.output.append('@R13\n')
        self.output.append('M=M-1\n')
        # go back to loop_label
        self.output.append(f'@{loop_label}\n')
        self.output.append('0;JMP\n')
        # end of loop
        self.output.append(f'({loop_label}_END)\n')
    
    
    def writeReturn(self):
        """
        frame = LCL  // frame is a temporary variable
        retAddr = *(frame-5) // puts the return address in a temporary variable
        *ARG = pop()  // repositions the return value for the caller
        SP = ARG+1   //repositions SP for the caller
        THAT = *(frame-1)   // restores THAT for the caller
        THIS = *(frame-2)   // restores THIS for the caller
        ARG = *(frame-3)    // restores ARG for the caller
        LCL = *(frame-4)    // restores LCL for the caller
        goto retAddr      // go to the return address
        """
        self.output.append('// return\n')
        
        # frame = LCL  // frame is a temporary variable, store it in R13
        self.output.append('@LCL\n')
        self.output.append('D=M\n')
        self.output.append('@R13\n')
        self.output.append('M=D\n')
        
        # retAddr = *(frame-5) // puts the return address in a temporary variable, store it in R14
        self.output.append('@5\n')
        self.output.append('D=A\n')
        self.output.append('@R13\n')
        self.output.append('A=M-D\n')
        self.output.append('D=M\n')
        self.output.append('@R14\n')
        self.output.append('M=D\n')
        
        # *ARG = pop()  // repositions the return value for the caller
        self._popFromStack()
        self.output.append('@ARG\n')
        self.output.append('A=M\n')
        self.output.append('M=D\n')
        
        # SP = ARG+1   //repositions SP for the caller
        self.output.append('@ARG\n')
        self.output.append('D=M+1\n')
        self.output.append('@SP\n')
        self.output.append('M=D\n')
        
        # THAT = *(frame-1)   // restores THAT for the caller
        self.output.append('@R13\n')
        self.output.append('A=M-1\n')
        self.output.append('D=M\n')
        self.output.append('@THAT\n')
        self.output.append('M=D\n')
        
        # THIS = *(frame-2)   // restores THIS for the caller
        self.output.append('@2\n')
        self.output.append('D=A\n')
        self.output.append('@R13\n')
        self.output.append('A=M-D\n')
        self.output.append('D=M\n')
        self.output.append('@THIS\n')
        self.output.append('M=D\n')
        
        # ARG = *(frame-3)    // restores ARG for the caller
        self.output.append('@3\n')
        self.output.append('D=A\n')
        self.output.append('@R13\n')
        self.output.append('A=M-D\n')
        self.output.append('D=M\n')
        self.output.append('@ARG\n')
        self.output.append('M=D\n')
        
        # LCL = *(frame-4)    // restores LCL for the caller
        self.output.append('@4\n')
        self.output.append('D=A\n')
        self.output.append('@R13\n')
        self.output.append('A=M-D\n')
        self.output.append('D=M\n')
        self.output.append('@LCL\n')
        self.output.append('M=D\n')
        
        # goto retAddr      // go to the return address
        self.output.append('@R14\n')
        self.output.append('A=M\n')
        self.output.append('0;JMP\n')
        self.output.append('// end of return\n')
        
     
    def writeCall(self, function_name: str, num_args: int):
        """
        push returnAddress to the stack
        push LCL to the stack
        push ARG to the stack
        push THIS to the stack
        push THAT to the stack
        ARG = SP - 5 - num_args
        LCL = SP
        goto functio_name
        (returnAddress)
        
        function_name: this argument has the form "filename.function_name"
        """
        self.output.append(f'// call {function_name} {num_args}\n')
        
        # push return address to the stack
        # Caution: here self._filename_dot_function_name is the function name of the caller
        return_address_label = f'{self._filename_dot_function_name}$ret.{len(self.output)}'
        self.output.append(f'@{return_address_label}\n')
        self.output.append('D=A\n')
        self._pushOntoStack()
        # push LCL to the stack
        self.output.append('@LCL\n')
        self.output.append('D=M\n')
        self._pushOntoStack()
        # push ARG to the stack
        self.output.append('@ARG\n')
        self.output.append('D=M\n')
        self._pushOntoStack()
        # push THIS to the stack
        self.output.append('@THIS\n')
        self.output.append('D=M\n')
        self._pushOntoStack()
        # push THAT to the stack
        self.output.append('@THAT\n')
        self.output.append('D=M\n')
        self._pushOntoStack()
        
        # ARG = SP - 5 - num_args
        self.output.append('@SP\n')
        self.output.append('D=M\n')
        self.output.append('@5\n')
        self.output.append('D=D-A\n')
        self.output.append(f'@{num_args}\n')
        self.output.append('D=D-A\n')
        self.output.append('@ARG\n')
        self.output.append('M=D\n')
        
        # LCL = SP
        self.output.append('@SP\n')
        self.output.append('D=M\n')
        self.output.append('@LCL\n')
        self.output.append('M=D\n')
        
        # goto function_name
        self.output.append(f'@{function_name}\n')
        self.output.append('0;JMP\n')
        
        # (returnAddress)
        self.output.append(f'({return_address_label})\n')
        
        
    def close(self):
        self.output.append('// add an infinite loop to keep the program running\n')
        self.output.append('(END)\n')
        self.output.append('@END\n')
        self.output.append('0;JMP\n')
        with open(self.output_file, 'w') as f:
            f.writelines(self.output)

