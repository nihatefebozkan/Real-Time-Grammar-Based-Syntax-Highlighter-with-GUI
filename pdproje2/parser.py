class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errors = []

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def advance(self):
        self.pos += 1

    def expect(self, token_type, token_value=None):
        token = self.current_token()
        if token[0] == token_type and (token_value is None or token[1] == token_value):
            self.advance()
            return True
        self.errors.append(f"Expected {token_type} {token_value or ''}, got {token} at position {self.pos}")
        return False

    def parse_program(self):
        if not self.tokens:  # Boş token listesi
            return True, []
        statements = []
        while self.pos < len(self.tokens):
            if self.current_token()[0] is None:
                break
            statement_result = self.parse_statement()
            if statement_result:
                statements.append(statement_result)
            else:
                self.advance()  # Hatalı token'ı atla
        return len(self.errors) == 0, self.errors

    def parse_statement(self):
        token = self.current_token()
        if token[0] == "KEYWORD" and token[1] in ["int", "char"]:
            return self.parse_var_decl()
        elif token[0] == "KEYWORD" and token[1] == "if":
            return self.parse_if_stmt()
        elif token[0] == "KEYWORD" and token[1] == "print":
            return self.parse_print_stmt()
        elif token[0] in ["ID", "INT_VAR", "CHAR_VAR"]:  # Atama ifadeleri için
            return self.parse_assign_stmt()
        else:
            self.errors.append(f"Invalid statement start: {token} at position {self.pos}")
            return False

    def parse_var_decl(self):
        token = self.current_token()
        if token[0] == "KEYWORD" and token[1] in ["int", "char"]:
            self.advance()
            token = self.current_token()
            if token[0] in ["ID", "INT_VAR", "CHAR_VAR"]:
                self.advance()
                return True
            self.errors.append(f"Expected ID, INT_VAR, or CHAR_VAR after variable declaration, got {token} at position {self.pos}")
            return False
        return False

    def parse_if_stmt(self):
        if not self.expect("KEYWORD", "if"):
            return False
        if not self.expect("SYMBOL", "("):
            return False
        if not self.parse_expr():
            return False
        if not self.expect("SYMBOL", ")"):
            return False
        if not self.expect("SYMBOL", ":"):
            return False
        if not self.parse_statement():
            return False
        token = self.current_token()
        if token[0] == "KEYWORD" and token[1] == "else":
            self.advance()
            if not self.expect("SYMBOL", ":"):
                return False
            if not self.parse_statement():
                return False
        return True

    def parse_print_stmt(self):
        if not self.expect("KEYWORD", "print"):
            return False
        if not self.expect("SYMBOL", "("):
            return False
        if not self.parse_expr():
            return False
        if not self.expect("SYMBOL", ")"):
            return False
        return True

    def parse_assign_stmt(self):
        token = self.current_token()
        if token[0] not in ["ID", "INT_VAR", "CHAR_VAR"]:
            self.errors.append(f"Expected ID, INT_VAR, or CHAR_VAR for assignment, got {token} at position {self.pos}")
            return False
        self.advance()
        if not self.expect("OPERATOR", "="):
            return False
        if not self.parse_expr():
            return False
        return True

    def parse_expr(self):
        if not self.parse_term():
            return False
        while self.current_token()[0] == "OPERATOR" and self.current_token()[1] in ["+", "-", "==", "!=", ">", "<"]:
            self.advance()
            if not self.parse_term():
                return False
        return True

    def parse_term(self):
        if not self.parse_factor():
            return False
        while self.current_token()[0] == "OPERATOR" and self.current_token()[1] in ["*", "/"]:
            self.advance()
            if not self.parse_factor():
                return False
        return True

    def parse_factor(self):
        token = self.current_token()
        if token[0] in ["NUMBER", "ID", "CHAR_VAR", "INT_VAR", "CHAR_LITERAL"]:
            self.advance()
            return True
        elif token[0] == "SYMBOL" and token[1] == "(":
            self.advance()
            if not self.parse_expr():
                return False
            if not self.expect("SYMBOL", ")"):
                return False
            return True
        self.errors.append(f"Invalid factor: {token} at position {self.pos}")
        return False