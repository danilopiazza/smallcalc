class CalcVisitor:
    def __init__(self):
        self.environment = {}

    def visit(self, ast):
        if ast['type'] in ('integer', 'float'):
            return (ast['value'], ast['type'])
        if ast['type'] == 'unary':
            operator = ast['operator']['value']
            content, type = self.visit(ast['content'])
            if operator == '+':
                return (content, type)
            if operator == '-':
                return (-content, type)
        if ast['type'] in ('binary', 'exponentiation'):
            left, left_type = self.visit(ast['left'])
            right, right_type = self.visit(ast['right'])
            result_type = self._promote_number(left_type, right_type)
            operator = ast['operator']['value']
            if operator == '+':
                return (left + right, result_type)
            if operator == '-':
                return (left - right, result_type)
            if operator == '*':
                return (left * right, result_type)
            if operator == '/':
                return (left // right, result_type)
            if operator == '^':
                return (left ** right, result_type)
        if ast['type'] == 'assignment':
            variable = ast['variable']
            value = ast['value']
            self.environment[variable] = value
        if ast['type'] == 'variable':
            variable = ast['value']
            return (self.valueof(variable), self.typeof(variable))
        return (None, None)

    def _promote_number(self, left_type, right_type):
        return 'float' if 'float' in (left_type, right_type) else 'integer'

    def isvariable(self, variable):
        return variable in self.environment

    def typeof(self, variable):
        return self.environment[variable]['type']

    def valueof(self, variable):
        return self.environment[variable]['value']
