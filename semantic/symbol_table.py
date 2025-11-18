# semantic/symbol_table.py
class SymbolTable:
    def __init__(self):
        self.data = {}

    def define(self, name, value_type):
        self.data[name] = value_type

    def get(self, name):
        return self.data.get(name)
