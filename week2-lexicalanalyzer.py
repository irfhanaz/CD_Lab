#lexical analyzer for C programs
import re
import pprint
file_name = input("Enter file name:")
with open(file_name, "r") as fp: 
    lines = fp.readlines()
lexical_tokens = {}
count = 1
for line in lines:
    code = line.split()
    tokens = []
    for word in code:
        if word in ["if", "else", "else if", "for", "while", "continue", "break", "do", "try", "catch", "throw", "return", "printf"]:
            tokens.append(['KEYWORD', word])
        elif re.match(".*?\(\)$", word):
            tokens.append(['FUNCTION', word])
        elif re.match("(<)([a-z])*.h(>)", word) or re.match("\"([a-z])*.h\"", word):
            tokens.append(['HEADER FILE', word])
        elif re.match("#[a-z]", word):
            tokens.append(['PREPROCESSING DIRECTIVE', word])
        elif word in ['char', 'int', 'boolean']:
            tokens.append(['DATATYPE', word])
        elif word in '*-/+%=':
            tokens.append(['ARITHMETIC OPERATOR', word])
        elif word in ['==', '!=', '<=', ">=", "<", ">"]:
            tokens.append(['RELATIONAL OPERATOR', word])
        elif word in ["&&", "|", "!"]:
            tokens.append(['LOGICAL OPERATOR', word])
        elif re.match(".[0-9]", word):
            if word[len(word) - 1] == ';': 
                tokens.append(["INTEGER", word[:-1]])
                tokens.append(['END_STATEMENT', ';'])
            else: 
                tokens.append(["INTEGER", word])
        elif re.match("([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*", word):
            tokens.append(['IDENTIFIER', word])
        elif word == "{":
            tokens.append(["START BLOCK", word])
        elif word == '}':
            tokens.append(["END BLOCK", word])
    lexical_tokens[count] = tokens
    count += 1
pprint.pprint(lexical_tokens)
        


