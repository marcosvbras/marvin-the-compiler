class LexicalError:

    def __init__(self, symbol, line, column):
        self.symbol = symbol
        self.line = line
        self.column = column

    def __str__(self):
        return "\n>>>>>>>>>>>>>>>>>>>>>>>>>> Lexical Error >>>>>>>>>>>>>>>>>>>>>>>>>>>>\n\"" \
               + self.symbol + "\" at " + str(self.line) + ":" \
               + str(self.column) \
               + " is not a valid symbol.\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n"


class CustomLexicalError:

    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column

    def __str__(self):
        return "\n>>>>>>>>>>>>>>>>>>>>>>>>>> Lexical Error >>>>>>>>>>>>>>>>>>>>>>>>>>>>\n" \
               + self.message + " at " + str(self.line) + ":" \
               + str(self.column) \
               + "\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n"