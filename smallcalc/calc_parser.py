from .calc_lexer import TokenError, CalcLexer, INTEGER, FLOAT, LITERAL, NAME
from .tok import Token

class CalcParser:
    """
    integer: [0-9]+
    addsymbol: '+' | '-'
    mulsymbol: '*' | '/'
    expression: term [ addsymbol expression ]
    term: factor [ mulsymbol term ]
    factor: [ addsymbol ] ( integer | variable | '(' expression ')' )
    """

    def __init__(self):
        self.lexer = CalcLexer()

    def _expect(self, token, types, values=None):
        if token.type not in types:
            raise TokenError('Expected token of type {}, found {}'.format(types, token))
        if values and token.value not in values:
            raise TokenError('Expected {}, found {}'.format(values, token))

    def parse_number(self):
        token = self.lexer.get_token()
        self._expect(token, [INTEGER, FLOAT])
        if token.type == INTEGER:
            return IntegerNode(token.value)
        return FloatNode(token.value)

    def _parse_literal(self, *values):
        token = self.lexer.get_token()
        self._expect(token, [LITERAL], values)
        return LiteralNode(token.value)

    def _parse_variable(self):
        token = self.lexer.get_token()
        self._expect(token, [NAME])
        return VariableNode(token.value)

    def parse_expression(self):
        left = self.parse_term()
        while self.lexer.peek_token() in (Token(LITERAL, '+'), Token(LITERAL, '-')):
            operator = self._parse_literal()
            right = self.parse_term()
            left = BinaryNode(left, right, operator)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.lexer.peek_token() in (Token(LITERAL, '*'), Token(LITERAL, '/')):
            operator = self._parse_literal()
            right = self.parse_factor()
            left = BinaryNode(left, right, operator)
        return left

    def parse_factor(self):
        left = self._parse_unary()
        with self.lexer:
            operator = self._parse_literal('^')
            right = self._parse_unary()
            return ExponentiationNode(left, right, operator)
        return left

    def parse_exponentiation(self):
        return self.parse_factor()

    def _parse_unary(self):
        with self.lexer:
            operator = self._parse_literal('+', '-')
            content = self._parse_unary()
            return UnaryNode(operator, content)
        with self.lexer:
            self._parse_literal('(')
            expression = self.parse_expression()
            self._parse_literal(')')
            return expression
        with self.lexer:
            return self._parse_variable()
        return self.parse_number()

    def parse_assignment(self):
        variable = self._parse_variable()
        self.lexer.discard(Token(LITERAL, '='))
        value = self.parse_expression()
        return AssignmentNode(variable.value, value)

    def parse_line(self):
        with self.lexer:
            return self.parse_assignment()
        return self.parse_expression()

class Node:
    def __init__(self, type):
        self.type = type

    def asdict(self):
        dict = vars(self)
        for (key, value) in dict.items():
            if isinstance(value, Node):
                dict[key] = value.asdict()
        return dict

class ValueNode(Node):
    def __init__(self, type, value):
        super().__init__(type)
        self.value = value

class NumberNode(ValueNode):
    def __init__(self, type, value):
        super().__init__(type, value)

class IntegerNode(NumberNode):
    def __init__(self, value):
        super().__init__('integer', int(value))

class FloatNode(NumberNode):
    def __init__(self, value):
        super().__init__('float', float(value))

class LiteralNode(ValueNode):
    def __init__(self, value):
        super().__init__('literal', value)

class VariableNode(ValueNode):
    def __init__(self, value):
        super().__init__('variable', value)

class OperationNode(Node):
    def __init__(self, type, operator):
        super().__init__(type)
        self.operator = operator

class UnaryNode(OperationNode):
    def __init__(self, operator, content):
        super().__init__('unary', operator)
        self.content = content

class BinaryNode(OperationNode):
    def __init__(self, left, right, operator):
        super().__init__('binary', operator)
        self.left = left
        self.right = right

class ExponentiationNode(OperationNode):
    def __init__(self, left, right, operator):
        super().__init__('exponentiation', operator)
        self.left = left
        self.right = right

class AssignmentNode(Node):
    def __init__(self, variable, value):
        super().__init__('assignment')
        self.variable = variable
        self.value = value
