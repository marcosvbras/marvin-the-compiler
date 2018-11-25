from .tag import Tag


class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.token = lexer.next_token()
        self.messageFormat = "Expected \"{}\", found \"{}\" instead"

    def raise_syntax_error(self, message=None):
        if message is not None:
            print("[Syntax Error] at {}:{} {}\n".format(self.token.line, self.token.column, message))

    def advance(self):
        self.token = self.lexer.next_token()
        print("[DEBUG]" + str(self.token))

    def skip(self, message=None):
        if message is not None:
            self.raise_syntax_error(message)
        self.advance()

    def eat(self, tag):
        if self.token.tag == tag:
            self.advance()
            return True

        return False

    # Compilador → Programa $ 1
    def compilador(self):
        if self.token.tag != Tag.KEYWORD_ALGORITHM:
            self.skip(self.messageFormat.format("algoritmo", self.token.lexeme))

        self.programa()

    # Programa → "algoritmo" RegexDeclVar ListaCmd "fim" "algoritmo" ListaRotina 2
    def programa(self):
        if not self.eat(Tag.KEYWORD_ALGORITHM):
            self.skip(self.messageFormat.format("algoritmo", self.token.lexeme))

        self.regex_decl_var()
        self.lista_cmd()

        if not self.eat(Tag.KEYWORD_END):
            self.raise_syntax_error(self.messageFormat.format("fim", self.token.lexeme))

        if not self.eat(Tag.KEYWORD_ALGORITHM):
            self.raise_syntax_error(self.messageFormat.format("algoritmo", self.token.lexeme))

        self.lista_rotina()

    # RegexDeclVar → “declare” Tipo ListaID";" DeclaraVar 3 | ε 4
    def regex_decl_var(self):
        if self.token.tag == Tag.KEYWORD_DECLARE:
            self.eat(Tag.KEYWORD_DECLARE)
            self.tipo()
            self.lista_id()

            if not self.eat(Tag.SYMBOL_SEMICOLON):
                self.raise_syntax_error(self.messageFormat.format(";", self.token.lexeme))

            self.declara_var()
        elif self.token.tag == Tag.KEYWORD_END or self.token.tag == Tag.ID or self.token.tag == Tag.KEYWORD_RETURN \
                or self.token.tag == Tag.KEYWORD_IF or self.token.tag == Tag.KEYWORD_WHILE \
                or self.token.tag == Tag.KEYWORD_FOR or self.token.tag == Tag.KEYWORD_REPEAT \
                or self.token.tag == Tag.KEYWORD_WRITE or self.token.tag == Tag.KEYWORD_READ:
            return
        else:
            self.skip(
                self.messageFormat.format(
                    "declare, fim, ID, retorne, se, enquanto, para, repita, escreva, leia", self.token.lexeme)
            )
            if self.token.tag is not Tag.END_OF_FILE:
                self.regex_decl_var()

    # DeclaraVar → Tipo ListaID ";" DeclaraVar 5 | ε 6
    def declara_var(self):
        if self.token.tag == Tag.KEYWORD_END or self.token.tag == Tag.ID or self.token.tag == Tag.KEYWORD_RETURN \
                or self.token.tag == Tag.KEYWORD_IF or self.token.tag == Tag.KEYWORD_WHILE \
                or self.token.tag == Tag.KEYWORD_FOR or self.token.tag == Tag.KEYWORD_REPEAT \
                or self.token.tag == Tag.KEYWORD_WRITE or self.token.tag == Tag.KEYWORD_READ:
            return
        elif self.token.tag == Tag.KEYWORD_BOOLEAN or self.token.tag == Tag.KEYWORD_NUMERIC \
                or self.token.tag == Tag.KEYWORD_STRING or self.token.tag == Tag.KEYWORD_NULL:
            self.tipo()
            self.lista_id()

            if not self.eat(Tag.SYMBOL_SEMICOLON):
                self.raise_syntax_error(self.messageFormat.format(";", self.token.lexeme))

            self.declara_var()
        else:
            self.skip(
                self.messageFormat.format(
                    "fim, ID, retorne, se, enquanto, para, repita, escreva, leia, logico, numerico, literal, nulo",
                    self.token.lexeme
                )
            )
            if self.token.tag is not Tag.END_OF_FILE:
                self.declara_var()

    # ListaRotina → ListaRotina’ 7
    def lista_rotina(self):
        if self.token.tag == Tag.KEYWORD_SUBROUTINE or self.token.tag == Tag.END_OF_FILE:
            self.lista_rotina_linha()
        else:
            self.skip(self.messageFormat.format("subrotina", self.token.lexeme))

            if self.token.tag is not Tag.END_OF_FILE:
                self.lista_rotina()

    # ListaRotina’ → Rotina ListaRotina’ 8 | ε 9
    def lista_rotina_linha(self):
        if self.token.tag == Tag.KEYWORD_SUBROUTINE:
            self.rotina()
            self.lista_rotina_linha()
        elif self.token.tag == Tag.END_OF_FILE:
            return
        else:
            self.skip(self.messageFormat.format("subrotina", self.token.lexeme))

            if self.token.tag is not Tag.END_OF_FILE:
                self.lista_rotina_linha()

    # Rotina → "subrotina" ID "(" ListaParam ")" RegexDeclVar ListaCmd Retorno "fim" "subrotina" 10
    def rotina(self):
        if self.token.tag == Tag.KEYWORD_SUBROUTINE:
            self.eat(Tag.KEYWORD_SUBROUTINE)

            if not self.eat(Tag.ID):
                self.raise_syntax_error(self.messageFormat.format("ID", self.token.lexeme))

            if not self.eat(Tag.SYMBOL_OPEN_PARENTHESIS):
                self.raise_syntax_error(self.messageFormat.format("(", self.token.lexeme))

            self.lista_param()

            if not self.eat(Tag.SYMBOL_CLOSE_PARENTHESIS):
                self.raise_syntax_error(self.messageFormat.format(")", self.token.lexeme))

            self.regex_decl_var()
            self.lista_cmd()
            self.retorno()

            if not self.eat(Tag.KEYWORD_END):
                self.raise_syntax_error(self.messageFormat.format("fim", self.token.lexeme))

            if not self.eat(Tag.KEYWORD_SUBROUTINE):
                self.raise_syntax_error(self.messageFormat.format("subrotina", self.token.lexeme))
        else:
            self.raise_syntax_error(self.messageFormat.format("subrotina", self.token.lexeme))

            # Synch
            if self.token.tag == Tag.END_OF_FILE:
                return

            # Skip
            self.skip(None)

            if self.token.tag is not Tag.END_OF_FILE:
                self.rotina()

    # ListaParam → Param ListaParam’ 11
    def lista_param(self):
        if self.token.tag == Tag.ID:
            self.param()
            self.lista_param_linha()
        else:
            self.skip(self.messageFormat.format("ID", self.token.lexeme))

            if self.token.tag is not Tag.END_OF_FILE:
                self.rotina()

    # ListaParam’ → "," ListaParam 12 | ε 13
    def lista_param_linha(self):
        if self.token.tag == Tag.SYMBOL_CLOSE_PARENTHESIS:
            return
        elif self.token.tag == Tag.SYMBOL_COMMA:
            self.eat(Tag.SYMBOL_COMMA)
            self.lista_param()
        else:
            self.skip(self.messageFormat.format("), ,", self.token.lexeme))

            if self.token.tag is not Tag.END_OF_FILE:
                self.lista_param_linha()

    # Param → ListaID Tipo 14
    def param(self):
        if self.token.tag == Tag.ID:
            self.lista_id()
            self.tipo()
        else:
            self.skip(self.messageFormat.format("ID", self.token.lexeme))

            if self.token.tag is not Tag.END_OF_FILE:
                self.param()

    # ListaID → ID ListaID’ 15
    def lista_id(self):
        if self.token.tag == Tag.ID:
            self.eat(Tag.ID)
            self.lista_id_linha()
        else:
            self.skip(self.messageFormat.format("ID", self.token.lexeme))

            if self.token.tag is not Tag.END_OF_FILE:
                self.lista_id()

    # ListaID’ → "," ListaID 16 | ε 17
    def lista_id_linha(self):
        if self.token.tag == Tag.SYMBOL_SEMICOLON or self.token.tag == Tag.KEYWORD_BOOLEAN \
                or self.token.tag == Tag.KEYWORD_NUMERIC or self.token.tag == Tag.KEYWORD_STRING \
                or self.token.tag == Tag.KEYWORD_NULL:
            return
        elif self.token.tag == Tag.SYMBOL_COMMA:
            self.eat(Tag.SYMBOL_COMMA)
            self.lista_id()
        else:
            self.skip(self.messageFormat.format(";, ,, logico, numerico, literal, nulo", self.token.lexeme))

            if self.token.tag is not Tag.END_OF_FILE:
                self.lista_id_linha()

    # Retorno → "retorne" Expressao 18 | ε 19
    def retorno(self):
        if self.token.tag == Tag.KEYWORD_END:
            return
        elif self.token.tag == Tag.KEYWORD_RETURN:
            self.eat(Tag.KEYWORD_RETURN)
            self.expressao()
        else:
            self.skip(self.messageFormat.format("fim, retorne", self.token.lexeme))

            if self.token.tag is not Tag.END_OF_FILE:
                self.retorno()

    # Tipo → "logico" 20 | "numerico" 21 | "literal" 22 | "nulo" 23
    def tipo(self):
        if self.token.tag == Tag.KEYWORD_BOOLEAN:
            self.eat(Tag.KEYWORD_BOOLEAN)
        elif self.token.tag == Tag.KEYWORD_NUMERIC:
            self.eat(Tag.KEYWORD_NUMERIC)
        elif self.token.tag == Tag.KEYWORD_STRING:
            self.eat(Tag.KEYWORD_STRING)
        elif self.token.tag == Tag.KEYWORD_NULL:
            self.eat(Tag.KEYWORD_NULL)
        else:
            self.raise_syntax_error(self.messageFormat.format("logico, numerico, literal, nulo", self.token.lexeme))

            # Synch
            if self.token.tag == Tag.ID or self.token.tag == Tag.SYMBOL_COMMA \
                    or self.token.tag == Tag.SYMBOL_CLOSE_PARENTHESIS:
                return
            else:  # Skip
                self.skip()

                if self.token.tag is not Tag.END_OF_FILE:
                    self.tipo()

    # ListaCmd → ListaCmd’ 24
    def lista_cmd(self):
        if self.token.tag == Tag.KEYWORD_END or self.token.tag == Tag.ID or self.token.tag == Tag.KEYWORD_RETURN \
                or self.token.tag == Tag.KEYWORD_IF or self.token.tag == Tag.KEYWORD_WHILE \
                or self.token.tag == Tag.KEYWORD_FOR or self.token.tag == Tag.KEYWORD_UNTIL \
                or self.token.tag == Tag.KEYWORD_REPEAT or self.token.tag == Tag.KEYWORD_WRITE \
                or self.token.tag == Tag.KEYWORD_READ:
            self.lista_cmd_linha()
        else:
            self.skip(
                self.messageFormat.format("fim, ID, retorne, se, enquanto, para, ate, repita, escreva, leia", self.token.lexeme))

            if self.token.tag is not Tag.END_OF_FILE:
                self.lista_cmd()

    # ListaCmd’ → Cmd ListaCmd’ 25 | ε 26
    def lista_cmd_linha(self):
        if self.token.tag == Tag.KEYWORD_END or self.token.tag == Tag.KEYWORD_RETURN or self.token.tag == Tag.KEYWORD_UNTIL:
            return
        elif self.token.tag == Tag.ID or self.token.tag == Tag.KEYWORD_IF or self.token.tag == Tag.KEYWORD_WHILE \
                or self.token.tag == Tag.KEYWORD_FOR or self.token.tag == Tag.KEYWORD_REPEAT \
                or self.token.tag == Tag.KEYWORD_WRITE or self.token.tag == Tag.KEYWORD_READ:
            self.cmd()
            self.lista_cmd_linha()
        else:
            self.skip(
                self.messageFormat.format(
                    "fim, retorne, ate, ID, se, enquanto, para, repita, escreva, leia", self.token.lexeme))

            if self.token.tag is not Tag.END_OF_FILE:
                self.lista_cmd_linha()

    # Cmd → CmdSe 27 | CmdEnquanto 28 | CmdPara 29 | CmdRepita 30 | ID Cmd’ 31 | CmdEscreva 32 | CmdLeia 33
    def cmd(self):
        if self.token.tag == Tag.ID:
            self.eat(Tag.ID)
            self.cmd_linha()
        elif self.token.tag == Tag.KEYWORD_IF:
            self.cmd_se()
        elif self.token.tag == Tag.KEYWORD_WHILE:
            self.cmd_enquanto()
        elif self.token.tag == Tag.KEYWORD_FOR:
            self.cmd_para()
        elif self.token.tag == Tag.KEYWORD_REPEAT:
            self.cmd_repita()
        elif self.token.tag == Tag.KEYWORD_WRITE:
            self.cmd_escreva()
        elif self.token.tag == Tag.KEYWORD_READ:
            self.cmd_leia()
        else:
            self.raise_syntax_error(
                self.messageFormat.format("ID, se, enquanto, para, repita, escreva, leia", self.token.lexeme))

            # Synch
            if self.token.tag == Tag.KEYWORD_END or self.token.tag == Tag.KEYWORD_RETURN \
                    or self.token.tag == Tag.KEYWORD_UNTIL:
                return
            else:  # Skip
                self.skip()

                if self.token.tag is not Tag.END_OF_FILE:
                    self.cmd()

    # Cmd’ → CmdAtrib 34 | CmdChamaRotina 35
    def cmd_linha(self):
        if self.token.tag == Tag.SYMBOL_OPEN_PARENTHESIS:
            self.cmd_chama_rotina()
        elif self.token.tag == Tag.OPERATOR_ASSIGN:
            self.cmd_atrib()
        else:
            self.raise_syntax_error(self.messageFormat.format("(, <--", self.token.lexeme))

            # Synch
            if self.token.tag == Tag.KEYWORD_END or self.token.tag == Tag.ID or self.token.tag == Tag.KEYWORD_RETURN \
                    or self.token.tag == Tag.KEYWORD_IF or self.token.tag == Tag.KEYWORD_WHILE \
                    or self.token.tag == Tag.KEYWORD_FOR or self.token.tag == Tag.KEYWORD_UNTIL \
                    or self.token.tag == Tag.KEYWORD_REPEAT or self.token.tag == Tag.KEYWORD_WRITE \
                    or self.token.tag == Tag.KEYWORD_READ:
                return
            else:  # Skip
                self.skip()

                if self.token.tag is not Tag.END_OF_FILE:
                    self.cmd_linha()

    # CmdSe → "se" "(" Expressao ")" "inicio" ListaCmd "fim" CmdSe’ 36
    def cmd_se(self):
        if self.token.tag == Tag.KEYWORD_IF:
            self.eat(Tag.KEYWORD_IF)

            if not self.eat(Tag.SYMBOL_OPEN_PARENTHESIS):
                self.raise_syntax_error(self.messageFormat.format("(", self.token.lexeme))

            self.expressao()

            if not self.eat(Tag.SYMBOL_CLOSE_PARENTHESIS):
                self.raise_syntax_error(self.messageFormat.format(")", self.token.lexeme))

            if not self.eat(Tag.KEYWORD_BEGIN):
                self.raise_syntax_error(self.messageFormat.format("inicio", self.token.lexeme))

            self.lista_cmd()

            if not self.eat(Tag.KEYWORD_END):
                self.raise_syntax_error(self.messageFormat.format("fim", self.token.lexeme))

            self.cmd_se_linha()
        else:
            self.raise_syntax_error(self.messageFormat.format("se", self.token.lexeme))

            # Synch
            if self.token.tag == Tag.KEYWORD_END or self.token.tag == Tag.ID or self.token.tag == Tag.KEYWORD_RETURN \
                    or self.token.tag == Tag.KEYWORD_WHILE or self.token.tag == Tag.KEYWORD_FOR \
                    or self.token.tag == Tag.KEYWORD_UNTIL or self.token.tag == Tag.KEYWORD_REPEAT \
                    or self.token.tag == Tag.KEYWORD_WRITE or self.token.tag == Tag.KEYWORD_READ:
                return
            else:  # Skip
                self.skip()

                if self.token.tag is not Tag.END_OF_FILE:
                    self.cmd_se()

    # CmdSe’ → "senao" "inicio" ListaCmd "fim" 37 | ε 38
    def cmd_se_linha(self):
        if self.token.tag == Tag.KEYWORD_ELSE:
            self.eat(Tag.KEYWORD_ELSE)

            if not self.eat(Tag.KEYWORD_BEGIN):
                self.raise_syntax_error(self.messageFormat.format("inicio", self.token.lexeme))

            self.lista_cmd()

            if not self.eat(Tag.KEYWORD_END):
                self.raise_syntax_error(self.messageFormat.format("fim", self.token.lexeme))
        elif self.token.tag == Tag.KEYWORD_END or self.token.tag == Tag.ID or self.token.tag == Tag.KEYWORD_RETURN \
                or self.token.tag == Tag.KEYWORD_IF or self.token.tag == Tag.KEYWORD_WHILE \
                or self.token.tag == Tag.KEYWORD_FOR or self.token.tag == Tag.KEYWORD_UNTIL \
                or self.token.tag == Tag.KEYWORD_REPEAT or self.token.tag == Tag.KEYWORD_WRITE \
                or self.token.tag == Tag.KEYWORD_READ:
            return
        else:
            self.skip(
                self.messageFormat.format(
                    "senao, fim, ID, retorne, se, enquanto, para, ate, repita, escreva, leia", self.token.lexeme))

            if self.token.tag is not Tag.END_OF_FILE:
                self.cmd_se_linha()

    # CmdEnquanto → "enquanto" "(" Expressao ")" "faca" "inicio" ListaCmd "fim" 39
    def cmd_enquanto(self):
        if self.token.tag == Tag.KEYWORD_WHILE:
            self.eat(Tag.KEYWORD_WHILE)

            if not self.eat(Tag.SYMBOL_OPEN_PARENTHESIS):
                self.raise_syntax_error(self.messageFormat.format("(", self.token.lexeme))

            self.expressao()

            if not self.eat(Tag.SYMBOL_CLOSE_PARENTHESIS):
                self.raise_syntax_error(self.messageFormat.format(")", self.token.lexeme))

            if not self.eat(Tag.KEYWORD_DO):
                self.raise_syntax_error(self.messageFormat.format("faca", self.token.lexeme))

            if not self.eat(Tag.KEYWORD_BEGIN):
                self.raise_syntax_error(self.messageFormat.format("inicio", self.token.lexeme))

            self.lista_cmd()

            if not self.eat(Tag.KEYWORD_END):
                self.raise_syntax_error(self.messageFormat.format("fim", self.token.lexeme))
        else:
            self.raise_syntax_error(self.messageFormat.format("enquanto", self.token.lexeme))

            # Synch
            if self.token.tag == Tag.KEYWORD_END or self.token.tag == Tag.ID or self.token.tag == Tag.KEYWORD_RETURN \
                    or self.token.tag == Tag.KEYWORD_IF or self.token.tag == Tag.KEYWORD_FOR \
                    or self.token.tag == Tag.KEYWORD_UNTIL or self.token.tag == Tag.KEYWORD_REPEAT \
                    or self.token.tag == Tag.KEYWORD_WRITE or self.token.tag == Tag.KEYWORD_READ:
                return
            else:  # Skip
                self.skip()

                if self.token.tag is not Tag.END_OF_FILE:
                    self.cmd_enquanto()

    # CmdPara → "para" ID CmdAtrib "ate" Expressao "faca" "inicio" ListaCmd "fim" 40
    def cmd_para(self):
        if self.token.tag == Tag.KEYWORD_FOR:
            self.eat(Tag.KEYWORD_FOR)

            if not self.eat(Tag.ID):
                self.raise_syntax_error(self.messageFormat.format("ID", self.token.lexeme))

            self.cmd_atrib()

            if not self.eat(Tag.KEYWORD_UNTIL):
                self.raise_syntax_error(self.messageFormat.format("ate", self.token.lexeme))

            self.expressao()

            if not self.eat(Tag.KEYWORD_DO):
                self.raise_syntax_error(self.messageFormat.format("faca", self.token.lexeme))

            if not self.eat(Tag.KEYWORD_BEGIN):
                self.raise_syntax_error(self.messageFormat.format("inicio", self.token.lexeme))

            self.lista_cmd()

            if not self.eat(Tag.KEYWORD_END):
                self.raise_syntax_error(self.messageFormat.format("fim", self.token.lexeme))
        else:
            self.raise_syntax_error(self.messageFormat.format("para", self.token.lexeme))

            # Synch
            if self.token.tag == Tag.KEYWORD_END or self.token.tag == Tag.ID or self.token.tag == Tag.KEYWORD_RETURN \
                    or self.token.tag == Tag.KEYWORD_IF or self.token.tag == Tag.KEYWORD_WHILE \
                    or self.token.tag == Tag.KEYWORD_UNTIL or self.token.tag == Tag.KEYWORD_REPEAT \
                    or self.token.tag == Tag.KEYWORD_WRITE or self.token.tag == Tag.KEYWORD_READ:
                return
            else:  # Skip
                self.skip()

                if self.token.tag is not Tag.END_OF_FILE:
                    self.cmd_para()

    # CmdRepita → "repita" ListaCmd "ate" Expressao 41
    def cmd_repita(self):
        if self.token.tag == Tag.KEYWORD_REPEAT:
            self.eat(Tag.KEYWORD_REPEAT)
            self.lista_cmd()

            if not self.eat(Tag.KEYWORD_UNTIL):
                self.raise_syntax_error(self.messageFormat.format("ate", self.token.lexeme))

            self.expressao()
        else:
            self.raise_syntax_error(self.messageFormat.format("repita", self.token.lexeme))

            # Synch
            if self.token.tag == Tag.KEYWORD_END or self.token.tag == Tag.ID or self.token.tag == Tag.KEYWORD_RETURN \
                    or self.token.tag == Tag.KEYWORD_IF or self.token.tag == Tag.KEYWORD_WHILE \
                    or self.token.tag == Tag.KEYWORD_FOR or self.token.tag == Tag.KEYWORD_UNTIL \
                    or self.token.tag == Tag.KEYWORD_WRITE or self.token.tag == Tag.KEYWORD_READ:
                return
            else:  # Skip
                self.skip()

                if self.token.tag is not Tag.END_OF_FILE:
                    self.cmd_repita()

    # CmdAtrib → "<--" Expressao ";" 42
    def cmd_atrib(self):
        if self.token.tag == Tag.OPERATOR_ASSIGN:
            self.eat(Tag.OPERATOR_ASSIGN)

            self.expressao()

            if not self.eat(Tag.SYMBOL_SEMICOLON):
                self.raise_syntax_error(self.messageFormat.format(";", self.token.lexeme))
        else:
            self.raise_syntax_error(self.messageFormat.format("<--", self.token.lexeme))

            # Synch
            if self.token.tag == Tag.KEYWORD_END or self.token.tag == Tag.ID or self.token.tag == Tag.KEYWORD_RETURN \
                    or self.token.tag == Tag.KEYWORD_IF or self.token.tag == Tag.KEYWORD_WHILE \
                    or self.token.tag == Tag.KEYWORD_FOR or self.token.tag == Tag.KEYWORD_UNTIL \
                    or self.token.tag == Tag.KEYWORD_REPEAT or self.token.tag == Tag.KEYWORD_WRITE \
                    or self.token.tag == Tag.KEYWORD_READ:
                return
            else:  # Skip
                self.skip()

                if self.token.tag is not Tag.END_OF_FILE:
                    self.cmd_atrib()

    # CmdChamaRotina → "(" RegexExp ")" ";" 43
    def cmd_chama_rotina(self):
        if self.token.tag == Tag.SYMBOL_OPEN_PARENTHESIS:
            self.eat(Tag.SYMBOL_OPEN_PARENTHESIS)

            self.regex_exp()

            if not self.eat(Tag.SYMBOL_CLOSE_PARENTHESIS):
                self.raise_syntax_error(self.messageFormat.format(")", self.token.lexeme))

            if not self.eat(Tag.SYMBOL_SEMICOLON):
                self.raise_syntax_error(self.messageFormat.format(";", self.token.lexeme))
        else:
            self.raise_syntax_error(self.messageFormat.format("(", self.token.lexeme))

            # Synch
            if self.token.tag == Tag.KEYWORD_END or self.token.tag == Tag.ID or self.token.tag == Tag.KEYWORD_RETURN \
                    or self.token.tag == Tag.KEYWORD_IF or self.token.tag == Tag.KEYWORD_WHILE \
                    or self.token.tag == Tag.KEYWORD_FOR or self.token.tag == Tag.KEYWORD_UNTIL \
                    or self.token.tag == Tag.KEYWORD_REPEAT or self.token.tag == Tag.KEYWORD_WRITE \
                    or self.token.tag == Tag.KEYWORD_READ:
                return
            else:  # Skip
                self.skip()

                if self.token.tag is not Tag.END_OF_FILE:
                    self.cmd_chama_rotina()

    # RegexExp → Expressao RegexExp’ 44 | ε 45
    def regex_exp(self):
        if self.token.tag == Tag.SYMBOL_CLOSE_PARENTHESIS:
            return
        elif self.token.tag == Tag.ID or self.token.tag == Tag.SYMBOL_OPEN_PARENTHESIS \
                or self.token.tag == Tag.KEYWORD_NOT or self.token.tag == Tag.KEYWORD_TRUE \
                or self.token.tag == Tag.KEYWORD_FALSE or self.token.tag == Tag.VALUE_NUMERICO \
                or self.token.tag == Tag.VALUE_LITERAL:
            self.expressao()
            self.regex_exp_linha()
        else:
            self.skip(
                self.messageFormat.format("), ID, (, nao, verdadeiro, falso, numerico, literal", self.token.lexeme))

            if self.token.tag is not Tag.END_OF_FILE:
                self.regex_exp()

    # RegexExp’ → , Expressao RegexExp’ 46 | ε 47
    def regex_exp_linha(self):
        if self.token.tag == Tag.SYMBOL_CLOSE_PARENTHESIS:
            return
        elif self.token.tag == Tag.SYMBOL_COMMA:
            self.eat(Tag.SYMBOL_COMMA)
            self.expressao()
            self.regex_exp_linha()
        else:
            self.skip(self.messageFormat.format("), ,,", self.token.lexeme))

            if self.token.tag is not Tag.END_OF_FILE:
                self.regex_exp_linha()

    # CmdEscreva → "escreva" "(" Expressao ")" ";" 48
    def cmd_escreva(self):
        if self.token.tag == Tag.KEYWORD_WRITE:
            self.eat(Tag.KEYWORD_WRITE)

            if not self.eat(Tag.SYMBOL_OPEN_PARENTHESIS):
                self.raise_syntax_error(self.messageFormat.format("(", self.token.lexeme))

            self.expressao()

            if not self.eat(Tag.SYMBOL_CLOSE_PARENTHESIS):
                self.raise_syntax_error(self.messageFormat.format(")", self.token.lexeme))

            if not self.eat(Tag.SYMBOL_SEMICOLON):
                self.raise_syntax_error(self.messageFormat.format(";", self.token.lexeme))
        else:
            self.skip(self.messageFormat.format("escreva", self.token.lexeme))

            if self.token.tag is not Tag.END_OF_FILE:
                self.cmd_escreva()

    # CmdLeia → "leia" "(" ID ")" ";" 49
    def cmd_leia(self):
        if self.token.tag == Tag.KEYWORD_READ:
            self.eat(Tag.KEYWORD_READ)

            if not self.eat(Tag.SYMBOL_OPEN_PARENTHESIS):
                self.raise_syntax_error(self.messageFormat.format("(", self.token.lexeme))

            if not self.eat(Tag.ID):
                self.raise_syntax_error(self.messageFormat.format("ID", self.token.lexeme))

            if not self.eat(Tag.SYMBOL_CLOSE_PARENTHESIS):
                self.raise_syntax_error(self.messageFormat.format(")", self.token.lexeme))

            if not self.eat(Tag.SYMBOL_SEMICOLON):
                self.raise_syntax_error(self.messageFormat.format(";", self.token.lexeme))
        else:
            self.skip(self.messageFormat.format("leia", self.token.lexeme))

            if self.token.tag is not Tag.END_OF_FILE:
                self.cmd_leia()

    # Expressao → Exp1 Exp’ 50
    def expressao(self):
        if self.token.tag == Tag.ID or self.token.tag == Tag.SYMBOL_OPEN_PARENTHESIS \
                or self.token.tag == Tag.KEYWORD_NOT or self.token.tag == Tag.KEYWORD_TRUE \
                or self.token.tag == Tag.KEYWORD_FALSE or self.token.tag == Tag.VALUE_NUMERICO \
                or self.token.tag == Tag.VALUE_LITERAL:
            self.exp1()
            self.exp_linha()
        else:
            self.skip(self.messageFormat.format("ID, (, nao, verdadeiro, falso, numerico, literal", self.token.lexeme))

            if self.token.tag is not Tag.END_OF_FILE:
                self.expressao()

    # Exp’ → < Exp1 Exp’ 51 | <= Exp1 Exp’ 52 | > Exp1 Exp’ 53 | >= Exp1 Exp’ 54 | = Exp1 Exp’ 55 | <> Exp1 Exp’ 56 | ε 57
    def exp_linha(self):
        if self.token.tag == Tag.KEYWORD_END or self.token.tag == Tag.SYMBOL_SEMICOLON \
                or self.token.tag == Tag.ID or self.token.tag == Tag.SYMBOL_CLOSE_PARENTHESIS \
                or self.token.tag == Tag.SYMBOL_COMMA or self.token.tag == Tag.KEYWORD_RETURN \
                or self.token.tag == Tag.KEYWORD_IF or self.token.tag == Tag.KEYWORD_WHILE \
                or self.token.tag == Tag.KEYWORD_DO or self.token.tag == Tag.KEYWORD_FOR \
                or self.token.tag == Tag.KEYWORD_UNTIL or self.token.tag == Tag.KEYWORD_REPEAT \
                or self.token.tag == Tag.KEYWORD_WRITE or self.token.tag == Tag.KEYWORD_READ:
            return
        elif self.token.tag == Tag.OPERATOR_LESS_THAN:
            self.eat(Tag.OPERATOR_LESS_THAN)
            self.exp1()
            self.exp_linha()
        elif self.token.tag == Tag.OPERATOR_LESS_THAN_EQUALS:
            self.eat(Tag.OPERATOR_LESS_THAN_EQUALS)
            self.exp1()
            self.exp_linha()
        elif self.token.tag == Tag.OPERATOR_GREATER_THAN:
            self.eat(Tag.OPERATOR_GREATER_THAN)
            self.exp1()
            self.exp_linha()
        elif self.token.tag == Tag.OPERATOR_GREATER_THAN_EQUALS:
            self.eat(Tag.OPERATOR_GREATER_THAN_EQUALS)
            self.exp1()
            self.exp_linha()
        elif self.token.tag == Tag.OPERATOR_EQUALS:
            self.eat(Tag.OPERATOR_EQUALS)
            self.exp1()
            self.exp_linha()
        elif self.token.tag == Tag.OPERATOR_DIFFERENT:
            self.eat(Tag.OPERATOR_DIFFERENT)
            self.exp1()
            self.exp_linha()
        else:
            self.skip(
                self.messageFormat.format(
                    "fim, ;, ID, ), ,, retorne, se, enquanto, faca, para, ate, repita, escreva, leia, <, <=, >, >=, =, <>",
                    self.token.lexeme
                )
            )

            if self.token.tag is not Tag.END_OF_FILE:
                self.exp_linha()

    # Exp 1 → Exp2 Exp1’ 58
    def exp1(self):
        if self.token.tag == Tag.ID or self.token.tag == Tag.SYMBOL_OPEN_PARENTHESIS \
                or self.token.tag == Tag.KEYWORD_NOT or self.token.tag == Tag.KEYWORD_TRUE \
                or self.token.tag == Tag.KEYWORD_FALSE or self.token.tag == Tag.VALUE_NUMERICO \
                or self.token.tag == Tag.VALUE_LITERAL:
            self.exp2()
            self.exp1_linha()
        else:
            self.skip(self.messageFormat.format("ID, (, nao, verdadeiro, falso, numerico, literal", self.token.lexeme))

            if self.token.tag is not Tag.END_OF_FILE:
                self.exp1()

    # Exp1’ → E Exp2 Exp1’ 59 | Ou Exp2 Exp1’ 60| ε 61
    def exp1_linha(self):
        if self.token.tag == Tag.KEYWORD_END or self.token.tag == Tag.SYMBOL_SEMICOLON \
                or self.token.tag == Tag.ID or self.token.tag == Tag.SYMBOL_CLOSE_PARENTHESIS \
                or self.token.tag == Tag.SYMBOL_COMMA or self.token.tag == Tag.KEYWORD_RETURN \
                or self.token.tag == Tag.KEYWORD_IF or self.token.tag == Tag.KEYWORD_WHILE \
                or self.token.tag == Tag.KEYWORD_DO or self.token.tag == Tag.KEYWORD_FOR \
                or self.token.tag == Tag.KEYWORD_UNTIL or self.token.tag == Tag.KEYWORD_REPEAT \
                or self.token.tag == Tag.KEYWORD_WRITE or self.token.tag == Tag.KEYWORD_READ \
                or self.token.tag == Tag.OPERATOR_LESS_THAN or self.token.tag == Tag.OPERATOR_LESS_THAN_EQUALS \
                or self.token.tag == Tag.OPERATOR_GREATER_THAN or self.token.tag == Tag.OPERATOR_GREATER_THAN_EQUALS \
                or self.token.tag == Tag.OPERATOR_EQUALS or self.token.tag == Tag.OPERATOR_DIFFERENT:
            return
        elif self.token.tag == Tag.KEYWORD_AND:
            self.eat(Tag.KEYWORD_AND)
            self.exp2()
            self.exp1_linha()
        elif self.token.tag == Tag.KEYWORD_OR:
            self.eat(Tag.KEYWORD_OR)
            self.exp2()
            self.exp1_linha()
        else:
            self.skip(
                self.messageFormat.format(
                    "fim, ;, ID, ), ,, retorne, se, enquanto, faca, para, ate, repita, escreva, leia, <, <=, >, >=, =, <>, E, Ou",
                    self.token.lexeme
                )
            )

            if self.token.tag is not Tag.END_OF_FILE:
                self.exp1_linha()

    # Exp2 → Exp3 Exp2’ 62
    def exp2(self):
        if self.token.tag == Tag.ID or self.token.tag == Tag.SYMBOL_OPEN_PARENTHESIS \
                or self.token.tag == Tag.KEYWORD_NOT or self.token.tag == Tag.KEYWORD_TRUE \
                or self.token.tag == Tag.KEYWORD_FALSE or self.token.tag == Tag.VALUE_NUMERICO \
                or self.token.tag == Tag.VALUE_LITERAL:
            self.exp3()
            self.exp2_linha()
        else:
            self.skip(self.messageFormat.format("ID, (, Nao, verdadeiro, falso, numerico, literal", self.token.lexeme))

            if self.token.tag is not Tag.END_OF_FILE:
                self.exp2()

    # Exp2’ → + Exp3 Exp2’ 63 | - Exp3 Exp2’ 64 | ε 65
    def exp2_linha(self):
        if self.token.tag == Tag.KEYWORD_END or self.token.tag == Tag.SYMBOL_SEMICOLON \
                or self.token.tag == Tag.ID or self.token.tag == Tag.SYMBOL_CLOSE_PARENTHESIS \
                or self.token.tag == Tag.SYMBOL_COMMA or self.token.tag == Tag.KEYWORD_RETURN \
                or self.token.tag == Tag.KEYWORD_IF or self.token.tag == Tag.KEYWORD_WHILE \
                or self.token.tag == Tag.KEYWORD_DO or self.token.tag == Tag.KEYWORD_FOR \
                or self.token.tag == Tag.KEYWORD_UNTIL or self.token.tag == Tag.KEYWORD_REPEAT \
                or self.token.tag == Tag.KEYWORD_WRITE or self.token.tag == Tag.KEYWORD_READ \
                or self.token.tag == Tag.KEYWORD_AND or self.token.tag == Tag.KEYWORD_OR \
                or self.token.tag == Tag.OPERATOR_LESS_THAN or self.token.tag == Tag.OPERATOR_LESS_THAN_EQUALS \
                or self.token.tag == Tag.OPERATOR_GREATER_THAN or self.token.tag == Tag.OPERATOR_GREATER_THAN_EQUALS \
                or self.token.tag == Tag.OPERATOR_EQUALS or self.token.tag == Tag.OPERATOR_DIFFERENT:
            return
        elif self.token.tag == Tag.OPERATOR_PLUS:
            self.eat(Tag.OPERATOR_PLUS)
            self.exp3()
            self.exp2_linha()
        elif self.token.tag == Tag.OPERATOR_MINUS:
            self.eat(Tag.OPERATOR_MINUS)
            self.exp3()
            self.exp2_linha()
        else:
            self.skip(
                self.messageFormat.format(
                    "fim, ;, ID, ), ,, retorne, se, enquanto, faca, para, ate, repita, escreva, leia, E, Ou, <, <=, >, >=, =, <>, +, -",
                    self.token.lexeme
                )
            )

            if self.token.tag is not Tag.END_OF_FILE:
                self.exp2_linha()

    # Exp3 → Exp4 Exp3’ 66
    def exp3(self):
        if self.token.tag == Tag.ID or self.token.tag == Tag.SYMBOL_OPEN_PARENTHESIS \
                or self.token.tag == Tag.KEYWORD_NOT or self.token.tag == Tag.KEYWORD_TRUE \
                or self.token.tag == Tag.KEYWORD_FALSE or self.token.tag == Tag.VALUE_NUMERICO \
                or self.token.tag == Tag.VALUE_LITERAL:
            self.exp4()
            self.exp3_linha()
        else:
            self.skip(
                self.messageFormat.format("ID, (, Nao, verdadeiro, falso, numerico, literal", self.token.lexeme)
            )

            if self.token.tag is not Tag.END_OF_FILE:
                self.exp3()

    # Exp3’ →* Exp4 Exp3’ 67 | / Exp4 Exp3’ 68 | ε 69
    def exp3_linha(self):
        if self.token.tag == Tag.KEYWORD_END or self.token.tag == Tag.SYMBOL_SEMICOLON \
                or self.token.tag == Tag.ID or self.token.tag == Tag.SYMBOL_CLOSE_PARENTHESIS \
                or self.token.tag == Tag.SYMBOL_COMMA or self.token.tag == Tag.KEYWORD_RETURN \
                or self.token.tag == Tag.KEYWORD_IF or self.token.tag == Tag.KEYWORD_WHILE \
                or self.token.tag == Tag.KEYWORD_DO or self.token.tag == Tag.KEYWORD_FOR \
                or self.token.tag == Tag.KEYWORD_UNTIL or self.token.tag == Tag.KEYWORD_REPEAT \
                or self.token.tag == Tag.KEYWORD_WRITE or self.token.tag == Tag.KEYWORD_READ \
                or self.token.tag == Tag.KEYWORD_AND or self.token.tag == Tag.KEYWORD_OR \
                or self.token.tag == Tag.OPERATOR_LESS_THAN or self.token.tag == Tag.OPERATOR_LESS_THAN_EQUALS \
                or self.token.tag == Tag.OPERATOR_GREATER_THAN or self.token.tag == Tag.OPERATOR_GREATER_THAN_EQUALS \
                or self.token.tag == Tag.OPERATOR_EQUALS or self.token.tag == Tag.OPERATOR_DIFFERENT \
                or self.token.tag == Tag.OPERATOR_PLUS or self.token.tag == Tag.OPERATOR_MINUS:
            return
        elif self.token.tag == Tag.OPERATOR_DIVISION:
            self.eat(Tag.OPERATOR_DIVISION)
            self.exp4()
            self.exp3_linha()
        elif self.token.tag == Tag.OPERATOR_MULTIPLICATION:
            self.eat(Tag.OPERATOR_MULTIPLICATION)
            self.exp4()
            self.exp3_linha()
        else:
            self.skip(
                self.messageFormat.format(
                    "fim, ;, ID, ), ,, retorne, se, enquanto, faca, para, ate, repita, escreva, leia, E, Ou, <, <=, >, >=, =, <>, +, -, /, *",
                    self.token.lexeme
                )
            )

            if self.token.tag is not Tag.END_OF_FILE:
                self.exp3_linha()

    # Exp4 → id Exp4’ 70 | Numerico 71 | Litetal 72 | “verdadeiro” 73 | “falso” 74 | OpUnario Expressao 75| “(“ Expressao “)” 76
    def exp4(self):
        if self.token.tag == Tag.ID:
            self.eat(Tag.ID)
            self.exp4_linha()
        elif self.token.tag == Tag.SYMBOL_OPEN_PARENTHESIS:
            self.eat(Tag.SYMBOL_OPEN_PARENTHESIS)
            self.expressao()

            if not self.eat(Tag.SYMBOL_CLOSE_PARENTHESIS):
                self.raise_syntax_error(self.messageFormat.format(")", self.token.lexeme))
        elif self.token.tag == Tag.KEYWORD_NOT:
            self.op_unario()
            self.expressao()
        elif self.token.tag == Tag.KEYWORD_TRUE:
            self.eat(Tag.KEYWORD_TRUE)
        elif self.token.tag == Tag.KEYWORD_FALSE:
            self.eat(Tag.KEYWORD_FALSE)
        elif self.token.tag == Tag.VALUE_NUMERICO:
            self.eat(Tag.VALUE_NUMERICO)
        elif self.token.tag == Tag.VALUE_LITERAL:
            self.eat(Tag.VALUE_LITERAL)
        else:
            self.skip(
                self.messageFormat.format("(, ID, Nao, verdadeiro, falso, Numerico, Literal", self.token.lexeme)
            )

            if self.token.tag is not Tag.END_OF_FILE:
                self.exp4()

    # Exp4’ → “(“ RegexExp ”)” 77 | ε 78
    def exp4_linha(self):
        if self.token.tag == Tag.KEYWORD_DECLARE or self.token.tag == Tag.SYMBOL_SEMICOLON \
                or self.token.tag == Tag.ID or self.token.tag == Tag.SYMBOL_CLOSE_PARENTHESIS \
                or self.token.tag == Tag.SYMBOL_COMMA or self.token.tag == Tag.KEYWORD_RETURN \
                or self.token.tag == Tag.KEYWORD_IF or self.token.tag == Tag.KEYWORD_WHILE \
                or self.token.tag == Tag.KEYWORD_DO or self.token.tag == Tag.KEYWORD_FOR \
                or self.token.tag == Tag.KEYWORD_UNTIL or self.token.tag == Tag.KEYWORD_REPEAT \
                or self.token.tag == Tag.KEYWORD_WRITE or self.token.tag == Tag.KEYWORD_READ \
                or self.token.tag == Tag.KEYWORD_AND or self.token.tag == Tag.KEYWORD_OR \
                or self.token.tag == Tag.OPERATOR_LESS_THAN or self.token.tag == Tag.OPERATOR_LESS_THAN_EQUALS \
                or self.token.tag == Tag.OPERATOR_GREATER_THAN or self.token.tag == Tag.OPERATOR_GREATER_THAN_EQUALS \
                or self.token.tag == Tag.OPERATOR_EQUALS or self.token.tag == Tag.OPERATOR_DIFFERENT \
                or self.token.tag == Tag.OPERATOR_PLUS or self.token.tag == Tag.OPERATOR_MINUS \
                or self.token.tag == Tag.OPERATOR_DIVISION or self.token.tag == Tag.OPERATOR_MULTIPLICATION:
            return
        elif self.token.tag == Tag.SYMBOL_OPEN_PARENTHESIS:
            self.eat(Tag.SYMBOL_OPEN_PARENTHESIS)
            self.regex_exp()

            if not self.eat(Tag.SYMBOL_CLOSE_PARENTHESIS):
                self.raise_syntax_error(self.messageFormat.format(")", self.token.lexeme))
        else:
            self.skip(
                self.messageFormat.format(
                    "(, declare, ;, ID, ), ,, retorne, se, enquanto, faca, para, ate, repita, escreva, leia, E, Ou, <, <=, >, >=, =, <>, +, -, /, *",
                    self.token.lexeme
                )
            )

            if self.token.tag is not Tag.END_OF_FILE:
                self.exp4_linha()

    # OpUnario → "Nao" 79
    def op_unario(self):
        if self.token.tag == Tag.KEYWORD_NOT:
            self.eat(Tag.KEYWORD_NOT)
        else:
            self.skip(self.messageFormat.format("Nao", self.token.lexeme))

            if self.token.tag is not Tag.END_OF_FILE:
                self.op_unario()