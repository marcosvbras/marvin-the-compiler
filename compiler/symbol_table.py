from .tag import Tag
from .token import Token


class SymbolTable:

    def __init__(self):
        self.table = dict()
        self.table["algoritmo"] = Token(Tag.KEYWORD, "algoritmo")
        self.table["declare"] = Token(Tag.KEYWORD, "declare")
        self.table["fim"] = Token(Tag.KEYWORD, "fim")
        self.table["se"] = Token(Tag.KEYWORD, "se")
        self.table["inicio"] = Token(Tag.KEYWORD, "inicio")
        self.table["senao"] = Token(Tag.KEYWORD, "senao")
        self.table["enquanto"] = Token(Tag.KEYWORD, "enquanto")
        self.table["faca"] = Token(Tag.KEYWORD, "faca")
        self.table["para"] = Token(Tag.KEYWORD, "para")
        self.table["ate"] = Token(Tag.KEYWORD, "ate")
        self.table["repita"] = Token(Tag.KEYWORD, "repita")
        self.table["escreva"] = Token(Tag.KEYWORD, "escreva")
        self.table["leia"] = Token(Tag.KEYWORD, "leia")
        self.table["subrotina"] = Token(Tag.KEYWORD, "subrotina")
        self.table["Ou"] = Token(Tag.KEYWORD, "Ou")
        self.table["E"] = Token(Tag.KEYWORD, "E")
        self.table["Nao"] = Token(Tag.KEYWORD, "Nao")
        self.table["logico"] = Token(Tag.KEYWORD, "logico")
        self.table["numerico"] = Token(Tag.KEYWORD, "numerico")
        self.table["literal"] = Token(Tag.KEYWORD, "literal")
        self.table["nulo"] = Token(Tag.KEYWORD, "nulo")
        self.table["retorne"] = Token(Tag.KEYWORD, "retorne")
        self.table["verdadeiro"] = Token(Tag.KEYWORD, "verdadeiro")
        self.table["falso"] = Token(Tag.KEYWORD, "falso")

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

