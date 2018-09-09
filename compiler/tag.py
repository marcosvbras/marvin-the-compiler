from enum import Enum, unique, auto


@unique
class Tag(Enum):

    # Language keyword
    KEYWORD = auto()

    # End of file
    END_OF_FILE = auto()

    # Operators
    OPERATOR_ASSIGN = auto()
    OPERATOR_LESS_THAN = auto()
    OPERATOR_LESS_THAN_EQUALS = auto()
    OPERATOR_GREATER_THAN = auto()
    OPERATOR_GREATER_THAN_EQUALS = auto()
    OPERATOR_EQUALS = auto()
    OPERATOR_DIFFERENT = auto()
    OPERATOR_DIVISION = auto()
    OPERATOR_MULTIPLICATION = auto()
    OPERATOR_MINUS = auto()
    OPERATOR_PLUS = auto()

    # Symbols
    SYMBOL_SEMICOLON = auto()
    SYMBOL_COMMA = auto()
    SYMBOL_OPEN_PARENTHESIS = auto()
    SYMBOL_CLOSE_PARENTHESIS = auto()

    # Identifier
    ID = auto()

    # Values
    VALUE_NUMERICO = auto()
    VALUE_LOGICO = auto()
    VALUE_LITERAL = auto()
    VALUE_NULO = auto()
