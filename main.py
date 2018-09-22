from compiler.lexer import Lexer
from compiler.tag import Tag


def run():
    lexer = Lexer('primeiro_portugolo.ptgl')
    token = lexer.next_token()

    while token and token.tag != Tag.END_OF_FILE:
        print(str(token))
        token = lexer.next_token()

    print("\n\n\nSymbol Table:")
    lexer.print_symbol_table()


if __name__ == '__main__':
    run()