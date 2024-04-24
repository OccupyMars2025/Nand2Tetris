// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

// pseudo code:
// R2=0
// LOOP:
//     if(R1 == 0) goto END
//     R2 += R0
//     R1 -= 1
//     goto LOOP
// END:

// modify R1 in place, reduce R1 one by one
@R2
M=0
(LOOP)
    // if(R1 == 0) goto END
    @R1
    D=M
    @END
    D;JEQ

    // R2 += R0
    @R0
    D=M
    @R2
    M=D+M

    // R1 -= 1
    @R1
    M=M-1

    // goto LOOP
    @LOOP
    0;JMP

(END)
    @END
    0;JMP


