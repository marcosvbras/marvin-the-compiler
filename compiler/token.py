class Token:

    def __init__(self, tag, lexeme, line=0, column=0):
        self.tag = tag
        self.lexeme = lexeme
        self.line = line
        self.column = column

    def __str__(self):
        return "<{}, \"{}\"> Line: {} - Column: {}".format(self.tag, self.lexeme, self.line, self.column)
