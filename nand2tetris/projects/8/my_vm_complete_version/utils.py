from enum import Enum

class CommandType(Enum):
    C_ARITHMETIC = 1
    C_PUSH = 2
    C_POP = 3
    C_LABEL = 4
    C_GOTO = 5
    C_IF = 6
    C_FUNCTION = 7
    C_RETURN = 8
    C_CALL = 9


SIMPLE_ARITHMETIC_LOGICAL_ASSEMBLY_COMMANDS = {
    'add': 'M=M+D',
    'sub': 'M=M-D',
    'neg': 'M=-M',
    'and': 'M=M&D',
    'or': 'M=M|D',
    'not': 'M=!M',
}


BINARY_OPEARATORS = {
    'add',
    'sub',
    'and',
    'or',
    'eq',
    'lt',
    'gt',
}

UNARY_OPEARATORS = {
    'neg',
    'not',
}