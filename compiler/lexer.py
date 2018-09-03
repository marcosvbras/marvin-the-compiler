class Lexer:

    def __init__(self):
        self.END_OF_FILE = -1
        self.lookAhead = 0
        self.currentLine = 1
        self.currentColumn = 1
        self.file = None
        self.symbolTable = None
