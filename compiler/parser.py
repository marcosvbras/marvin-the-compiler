from .tag import Tag


class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.token = lexer.next_token()

    def raise_syntax_error(self, message):
        print("[Erro Sintatico] na linha " + self.token.line + " e coluna " + self.token.column + ": ")
        print(message + "\n")

    def advance(self):
        token = self.lexer.next_token()
        print("[DEBUG]" + str(token))

    def skip(self, message):
        self.raise_syntax_error(message)
        self.advance()

    def eat(self, tag):
        if self.token.tag == tag:
            self.advance()
            return True

        return False

    def compilador(self):
        if self.token.tag == Tag.KEYWORD_ALGORITHM:
            self.skip("Expected \"algoritmo\", found \"{}\" instead".format(self.token.lexeme))

        self.programa()

    def programa(self):
        if not self.eat(Tag.KEYWORD_ALGORITHM):
            self.skip("Expected \"algoritmo\", found \"{}\" instead".format(self.token.lexeme))

        self.regex_decl_var()
        self.lista_cmd()

        if not self.eat(Tag.KEYWORD_END):
            self.skip("Expected \"fim\", found \"{}\" instead".format(self.token.lexeme))

        if not self.eat(Tag.KEYWORD_ALGORITHM):
            self.skip("Expected \"algoritmo\", found \"{}\" instead".format(self.token.lexeme))

        self.lista_rotina()

    def regex_decl_var(self):
        pass

    def declara_var(self):
        pass

    def lista_rotina(self):
        self.lista_rotina_linha()

    def lista_rotina_linha(self):
        pass

    def rotina(self):
        if not self.eat(Tag.KEYWORD_SUBROUTINE):
            self.skip("Expected \"subrotina\", found \"{}\" instead".format(self.token.lexeme))

        if not self.eat(Tag.ID):
            self.skip("Expected an \"ID\", found \"{}\" instead".format(self.token.lexeme))

        if not self.eat(Tag.SYMBOL_OPEN_PARENTHESIS):
            self.skip("Expected \"(\", found \"{}\" instead".format(self.token.lexeme))

        self.lista_param()

        if not self.eat(Tag.SYMBOL_CLOSE_PARENTHESIS):
            self.skip("Expected \")\", found \"{}\" instead".format(self.token.lexeme))

        self.regex_decl_var()
        self.lista_cmd()
        self.retorno()

        if not self.eat(Tag.KEYWORD_END):
            self.skip("Expected \"fim\", found \"{}\" instead".format(self.token.lexeme))

        if not self.eat(Tag.KEYWORD_SUBROUTINE):
            self.skip("Expected \"subrotina\", found \"{}\" instead".format(self.token.lexeme))

    def lista_param(self):
        self.param()
        self.lista_param()

    def lista_param_linha(self):
        pass

    def param(self):
        self.lista_id()
        self.tipo()

    def lista_id(self):
        if not self.eat(Tag.ID):
            self.skip("Expected an \"ID\", found \"{}\" instead".format(self.token.lexeme))

        self.lista_id()

    def lista_id_linha(self):
        pass

    def retorno(self):
        pass

    def tipo(self):
        pass

    def lista_cmd(self):
        self.lista_cmd_linha()

    def lista_cmd_linha(self):
        pass

    def cmd(self):
        pass

    def cmd_linha(self):
        pass

    def cmd_se(self):
        if not self.eat(Tag.KEYWORD_IF):
            self.skip("Expected \"se\", found \"{}\" instead".format(self.token.lexeme))

        if not self.eat(Tag.SYMBOL_OPEN_PARENTHESIS):
            self.skip("Expected \"(\", found \"{}\" instead".format(self.token.lexeme))

        self.expressao()

        if not self.eat(Tag.SYMBOL_CLOSE_PARENTHESIS):
            self.skip("Expected \")\", found \"{}\" instead".format(self.token.lexeme))

        if not self.eat(Tag.KEYWORD_BEGIN):
            self.skip("Expected \"inicio\", found \"{}\" instead".format(self.token.lexeme))

        self.lista_cmd()

        if not self.eat(Tag.KEYWORD_END):
            self.skip("Expected \"fim\", found \"{}\" instead".format(self.token.lexeme))

        self.cmd_se_linha()

    def cmd_se_linha(self):
        pass

    def cmd_enquanto(self):
        if not self.eat(Tag.KEYWORD_WHILE):
            self.skip("Expected \"enquanto\", found \"{}\" instead".format(self.token.lexeme))

        if not self.eat(Tag.SYMBOL_OPEN_PARENTHESIS):
            self.skip("Expected \"(\", found \"{}\" instead".format(self.token.lexeme))

        self.expressao()

        if not self.eat(Tag.SYMBOL_CLOSE_PARENTHESIS):
            self.skip("Expected \")\", found \"{}\" instead".format(self.token.lexeme))

        if not self.eat(Tag.KEYWORD_DO):
            self.skip("Expected \"faca\", found \"{}\" instead".format(self.token.lexeme))

        if not self.eat(Tag.KEYWORD_BEGIN):
            self.skip("Expected \"inicio\", found \"{}\" instead".format(self.token.lexeme))

        self.lista_cmd()

        if not self.eat(Tag.KEYWORD_END):
            self.skip("Expected \"fim\", found \"{}\" instead".format(self.token.lexeme))

    def cmd_para(self):
        if not self.eat(Tag.KEYWORD_FOR):
            self.skip("Expected \"para\", found \"{}\" instead".format(self.token.lexeme))

        if not self.eat(Tag.ID):
            self.skip("Expected an \"ID\", found \"{}\" instead".format(self.token.lexeme))

        self.cmd_atrib()

        if not self.eat(Tag.KEYWORD_UNTIL):
            self.skip("Expected \"ate\", found \"{}\" instead".format(self.token.lexeme))

        self.expressao()

        if not self.eat(Tag.KEYWORD_DO):
            self.skip("Expected \"faca\", found \"{}\" instead".format(self.token.lexeme))

        if not self.eat(Tag.KEYWORD_BEGIN):
            self.skip("Expected \"inicio\", found \"{}\" instead".format(self.token.lexeme))

        self.lista_cmd()

        if not self.eat(Tag.KEYWORD_END):
            self.skip("Expected \"fim\", found \"{}\" instead".format(self.token.lexeme))

    def cmd_repita(self):
        if not self.eat(Tag.KEYWORD_REPEAT):
            self.skip("Expected \"repita\", found \"{}\" instead".format(self.token.lexeme))

        self.lista_cmd()

        if not self.eat(Tag.KEYWORD_UNTIL):
            self.skip("Expected \"ate\", found \"{}\" instead".format(self.token.lexeme))

        self.expressao()

    def cmd_atrib(self):
        if not self.eat(Tag.OPERATOR_ASSIGN):
            self.skip("Expected \"<--\", found \"{}\" instead".format(self.token.lexeme))

        self.expressao()

        if not self.eat(Tag.SYMBOL_SEMICOLON):
            self.skip("Expected \";\", found \"{}\" instead".format(self.token.lexeme))

    def cmd_chama_rotina(self):
        if not self.eat(Tag.SYMBOL_OPEN_PARENTHESIS):
            self.skip("Expected \"(\", found \"{}\" instead".format(self.token.lexeme))

        self.regex_exp()

        if not self.eat(Tag.SYMBOL_CLOSE_PARENTHESIS):
            self.skip("Expected \")\", found \"{}\" instead".format(self.token.lexeme))

        if not self.eat(Tag.SYMBOL_SEMICOLON):
            self.skip("Expected \";\", found \"{}\" instead".format(self.token.lexeme))

    def regex_exp(self):
        pass

    def regex_exp_linha(self):
        pass

    def cmd_escreva(self):
        if not self.eat(Tag.KEYWORD_WRITE):
            self.skip("Expected \"escreva\", found \"{}\" instead".format(self.token.lexeme))

        if not self.eat(Tag.SYMBOL_OPEN_PARENTHESIS):
            self.skip("Expected \"(\", found \"{}\" instead".format(self.token.lexeme))

        self.expressao()

        if not self.eat(Tag.SYMBOL_CLOSE_PARENTHESIS):
            self.skip("Expected \")\", found \"{}\" instead".format(self.token.lexeme))

        if not self.eat(Tag.SYMBOL_SEMICOLON):
            self.skip("Expected \";\", found \"{}\" instead".format(self.token.lexeme))

    def cmd_leia(self):
        if not self.eat(Tag.KEYWORD_READ):
            self.skip("Expected \"leia\", found \"{}\" instead".format(self.token.lexeme))

        if not self.eat(Tag.SYMBOL_OPEN_PARENTHESIS):
            self.skip("Expected \"(\", found \"{}\" instead".format(self.token.lexeme))

        if not self.eat(Tag.ID):
            self.skip("Expected an \"ID\", found \"{}\" instead".format(self.token.lexeme))

        if not self.eat(Tag.SYMBOL_CLOSE_PARENTHESIS):
            self.skip("Expected \")\", found \"{}\" instead".format(self.token.lexeme))

        if not self.eat(Tag.SYMBOL_SEMICOLON):
            self.skip("Expected \";\", found \"{}\" instead".format(self.token.lexeme))

    def expressao(self):
        self.exp1()
        self.exp_linha()

    def exp_linha(self):
        pass

    def exp1(self):
        self.exp2()
        self.exp1_linha()

    def exp1_linha(self):
        pass

    def exp2(self):
        self.exp3()
        self.exp2_linha()

    def exp2_linha(self):
        pass

    def exp3(self):
        self.exp4()
        self.exp3_linha()

    def exp3_linha(self):
        pass

    def exp4(self):
        pass

    def exp4_linha(self):
        pass

    def op_unario(self):
        if not self.eat(Tag.KEYWORD_NOT):
            self.skip("Expected \"Nao\", found \"{}\" instead".format(self.token.lexeme))


























