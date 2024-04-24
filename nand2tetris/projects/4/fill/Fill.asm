// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

// pseudo code
// while(true) {
//     if((*R0) >= 8192) {// 
//        (*R0) = 0;
//     }
//     if((*KBD) != 0) {// 
//        *(SCREEN + (*R0)) = -1;
//     } else {
//         *(SCREEN + (*R0)) = 0;
//     }
//     (*R0) = (*R0) + 1;
// }


// use R0 to index the array of 16-bit words
(LOOP_FOREVER)
    // if((*R0) >= 8192)
    @R0
    D=M
    @8192
    D=D-A
    @SCREEN_INDEX
    D;JLT
    // (*R0) = 0
    @R0
    M=0

    (SCREEN_INDEX)
        @KBD
        D=M
        @NO_KEYBOAD_PRESSED
        D;JEQ
        // if((*KBD) != 0)
        //  *(SCREEN + (*R0)) = -1;
        @R0
        D=M
        @SCREEN
        A=D+A
        M=-1
        @INCREASE_R0
        0;JMP

        // else
        //  *(SCREEN + (*R0)) = 0;
        (NO_KEYBOAD_PRESSED)
            @R0
            D=M
            @SCREEN
            A=D+A
            M=0

    (INCREASE_R0)
        // (*R0) = (*R0) + 1;
        @R0
        M=M+1

    @LOOP_FOREVER
    0;JMP

