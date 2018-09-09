from .tag import Tag
from .token import Token
from .identifier import Identifier


class SymbolTable:

    def __init__(self):
        self.table = dict()
        self.table[Token(Tag.KEYWORD, "algoritmo")] = Identifier()
        self.table[Token(Tag.KEYWORD, "declare")] = Identifier()
        self.table[Token(Tag.KEYWORD, "fim")] = Identifier()
        self.table[Token(Tag.KEYWORD, "se")] = Identifier()
        self.table[Token(Tag.KEYWORD, "inicio")] = Identifier()
        self.table[Token(Tag.KEYWORD, "senao")] = Identifier()
        self.table[Token(Tag.KEYWORD, "enquanto")] = Identifier()
        self.table[Token(Tag.KEYWORD, "faca")] = Identifier()
        self.table[Token(Tag.KEYWORD, "para")] = Identifier()
        self.table[Token(Tag.KEYWORD, "ate")] = Identifier()
        self.table[Token(Tag.KEYWORD, "repita")] = Identifier()
        self.table[Token(Tag.KEYWORD, "escreva")] = Identifier()
        self.table[Token(Tag.KEYWORD, "leia")] = Identifier()
        self.table[Token(Tag.KEYWORD, "subrotina")] = Identifier()
        self.table[Token(Tag.KEYWORD, "Ou")] = Identifier()
        self.table[Token(Tag.KEYWORD, "E")] = Identifier()
        self.table[Token(Tag.KEYWORD, "Nao")] = Identifier()
        self.table[Token(Tag.KEYWORD, "logico")] = Identifier()
        self.table[Token(Tag.KEYWORD, "numerico")] = Identifier()
        self.table[Token(Tag.KEYWORD, "literal")] = Identifier()
        self.table[Token(Tag.KEYWORD, "nulo")] = Identifier()
        self.table[Token(Tag.KEYWORD, "retorne")] = Identifier()
        self.table[Token(Tag.KEYWORD, "verdadeiro")] = Identifier()
        self.table[Token(Tag.KEYWORD, "falso")] = Identifier()

    def __len__(self, other):
        return len(self.table)

    def __getitem__(self, item):
        for i in self.table.keys():
            if i.lexeme.lower() == item.lower():
                return i

        return None

