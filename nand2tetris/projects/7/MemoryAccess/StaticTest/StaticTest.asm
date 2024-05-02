// push constant 111
@111
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 333
@333
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 888
@888
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop static 8
@SP
M=M-1
A=M
D=M
@R13
M=D
@StaticTest.static.8
D=A
@R14
M=D
@R13
D=M
@R14
A=M
M=D
// pop static 3
@SP
M=M-1
A=M
D=M
@R13
M=D
@StaticTest.static.3
D=A
@R14
M=D
@R13
D=M
@R14
A=M
M=D
// pop static 1
@SP
M=M-1
A=M
D=M
@R13
M=D
@StaticTest.static.1
D=A
@R14
M=D
@R13
D=M
@R14
A=M
M=D
// push static 3
@StaticTest.static.3
D=M
@SP
A=M
M=D
@SP
M=M+1
// push static 1
@StaticTest.static.1
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
// push static 8
@StaticTest.static.8
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
// add an infinite loop to keep the program running
(END)
@END
0;JMP
