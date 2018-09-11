from .symbol_table import SymbolTable
from .token import Token
from .tag import Tag

# TODO: Check "verdadeiro" and "falso"


class Lexer:

    END_OF_FILE = ''
    NEW_LINE = '\n'
    WHITE_SPACE = ' '
    TABULATION = '\t'

    def __init__(self, file_name):
        self.last_read_char = None
        self.current_line = 1
        self.current_column = 1
        self.file = None
        self.symbolTable = None
        self.file_name = file_name
        self.symbol_table = SymbolTable()

        try:
            self.file = open(self.file_name, 'r')
        except Exception as ex:
            raise Exception("File not found")

    def seek_to_previous_position(self):
        if self.last_read_char is not None:
            self.file.seek(self.file.tell() - 1)
            self.current_column -= 1

    def next_token(self):
        lexeme = ""
        current_state = 1

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
                    # self.current_column += 1
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
                    lexeme += self.last_read_char
                    current_state = 21

            elif current_state == 2:
                if self.last_read_char.isalpha() or self.last_read_char.isdigit():  # Stay at state 2
                    lexeme += self.last_read_char
                else:  # Other
                    self.seek_to_previous_position()
                    token = self.symbol_table[lexeme]

                    if token is None:
                        return Token(Tag.ID, lexeme, self.current_line, self.current_column)
                    else:
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
                elif self.last_read_char == '>':  # Go to state 13
                    lexeme += self.last_read_char
                    return Token(Tag.OPERATOR_DIFFERENT, lexeme, self.current_line, self.current_column)
                else:  # 10
                    self.seek_to_previous_position()
                    return Token(Tag.OPERATOR_LESS_THAN, lexeme, self.current_line, self.current_column)

            elif current_state == 14:
                if self.last_read_char == '=':  # Go to state 15
                    lexeme += self.last_read_char
                    return Token(Tag.OPERATOR_GREATER_THAN_EQUALS, lexeme, self.current_line, self.current_column)
                else:  # Go to state 16
                    self.seek_to_previous_position()
                    return Token(Tag.OPERATOR_GREATER_THAN, lexeme, self.current_line, self.current_column)

            elif current_state == 12:
                if self.last_read_char == '-':  # Go to state 12
                    lexeme += self.last_read_char
                    return Token(Tag.OPERATOR_ASSIGN, lexeme, self.current_line, self.current_column)
                else:
                    # TODO: Throw error if it reads something different of '<--'
                    pass

            elif current_state == 21:
                if self.last_read_char == '*':  # Go to state 22
                    current_state = 22
                elif self.last_read_char == '/':  # Go to state 25
                    current_state = 25
                else:  # Go to state 24 - Final State - Return the token and the file pointer
                    self.seek_to_previous_position()
                    return Token(Tag.OPERATOR_DIVISION, lexeme, self.current_line, self.current_column)

            elif current_state == 22:
                if self.last_read_char == '*':  # Go to state 23
                    current_state = 23

            elif current_state == 23:
                if self.last_read_char == '/':  # Return to initial state
                    current_state = 1
                elif self.last_read_char == '*':  # Stay at state 23
                    pass
                else:  # Return to state 22
                    current_state = 22

            elif current_state == 25:
                if self.last_read_char == self.NEW_LINE:  # Return to initial state
                    current_state = 1

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
                    lexeme += self.last_read_char
                    current_state = 29
                else:
                    # TODO: throw error if it reads something different after the "."
                    pass

            elif current_state == 29:
                if self.last_read_char.isdigit():  # Keep in state 29
                    lexeme += self.last_read_char
                else:  # Go to state 30 - Final State - Return the token and the file pointer
                    self.seek_to_previous_position()
                    return Token(Tag.VALUE_NUMERICO, lexeme, self.current_line, self.current_column)

            elif current_state == 31:
                if self.last_read_char == self.END_OF_FILE:
                    # TODO: throw error if it reaches EOF without close string
                    pass
                elif self.is_ascii(self.last_read_char):
                    lexeme += self.last_read_char
                elif self.last_read_char == '"':
                    return Token(Tag.VALUE_LITERAL, lexeme, self.current_line, self.current_column)
                else:
                    # TODO: throw error if it is not ASCII
                    pass

    def is_ascii(self, string):
        try:
            string.encode('ascii')
        except UnicodeEncodeError:
            return False
        else:
            return True

    def throw_error(self, error):
        pass

    def __del__(self):
        self.file.close()

#     return word.encode('ascii').isalpha()
