# Nodos del AST del lenguaje basado en reglas


class Program:
    def __init__(self, rules):
        self.rules = rules


class Rule:
    def __init__(self, name, condition, action):
        self.name = name
        self.condition = condition
        self.action = action


class And:
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Comparison:
    def __init__(self, identifier, operator, value):
        self.identifier = identifier
        self.operator = operator
        self.value = value


class Fact:
    def __init__(self, identifier):
        self.identifier = identifier


class Action:
    def __init__(self, identifier):
        self.identifier = identifier
