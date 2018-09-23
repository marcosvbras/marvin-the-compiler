from .symbol_table import SymbolTable
from .token import Token
from .tag import Tag
from .errors import LexicalError, CustomLexicalError


class Lexer:

    END_OF_FILE = ''
    NEW_LINE = '\n'
    WHITE_SPACE = ' '
    TABULATION = '\t'
    INITIAL_STATE = 1

    def __init__(self, file_name):
        self.last_read_char = None
        self.current_line = 1
        self.current_column = 1
        self.file = None
        self.file_name = file_name
        self.symbol_table = SymbolTable()
        self.was_error_raised = False
        self.file = open(self.file_name, 'r')

    def seek_to_previous_position(self):
        if self.last_read_char is not None:
            self.file.seek(self.file.tell() - 1)
            self.current_column -= 1

    def next_token(self):
        lexeme = ""
        current_state = self.INITIAL_STATE

        while True:
            self.last_read_char = self.file.read(1)

            if self.last_read_char is not self.END_OF_FILE:
                self.current_column += 1

            if current_state == 1:
                if self.last_read_char is self.END_OF_FILE:
                    return Token(Tag.END_OF_FILE, 'EOF', self.current_line, self.current_column)
                elif self.last_read_char == self.TABULATION:
                    self.current_column += 2
                elif self.last_read_char == self.WHITE_SPACE or self.last_read_char == '\r':
                    pass
                elif self.last_read_char == self.NEW_LINE:
                    self.current_line += 1
                    self.current_column = 1
                elif self.last_read_char.isalpha():  # Go to state 2
                    lexeme += self.last_read_char
                    current_state = 2
                elif self.last_read_char.isdigit():  # Go to state 26
                    lexeme += self.last_read_char
                    current_state = 26
                elif self.last_read_char == '"':  # Go to state 31
                    current_state = 31
                elif self.last_read_char == ';':  # Go to state 4
                    return Token(Tag.SYMBOL_SEMICOLON, ';', self.current_line, self.current_column)
                elif self.last_read_char == ',':  # Go to state 5
                    return Token(Tag.SYMBOL_COMMA, ',', self.current_line, self.current_column)
                elif self.last_read_char == '(':  # Go to state 6
                    return Token(Tag.SYMBOL_OPEN_PARENTHESIS, '(', self.current_line, self.current_column)
                elif self.last_read_char == ')':  # Go to state 7
                    return Token(Tag.SYMBOL_CLOSE_PARENTHESIS, ')', self.current_line, self.current_column)
                elif self.last_read_char == '<':  # Go to state 8
                    lexeme += self.last_read_char
                    current_state = 8
                elif self.last_read_char == '>':  # Go to state 14
                    lexeme += self.last_read_char
                    current_state = 14
                elif self.last_read_char == '=':  # Go to state 17
                    return Token(Tag.OPERATOR_EQUALS, '=', self.current_line, self.current_column)
                elif self.last_read_char == '+':  # Go to state 18
                    return Token(Tag.OPERATOR_PLUS, '+', self.current_line, self.current_column)
                elif self.last_read_char == '-':  # Go to state 19
                    return Token(Tag.OPERATOR_MINUS, '-', self.current_line, self.current_column)
                elif self.last_read_char == '*':  # Go to state 20
                    return Token(Tag.OPERATOR_MULTIPLICATION, '*', self.current_line, self.current_column)
                elif self.last_read_char == '/':  # Go to state 21
                    current_state = 21
                else:
                    self.raise_lexical_error(self.last_read_char, self.current_line, self.current_column)
                    self.was_error_raised = False

            elif current_state == 2:
                if self.last_read_char.isalpha() or self.last_read_char.isdigit():  # Stay at state 2
                    lexeme += self.last_read_char
                else:  # Other
                    self.seek_to_previous_position()
                    token = self.symbol_table[lexeme]

                    if token is None:
                        token = self.symbol_table.include(lexeme, Tag.ID)

                    token.line = self.current_line
                    token.column = self.current_column

                    return token

            elif current_state == 8:
                if self.last_read_char == '=':  # Go to state 9
                    lexeme += self.last_read_char
                    return Token(Tag.OPERATOR_LESS_THAN_EQUALS, lexeme, self.current_line, self.current_column)
                elif self.last_read_char == '-':  # Go to state 11
                    lexeme += self.last_read_char
                    current_state = 11
                elif self.last_read_char == '>':  # Go to state 13 - Final State - Just Return the Token
                    lexeme += self.last_read_char
                    return Token(Tag.OPERATOR_DIFFERENT, lexeme, self.current_line, self.current_column)
                else:  # Go to state 10 - Final State - Just Return the Token and and the file pointer
                    self.seek_to_previous_position()
                    return Token(Tag.OPERATOR_LESS_THAN, lexeme, self.current_line, self.current_column)

            elif current_state == 11:
                if self.last_read_char == '-':  # Go to state 12 - Final State - Just Return the Token
                    lexeme += self.last_read_char
                    self.was_error_raised = False
                    return Token(Tag.OPERATOR_ASSIGN, lexeme, self.current_line, self.current_column)
                elif not self.was_error_raised:
                    """
                        The symbol read is different of the expected for '<--'
                    """
                    self.raise_lexical_error(self.last_read_char, self.current_line, self.current_column)

            elif current_state == 14:
                if self.last_read_char == '=':  # Go to state 15
                    lexeme += self.last_read_char
                    return Token(Tag.OPERATOR_GREATER_THAN_EQUALS, lexeme, self.current_line, self.current_column)
                else:  # Go to state 16
                    self.seek_to_previous_position()
                    return Token(Tag.OPERATOR_GREATER_THAN, lexeme, self.current_line, self.current_column)

            elif current_state == 21:
                if self.last_read_char == '*':  # Go to state 22
                    current_state = 22
                elif self.last_read_char == '/':  # Go to state 25
                    current_state = 25
                else:  # Go to state 24 - Final State - Return the token and the file pointer
                    self.seek_to_previous_position()
                    return Token(Tag.OPERATOR_DIVISION, "/", self.current_line, self.current_column)

            elif current_state == 22:
                if self.last_read_char == self.NEW_LINE:
                    self.current_line += 1
                    self.current_column = 1
                elif self.last_read_char == '*':  # Go to state 23
                    current_state = 23
                elif self.last_read_char == self.END_OF_FILE:
                    """
                        Multi-line comments must be closed before end of file.
                    """
                    self.raise_error("Comment not closed", self.current_line, self.current_column)

            elif current_state == 23:
                if self.last_read_char == '/':  # Return to initial state
                    current_state = 1
                elif self.last_read_char == '*':  # Stay at state 23
                    pass
                elif self.last_read_char == self.NEW_LINE:
                    self.current_line += 1
                    self.current_column = 1
                elif self.last_read_char == self.END_OF_FILE:
                    """
                        Multi-line comments must be closed before end of file.
                    """
                    self.raise_error("Comment not closed", self.current_line, self.current_column)
                else:  # Return to state 22
                    current_state = 22

            elif current_state == 25:
                if self.last_read_char == self.NEW_LINE:  # Return to initial state
                    current_state = 1
                    self.current_column = 1
                    self.current_line += 1

            elif current_state == 26:
                if self.last_read_char.isdigit():  # Keep in state 26
                    lexeme += self.last_read_char
                elif self.last_read_char == '.':  # Go to state 28
                    lexeme += self.last_read_char
                    current_state = 28
                else:  # Go to state 27 - Final State - Return the token and the file pointer
                    self.seek_to_previous_position()
                    return Token(Tag.VALUE_NUMERICO, lexeme, self.current_line, self.current_column)

            elif current_state == 28:
                if self.last_read_char.isdigit():  # Go to state 29
                    self.was_error_raised = False
                    lexeme += self.last_read_char
                    current_state = 29
                elif not self.was_error_raised:
                    """
                        The symbol read is different of the expected for a decimal number
                    """
                    self.raise_lexical_error(self.last_read_char, self.current_line, self.current_column)
                    self.was_error_raised = True

            elif current_state == 29:
                if self.last_read_char.isdigit():  # Keep in state 29
                    lexeme += self.last_read_char
                else:  # Go to state 30 - Final State - Return the token and the file pointer
                    self.seek_to_previous_position()
                    self.was_error_raised = False
                    return Token(Tag.VALUE_NUMERICO, lexeme, self.current_line, self.current_column)

            elif current_state == 31:
                self.was_error_raised = False

                if self.last_read_char == self.END_OF_FILE and not self.was_error_raised:
                    self.raise_lexical_error("Literal values must be closed with double quote before end of file", self.current_line, self.current_column)
                elif self.last_read_char == self.NEW_LINE:
                    if not self.was_error_raised:
                        self.raise_error("Literal values must be closed with double quote before a new line starts", self.current_line,
                                         self.current_column)
                    self.current_line += 1
                    self.current_column = 1
                elif self.last_read_char == '"' and not self.was_error_raised:
                    self.raise_error("Empty literal values are not allowed", self.current_line, self.current_column)
                elif self.is_ascii(self.last_read_char):
                    lexeme += self.last_read_char
                    current_state = 32
                elif not self.was_error_raised:
                    self.raise_lexical_error(self.last_read_char, self.current_line, self.current_column)

            elif current_state == 32:
                if self.last_read_char == '"':  # Go to state 33 - Final State - Return the token
                    self.was_error_raised = False
                    return Token(Tag.VALUE_LITERAL, lexeme, self.current_line, self.current_column)
                elif self.last_read_char == self.END_OF_FILE and not self.was_error_raised:
                    self.raise_error("Literal values must be closed with double quote before end of file", self.current_line, self.current_column)
                elif self.last_read_char == self.NEW_LINE:
                    if not self.was_error_raised:
                        self.raise_error("Literal values must be closed with double quote before a new line starts", self.current_line,
                                         self.current_column)

                    self.current_line += 1
                    self.current_column = 1
                elif self.is_ascii(self.last_read_char):
                    lexeme += self.last_read_char
                elif not self.was_error_raised:
                    self.raise_lexical_error(self.last_read_char, self.current_line, self.current_column)

    def is_ascii(self, string):
        try:
            string.encode('ascii')
        except UnicodeEncodeError:
            return False
        else:
            return True

    def print_symbol_table(self):
        for item in self.symbol_table.table.values():
            print(item)

    def raise_lexical_error(self, symbol, line, column):
        print(LexicalError(symbol, line, column))
        self.was_error_raised = True

    def raise_error(self, message, line, column):
        print(CustomLexicalError(message, line, column))
        self.was_error_raised = True

    def __del__(self):
        self.file.close()

