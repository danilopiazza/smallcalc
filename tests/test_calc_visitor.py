from smallcalc import calc_visitor as cvis


def test_visitor_integer():
    ast = {
        'type': 'integer',
        'value': 12
    }

    v = cvis.CalcVisitor()
    assert v.visit(ast) == (12, 'integer')

def test_visitor_float():
    ast = {
        'type': 'float',
        'value': 12.345
    }

    v = cvis.CalcVisitor()
    assert v.visit(ast) == (12.345, 'float')

def test_visitor_expression_sum():
    ast = {
        'type': 'binary',
        'left': {
            'type': 'integer',
            'value': 5
        },
        'right': {
            'type': 'integer',
            'value': 4
        },
        'operator': {
            'type': 'literal',
            'value': '+'
        }
    }

    v = cvis.CalcVisitor()
    assert v.visit(ast) == (9, 'integer')

def test_visitor_expression_subtraction():
    ast = {
        'type': 'binary',
        'left': {
            'type': 'integer',
            'value': 5
        },
        'right': {
            'type': 'integer',
            'value': 4
        },
        'operator': {
            'type': 'literal',
            'value': '-'
        }
    }

    v = cvis.CalcVisitor()
    assert v.visit(ast) == (1, 'integer')

def test_visitor_expression_with_multiple_operations():
    ast = {
        'type': 'binary',
        'left': {
            'type': 'binary',
            'left': {
                'type': 'integer',
                'value': 3
            },
            'right': {
                'type': 'integer',
                'value': 4
            },
            'operator': {
                'type': 'literal',
                'value': '-'
            }
        },
        'right': {
            'type': 'integer',
            'value': 200
        },
        'operator': {
            'type': 'literal',
            'value': '+'
        }
    }

    v = cvis.CalcVisitor()
    assert v.visit(ast) == (199, 'integer')

def test_visitor_term_multiplication():
    ast = {
        'type': 'binary',
        'left': {
            'type': 'integer',
            'value': 5
        },
        'right': {
            'type': 'integer',
            'value': 4
        },
        'operator': {
            'type': 'literal',
            'value': '*'
        }
    }

    v = cvis.CalcVisitor()
    assert v.visit(ast) == (20, 'integer')

def test_visitor_term_division():
    ast = {
        'type': 'binary',
        'left': {
            'type': 'integer',
            'value': 11
        },
        'right': {
            'type': 'integer',
            'value': 4
        },
        'operator': {
            'type': 'literal',
            'value': '/'
        }
    }

    v = cvis.CalcVisitor()
    assert v.visit(ast) == (2, 'integer')

def test_visitor_unary_minus():
    ast = {
        'type': 'unary',
        'operator': {
            'type': 'literal',
            'value': '-'
        },
        'content': {
            'type': 'binary',
            'left': {
                'type': 'integer',
                'value': 2
            },
            'right': {
                'type': 'integer',
                'value': 3
            },
            'operator': {
                'type': 'literal',
                'value': '+'
            }
        },
    }

    v = cvis.CalcVisitor()
    assert v.visit(ast) == (-5, 'integer')

def test_visitor_unary_plus():
    ast = {
        'type': 'unary',
        'operator': {
            'type': 'literal',
            'value': '+'
        },
        'content': {
            'type': 'binary',
            'left': {
                'type': 'integer',
                'value': 2
            },
            'right': {
                'type': 'integer',
                'value': 3
            },
            'operator': {
                'type': 'literal',
                'value': '+'
            }
        },
    }

    v = cvis.CalcVisitor()
    assert v.visit(ast) == (5, 'integer')

def test_visitor_assignment():
    ast = {
        'type': 'assignment',
        'variable': 'x',
        'value': {
            'type': 'integer',
            'value': 5
        }
    }

    v = cvis.CalcVisitor()
    assert v.visit(ast) == (None, None)
    assert v.isvariable('x') is True
    assert v.valueof('x') == 5
    assert v.typeof('x') == 'integer'

def test_visitor_variable():
    assignemnt_ast = {
        'type': 'assignment',
        'variable': 'x',
        'value': {
            'type': 'integer',
            'value': 123
        }
    }

    read_ast = {
        'type': 'variable',
        'value': 'x'
    }

    v = cvis.CalcVisitor()
    v.visit(assignemnt_ast)
    assert v.visit(read_ast) == (123, 'integer')

def test_visitor_exponentiation():
    ast = {
        'type': 'exponentiation',
        'left': {
            'type': 'integer',
            'value': 2
        },
        'right': {
            'type': 'integer',
            'value': 3
        },
        'operator': {
            'type': 'literal',
            'value': '^'
        }
    }

    v = cvis.CalcVisitor()
    assert v.visit(ast) == (8, 'integer')

def test_visitor_expression_sum_with_float():
    ast = {
        'type': 'binary',
        'left': {
            'type': 'float',
            'value': 5.1
        },
        'right': {
            'type': 'integer',
            'value': 4
        },
        'operator': {
            'type': 'literal',
            'value': '+'
        }
    }

    v = cvis.CalcVisitor()
    assert v.visit(ast) == (9.1, 'float')
