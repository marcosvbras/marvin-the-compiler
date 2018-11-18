from enum import Enum, unique, auto


@unique
class Tag(Enum):

    # Language keyword
    KEYWORD = auto()
    KEYWORD_ALGORITHM = auto()
    KEYWORD_DECLARE = auto()
    KEYWORD_END = auto()
    KEYWORD_IF = auto()
    KEYWORD_BEGIN = auto()
    KEYWORD_ELSE = auto()
    KEYWORD_WHILE = auto()
    KEYWORD_DO = auto()
    KEYWORD_FOR = auto()
    KEYWORD_UNTIL = auto()
    KEYWORD_REPEAT = auto()
    KEYWORD_WRITE = auto()
    KEYWORD_READ = auto()
    KEYWORD_SUBROUTINE = auto()
    KEYWORD_OR = auto()
    KEYWORD_AND = auto()
    KEYWORD_NOT = auto()
    KEYWORD_BOOLEAN = auto()
    KEYWORD_NUMERIC = auto()
    KEYWORD_STRING = auto()
    KEYWORD_NULL = auto()
    KEYWORD_RETURN = auto()
    KEYWORD_TRUE = auto()
    KEYWORD_FALSE = auto()

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
    VALUE_LITERAL = auto()
