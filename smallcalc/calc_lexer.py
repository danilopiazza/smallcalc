import itertools

from . import text_buffer
from . import tok as token

EOF = 'EOF'
EOL = 'EOL'
INTEGER = 'INTEGER'
FLOAT = 'FLOAT'
LITERAL = 'LITERAL'
NAME = 'NAME'

class TokenError(ValueError):
    pass

class CalcLexer:
    def __init__(self):
        self.buffer = text_buffer.TextBuffer()
        self.positions = []

    def load(self, text):
        self.buffer.load(text)

    def _is_identifier(self, char):
        return char.isalpha() or char == '_'

    def _is_number(self, char):
        return char.isdigit() or char == '.'

    def get_token(self):

        try:
            current_char = self.buffer.current_char
            while current_char.isspace():
                self.buffer.skip()
                current_char = self.buffer.current_char
            if self._is_number(current_char):
                number = ''.join(itertools.takewhile(self._is_number, self.buffer.tail))
                self.buffer.skip(len(number))
                decimal_point_count = number.count('.')
                if decimal_point_count == 0:
                    return token.Token(INTEGER, number)
                elif decimal_point_count == 1:
                    return token.Token(FLOAT, number)
                #raise TokenError('Invalid number {}', number)
            if self._is_identifier(current_char):
                name = ''.join(itertools.takewhile(self._is_identifier, self.buffer.tail))
                self.buffer.skip(len(name))
                return token.Token(NAME, name)
            else:
                self.buffer.skip()
                return token.Token(LITERAL, current_char)
        except text_buffer.EOLError:
            self.buffer.newline()
            return token.Token(EOL)
        except text_buffer.EOFError:
            return token.Token(EOF)

    def get_tokens(self):
        tokens = []
        while token.Token(EOF) not in tokens:
            tokens.append(self.get_token())
        return tokens

    def stash(self):
        self.positions.append(self.buffer.position)

    def pop(self):
        self.buffer.goto(*self.positions.pop())

    def peek_token(self):
        self.stash()
        token = self.get_token()
        self.pop()
        return token

    def discard(self, token):
        next_token = self.get_token()
        if next_token != token:
            raise TokenError('Expected token {}, found {}'.format(token, next_token))

    def discard_type(self, type):
        next_token = self.get_token()
        if next_token.type != type:
            raise TokenError('Expected token of type {}, found {}'.format(type, next_token))

    def __enter__(self):
        self.stash()

    def __exit__(self, type, value, traceback):
        if type == TokenError:
            self.pop()
        return True
