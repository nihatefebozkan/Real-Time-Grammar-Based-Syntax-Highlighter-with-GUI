def is_number(s):
    return s.isdigit()

def classify(word, prev_keyword=None, typed_ids=None):
    keywords = ["if", "print", "else", "elif", "int", "char"]
    if not word:
        return None
    if word in keywords:
        return ("KEYWORD", word)
    elif is_number(word):
        return ("NUMBER", word)
    elif prev_keyword == "int":
        typed_ids[word] = "INT_VAR"
        return ("INT_VAR", word)
    elif prev_keyword == "char":
        typed_ids[word] = "CHAR_VAR"
        return ("CHAR_VAR", word)
    else:
        return (typed_ids.get(word, "ID"), word)

def tokenize(code):
    tokens = []
    i = 0
    word = ''
    prev_token = None
    typed_ids = {}
    operators = ['+', '-', '*', '/', '=', '>', '<', '==', '!=']
    symbols = ['(', ')', ':']
    
    if not code.strip():  # Boş input kontrolü
        return tokens

    while i < len(code):
        char = code[i]
        two_char = code[i:i+2]

        # CHAR LITERAL: 'a'
        if char == "'" and i + 2 < len(code) and code[i+2] == "'":
            tokens.append(("CHAR_LITERAL", code[i:i+3]))
            i += 3
            continue

        if two_char in operators:
            if word:
                token = classify(word, prev_token, typed_ids)
                if token:
                    tokens.append(token)
                    prev_token = word
                word = ''
            tokens.append(("OPERATOR", two_char))
            i += 2
        elif char in operators:
            if word:
                token = classify(word, prev_token, typed_ids)
                if token:
                    tokens.append(token)
                    prev_token = word
                word = ''
            tokens.append(("OPERATOR", char))
            i += 1
        elif char in symbols:
            if word:
                token = classify(word, prev_token, typed_ids)
                if token:
                    tokens.append(token)
                    prev_token = word
                word = ''
            tokens.append(("SYMBOL", char))
            i += 1
        elif char == '#':
            if word:
                token = classify(word, prev_token, typed_ids)
                if token:
                    tokens.append(token)
                word = ''
            start = i
            newline_index = code.find('\n', i)
            if newline_index == -1:
                comment_text = code[start:].rstrip('\n')
                i = len(code)
            else:
                comment_text = code[start:newline_index]
                i = newline_index
            tokens.append(("COMMENT", comment_text))
        elif char in [' ', '\n', '\t']:
            if word:
                token = classify(word, prev_token, typed_ids)
                if token:
                    tokens.append(token)
                    prev_token = word
                word = ''
            i += 1
        else:
            word += char
            i += 1

    if word:
        token = classify(word, prev_token, typed_ids)
        if token:
            tokens.append(token)
    return tokens