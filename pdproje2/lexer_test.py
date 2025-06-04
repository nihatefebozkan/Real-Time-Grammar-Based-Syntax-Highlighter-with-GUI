import lexer

def test_tokenize_simple_var():
    code = "int x"
    tokens = lexer.tokenize(code)
    assert tokens == [("KEYWORD", "int"), ("INT_VAR", "x")], f"Expected [('KEYWORD', 'int'), ('INT_VAR', 'x')], got {tokens}"

def test_tokenize_assignment():
    code = "int x\nx = 5"
    tokens = lexer.tokenize(code)
    assert tokens == [("KEYWORD", "int"), ("INT_VAR", "x"), ("INT_VAR", "x"), ("OPERATOR", "="), ("NUMBER", "5")], f"Expected [('KEYWORD', 'int'), ('INT_VAR', 'x'), ('INT_VAR', 'x'), ('OPERATOR', '='), ('NUMBER', '5')], got {tokens}"

def test_tokenize_if_else():
    code = "if (x + 1):\nelse:"
    tokens = lexer.tokenize(code)
    assert tokens == [("KEYWORD", "if"), ("SYMBOL", "("), ("INT_VAR", "x"), ("OPERATOR", "+"), ("NUMBER", "1"), ("SYMBOL", ")"), ("SYMBOL", ":"), ("KEYWORD", "else"), ("SYMBOL", ":")], f"Expected [('KEYWORD', 'if'), ('SYMBOL', '('), ('INT_VAR', 'x'), ('OPERATOR', '+'), ('NUMBER', '1'), ('SYMBOL', ')'), ('SYMBOL', ':'), ('KEYWORD', 'else'), ('SYMBOL', ':')], got {tokens}"

def test_tokenize_comment():
    code = "int x  # comment"
    tokens = lexer.tokenize(code)
    assert tokens == [("KEYWORD", "int"), ("INT_VAR", "x"), ("COMMENT", "# comment")], f"Expected [('KEYWORD', 'int'), ('INT_VAR', 'x'), ('COMMENT', '# comment')], got {tokens}"

def test_tokenize_char_literal():
    code = "char c\nc = 'a'"
    tokens = lexer.tokenize(code)
    assert tokens == [("KEYWORD", "char"), ("CHAR_VAR", "c"), ("CHAR_VAR", "c"), ("OPERATOR", "="), ("CHAR_LITERAL", "'a'")], f"Expected [('KEYWORD', 'char'), ('CHAR_VAR', 'c'), ('CHAR_VAR', 'c'), ('OPERATOR', '='), ('CHAR_LITERAL', "'a'")], got {tokens}"

def test_tokenize_empty():
    code = ""
    tokens = lexer.tokenize(code)
    assert tokens == [], f"Expected [], got {tokens}"

if __name__ == "__main__":
    test_tokenize_simple_var()
    test_tokenize_assignment()
    test_tokenize_if_else()
    test_tokenize_comment()
    test_tokenize_char_literal()
    test_tokenize_empty()
    print("All lexer tests passed!")