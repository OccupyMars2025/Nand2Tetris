from .utils import *
import os 

class Parser:
    def __init__(self, file_name: str):
        with open(file_name, 'r') as f:
            self.lines = f.read().split('\n')
        self._currentCommandIndex = 0
        self._currentCommand = None
        self.file_name_without_extension = os.path.splitext(os.path.basename(file_name))[0]
        self.function_name = ""
            
    
    def hasMoreLines(self):
        return self._currentCommandIndex < len(self.lines)
    
    
    def advance(self):
        self._currentCommand = self.lines[self._currentCommandIndex]
        self._currentCommandIndex += 1
        if '//' in self._currentCommand:
            self._currentCommand = self._currentCommand[:self._currentCommand.index('//')]
        self._currentCommand = self._currentCommand.strip()
        return self._currentCommand
    
    
    def commandType(self):
        if self._currentCommand in {'add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'}:
            return CommandType.C_ARITHMETIC
        elif self._currentCommand.startswith('push'):
            return CommandType.C_PUSH
        elif self._currentCommand.startswith('pop'):
            return CommandType.C_POP
        elif self._currentCommand.startswith('label'):
            return CommandType.C_LABEL
        elif self._currentCommand.startswith('goto'):
            return CommandType.C_GOTO
        elif self._currentCommand.startswith('if-goto'):
            return CommandType.C_IF
        elif self._currentCommand.startswith('function'):
            return CommandType.C_FUNCTION
        elif self._currentCommand == 'return':
            return CommandType.C_RETURN
        elif self._currentCommand.startswith('call'):
            return CommandType.C_CALL
        else:
            raise Exception('Unknown command type')
 

    def arg1(self) -> str:
        if self.commandType() == CommandType.C_ARITHMETIC:
            return self._currentCommand
        elif self.commandType() in {CommandType.C_PUSH, CommandType.C_POP}:
            return self._currentCommand.split(' ')[1].strip()
        elif self.commandType() == CommandType.C_RETURN:
            raise Exception('Return command does not have an argument')
        elif self.commandType() in {CommandType.C_LABEL, CommandType.C_GOTO, CommandType.C_IF}:
            label_string = self._currentCommand.split(' ')[1].strip()
            return f'{self.file_name_without_extension}.{self.function_name}${label_string}'
        elif self.commandType() == CommandType.C_FUNCTION:
            self.function_name = self._currentCommand.split(' ')[1].strip()
            return f'{self.file_name_without_extension}.{self.function_name}'
        else:
            raise Exception('Unknown command type')
    
    
    def arg2(self) -> int:
        if self.commandType() in {CommandType.C_PUSH, CommandType.C_POP}:
            return int(self._currentCommand.split(' ')[2])
        elif self.commandType() == CommandType.C_FUNCTION:
            return int(self._currentCommand.split(' ')[2])
        elif self.commandType() == CommandType.C_CALL:
            raise Exception('Not implemented yet')
        else:
            raise Exception('There is no second argument for this command')
    
    
    