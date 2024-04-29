
class CodeGenerator:
    def dest(self, dest: str) -> str:
        if dest == '' or dest is None:
            return '000'
        elif dest == 'M':
            return '001'
        elif dest == 'D':
            return '010'
        elif dest in {'DM', 'MD'}:
            return '011'
        elif dest == 'A':
            return '100'
        elif dest in {'AM', 'MA'}:
            return '101'
        elif dest in {'AD', 'DA'}:
            return '110'
        # dest == 'ADM':
        elif isinstance(dest, str) and len(dest) == 3 and ('A' in dest) and ('D' in dest) and ('M' in dest):
            return '111'
        else:
            raise Exception(f'Invalid dest {dest}')
        
    def comp(self, comp: str) -> str:
        if comp == '0':
            return '0101010'
        elif comp == '1':
            return '0111111'
        elif comp == '-1':
            return '0111010'
        elif comp == 'D':
            return '0001100'
        elif comp == 'A':
            return '0110000'
        elif comp == 'M':
            return '1110000'
        elif comp == '!D':
            return '0001101'
        elif comp == '!A':
            return '0110001'
        elif comp == '!M':
            return '1110001'
        elif comp == '-D':
            return '0001111'
        elif comp == '-A':
            return '0110011'
        elif comp == '-M':
            return '1110011'
        elif comp == 'D+1':
            return '0011111'
        elif comp == 'A+1':
            return '0110111'
        elif comp == 'M+1':
            return '1110111'
        elif comp == 'D-1':
            return '0001110'
        elif comp == 'A-1':
            return '0110010'
        elif comp == 'M-1':
            return '1110010'
        elif comp == 'D+A':
            return '0000010'
        elif comp == 'D+M':
            return '1000010'
        elif comp == 'D-A':
            return '0010011'
        elif comp == 'D-M':
            return '1010011'
        elif comp == 'A-D':
            return '0000111'
        elif comp == 'M-D':
            return '1000111'
        elif comp == 'D&A':
            return '0000000'
        elif comp == 'D&M':
            return '1000000'
        elif comp == 'D|A':
            return '0010101'
        elif comp == 'D|M':
            return '1010101'
        else:
            raise Exception(f'Invalid comp {comp}')
        
    def jump(self, jump: str) -> str:
        if jump == '' or jump is None:
            return '000'
        elif jump == 'JGT':
            return '001'
        elif jump == 'JEQ':
            return '010'
        elif jump == 'JGE':
            return '011'
        elif jump == 'JLT':
            return '100'
        elif jump == 'JNE':
            return '101'
        elif jump == 'JLE':
            return '110'
        elif jump == 'JMP':
            return '111'
        else:
            raise Exception(f'Invalid jump {jump}')

    def generate(self, dest: str, comp: str, jump: str) -> str:
        return '111' + self.comp(comp) + self.dest(dest) + self.jump(jump)
