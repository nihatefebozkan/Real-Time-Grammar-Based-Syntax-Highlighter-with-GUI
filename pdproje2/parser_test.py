import lexer
from parser import Parser

def test_parse_var_decl():
    tokens = lexer.tokenize("int x")
    parser = Parser(tokens)
    valid, errors = parser.parse_program()
    assert valid, f"Expected valid syntax, got errors: {errors}"

def test_parse_assignment():
    tokens = lexer.tokenize("int x\nx = 5")
    parser = Parser(tokens)
    valid, errors = parser.parse_program()
    assert valid, f"Expected valid syntax, got errors: {errors}"

def test_parse_if_else():
    tokens = lexer.tokenize("if (x == 5):\n    print('a')\nelse:\n    print(2)")
    parser = Parser(tokens)
    valid, errors = parser.parse_program()
    assert valid, f"Expected valid syntax, got errors: {errors}"

def test_parse_invalid_else():
    tokens = lexer.tokenize("else: print(5)")
    parser = Parser(tokens)
    valid, errors = parser.parse_program()
    assert not valid, f"Expected invalid syntax, got valid: {errors}"
    assert any("Invalid statement start" in error for error in errors), f"Expected 'Invalid statement start' error, got {errors}"

def test_parse_empty():
    tokens = lexer.tokenize("")
    parser = Parser(tokens)
    valid, errors = parser.parse_program()
    assert valid, f"Expected valid syntax for empty input, got errors: {errors}"

if __name__ == "__main__":
    test_parse_var_decl()
    test_parse_assignment()
    test_parse_if_else()
    test_parse_invalid_else()
    test_parse_empty()
    print("All parser tests passed!")