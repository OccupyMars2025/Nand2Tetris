class SymbolTable:
    def __init__(self):
        self.symbol_table = {}
        # add predefined symbols
        for i in range(16):
            self.symbol_table[f"R{i}"] = i
        self.symbol_table["SP"] = 0
        self.symbol_table["LCL"] = 1
        self.symbol_table["ARG"] = 2
        self.symbol_table["THIS"] = 3
        self.symbol_table["THAT"] = 4
        self.symbol_table["SCREEN"] = 16384  # 0x4000
        self.symbol_table["KBD"] = 24576 # 0x6000
        
        
    def addEntry(self, symbol: str, address: int):
        self.symbol_table[symbol] = address

        
    def contains(self, symbol: str) -> bool:
        return symbol in self.symbol_table
         
            
    def getAddress(self, symbol: str) -> int:
        return self.symbol_table[symbol]
