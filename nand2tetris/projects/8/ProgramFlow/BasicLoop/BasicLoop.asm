// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 0
@SP
M=M-1
A=M
D=M
@R13
M=D
@0
D=A
@LCL
A=D+M
D=A
@R14
M=D
@R13
D=M
@R14
A=M
M=D
// label LOOP
(BasicLoop.$LOOP)
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
// add
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M+D
// pop local 0
@SP
M=M-1
A=M
D=M
@R13
M=D
@0
D=A
@LCL
A=D+M
D=A
@R14
M=D
@R13
D=M
@R14
A=M
M=D
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
// push constant 1
@1
D=A
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
// pop argument 0
@SP
M=M-1
A=M
D=M
@R13
M=D
@0
D=A
@ARG
A=D+M
D=A
@R14
M=D
@R13
D=M
@R14
A=M
M=D
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
// if-goto LOOP
@SP
M=M-1
A=M
D=M
@BasicLoop.$LOOP
D;JNE
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
// add an infinite loop to keep the program running
(END)
@END
0;JMP
