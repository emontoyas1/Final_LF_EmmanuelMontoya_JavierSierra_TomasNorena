# Analizador lexico: convierte el texto de las reglas en una lista de tokens

# Tipos de token
RULE = "RULE"
IF = "IF"
THEN = "THEN"
AND = "AND"
COLON = "COLON"
GT = "GT"
LT = "LT"
EQ = "EQ"
ID = "ID"
VALUE = "VALUE"

KEYWORDS = {
    "rule": RULE,
    "if": IF,
    "then": THEN,
    "AND": AND,
}


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return "Token(" + self.type + ", " + str(self.value) + ")"


def tokenize(text):
    tokens = []
    i = 0
    n = len(text)

    while i < n:
        c = text[i]

        if c == " " or c == "\t" or c == "\n" or c == "\r":
            i += 1
            continue

        if c == ":":
            tokens.append(Token(COLON, ":"))
            i += 1
        elif c == ">":
            tokens.append(Token(GT, ">"))
            i += 1
        elif c == "<":
            tokens.append(Token(LT, "<"))
            i += 1
        elif c == "=":
            tokens.append(Token(EQ, "="))
            i += 1
        elif c.isdigit():
            num = ""
            while i < n and text[i].isdigit():
                num += text[i]
                i += 1
            tokens.append(Token(VALUE, int(num)))
        elif c.islower():
            word = ""
            while i < n and (text[i].islower() or text[i].isdigit() or text[i] == "_"):
                word += text[i]
                i += 1
            if word in KEYWORDS:
                tokens.append(Token(KEYWORDS[word], word))
            else:
                tokens.append(Token(ID, word))
        elif c.isupper():
            # el unico token en mayuscula permitido es AND
            word = ""
            while i < n and text[i].isupper():
                word += text[i]
                i += 1
            if word == "AND":
                tokens.append(Token(AND, word))
            else:
                raise Exception("Error lexico: token invalido '" + word + "'")
        else:
            raise Exception("Error lexico: caracter invalido '" + c + "'")

    return tokens
