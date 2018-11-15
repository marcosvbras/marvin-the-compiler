from .tag import Tag
from .token import Token


class SymbolTable:

    def __init__(self):
        self.table = dict()
        self.table["algoritmo"] = Token(Tag.KEYWORD_ALGORITHM, "algoritmo")
        self.table["declare"] = Token(Tag.KEYWORD_DECLARE, "declare")
        self.table["fim"] = Token(Tag.KEYWORD_END, "fim")
        self.table["se"] = Token(Tag.KEYWORD_IF, "se")
        self.table["inicio"] = Token(Tag.KEYWORD_BEGIN, "inicio")
        self.table["senao"] = Token(Tag.KEYWORD_ELSE_IF, "senao")
        self.table["enquanto"] = Token(Tag.KEYWORD_WHILE, "enquanto")
        self.table["faca"] = Token(Tag.KEYWORD_DO, "faca")
        self.table["para"] = Token(Tag.KEYWORD_FOR, "para")
        self.table["ate"] = Token(Tag.KEYWORD_UNTIL, "ate")
        self.table["repita"] = Token(Tag.KEYWORD_REPEAT, "repita")
        self.table["escreva"] = Token(Tag.KEYWORD_WRITE, "escreva")
        self.table["leia"] = Token(Tag.KEYWORD_READ, "leia")
        self.table["subrotina"] = Token(Tag.KEYWORD_SUBROUTINE, "subrotina")
        self.table["Ou"] = Token(Tag.KEYWORD_OR, "Ou")
        self.table["E"] = Token(Tag.KEYWORD_AND, "E")
        self.table["Nao"] = Token(Tag.KEYWORD_NOT, "Nao")
        self.table["logico"] = Token(Tag.KEYWORD_BOOLEAN, "logico")
        self.table["numerico"] = Token(Tag.KEYWORD_NUMERIC, "numerico")
        self.table["literal"] = Token(Tag.KEYWORD_STRING, "literal")
        self.table["nulo"] = Token(Tag.KEYWORD_NULL, "nulo")
        self.table["retorne"] = Token(Tag.KEYWORD_RETURN, "retorne")
        self.table["verdadeiro"] = Token(Tag.KEYWORD_TRUE, "verdadeiro")
        self.table["falso"] = Token(Tag.KEYWORD_FALSE, "falso")

    def include(self, lexeme, tag):
        token = self.table.get(lexeme, None)

        if not token:
            token = Token(tag, lexeme)
            self.table[lexeme] = token

        return token

    def __len__(self):
        return len(self.table)

    def __getitem__(self, item):
        for token in self.table.values():
            if token.lexeme.lower() == item.lower():
                return token

        return None

    def __str__(self):
        print(self.table)

