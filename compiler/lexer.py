from .symbol_table import SymbolTable


class Lexer:

    END_OF_FILE = ''
    NEW_LINE = '\n'

    def __init__(self, file_name):
        self.END_OF_FILE = -1
        self.lookAhead = 0
        self.currentLine = 1
        self.currentColumn = 1
        self.file = None
        self.symbolTable = None
        self.file_name = file_name

        try:
            self.file = open(self.file_name, 'r')
        except Exception as ex:
            raise Exception("File not found")

    def seek_to_previous_position(self):
        self.file.seek(self.file.tell() - 1)
        self.currentColumn -= 1

    def analyse(self):
        # lexeme = None
        # current_state = 0
        # current_char = '\u0000'
        #
        # while True:
        #     pass
        table = SymbolTable()
        print(table["algoritmo"])

    def __del__(self):
        self.file.close()
