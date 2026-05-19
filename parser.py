# Analizador sintactico LL(1) por descenso recursivo
# Construye el AST a partir de la lista de tokens producida por el lexer

import lexer
from ast_nodes import Program, Rule, And, Comparison, Fact, Action


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def expect(self, type):
        token = self.peek()
        if token is None or token.type != type:
            raise Exception("Error sintactico: se esperaba " + type)
        return self.advance()

    # Program -> RuleList
    def parse_program(self):
        rules = []
        while self.peek() is not None:
            rules.append(self.parse_rule())
        return Program(rules)

    # Rule -> rule id : if Cond then Action
    def parse_rule(self):
        self.expect(lexer.RULE)
        name = self.expect(lexer.ID).value
        self.expect(lexer.COLON)
        self.expect(lexer.IF)
        condition = self.parse_cond()
        self.expect(lexer.THEN)
        action = self.parse_action()
        return Rule(name, condition, action)

    # Cond -> Atom (AND Atom)*
    def parse_cond(self):
        cond = self.parse_atom()
        while self.peek() is not None and self.peek().type == lexer.AND:
            self.advance()
            right = self.parse_atom()
            cond = And(cond, right)
        return cond

    # Atom -> id RelOp value | id
    def parse_atom(self):
        identifier = self.expect(lexer.ID).value
        token = self.peek()
        if token is not None and token.type in (lexer.GT, lexer.LT, lexer.EQ):
            op = self.advance().value
            value = self.expect(lexer.VALUE).value
            return Comparison(identifier, op, value)
        else:
            return Fact(identifier)

    # Action -> id
    def parse_action(self):
        identifier = self.expect(lexer.ID).value
        return Action(identifier)


def parse(tokens):
    parser = Parser(tokens)
    return parser.parse_program()
