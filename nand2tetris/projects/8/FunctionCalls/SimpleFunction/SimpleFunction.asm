// function SimpleFunction.test 2
(SimpleFunction.test)
@2
D=A
@R13
M=D
(SimpleFunction.test$LOOP_TO_INITIALIZE_LOCAL_VARIABLES_WITH_ID_6)
@R13
D=M
@SimpleFunction.test$LOOP_TO_INITIALIZE_LOCAL_VARIABLES_WITH_ID_6_END
D;JLE
@SP
A=M
M=0
@SP
M=M+1
@R13
M=M-1
@SimpleFunction.test$LOOP_TO_INITIALIZE_LOCAL_VARIABLES_WITH_ID_6
0;JMP
(SimpleFunction.test$LOOP_TO_INITIALIZE_LOCAL_VARIABLES_WITH_ID_6_END)
// push local 0
@0
D=A
@LCL
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
// push local 1
@1
D=A
@LCL
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M+D
// not
@SP
A=M-1
M=!M
// push argument 0
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M+D
// push argument 1
@1
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M-D
// return
@LCL
D=M
@R13
M=D
@5
D=A
@R13
A=M-D
D=M
@R14
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
A=M-1
D=M
@THAT
M=D
@2
D=A
@R13
A=M-D
D=M
@THIS
M=D
@3
D=A
@R13
A=M-D
D=M
@ARG
M=D
@4
D=A
@R13
A=M-D
D=M
@LCL
M=D
@R14
A=M
0;JMP
// end of return
// add an infinite loop to keep the program running
(END)
@END
0;JMP