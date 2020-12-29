from __future__ import annotations

from graph_engine.graph_token import Token, TokenTypes


class Lexer:

    def __init__(self, input: str) -> None:
        self.input = input
        self.p = 0
        self.line_num = 1
        self.char_num = 1
        if len(input) != 0:
            self.c = self.input[self.p]
        else:
            self.c = TokenTypes.EOF

    def next_token(self):
        """Return the next Token in the input stream, ignoring whitespace."""
        while self.c != TokenTypes.EOF:
            if self.c in [' ', '\t', '\n', '\r']:
                self._consume()

            elif self.c == ';':
                self._consume()
                return Token(TokenTypes.SEMICOLON, ';')

            elif self.c == ',':
                self._consume()
                return Token(TokenTypes.COMMA, ',')

            elif self.c == '{':
                self._consume()
                return Token(TokenTypes.LBRACE, '{')

            elif self.c == '}':
                self._consume()
                return Token(TokenTypes.RBRACE, '}')

            elif self.c == '-':
                # '->' is an ARROW, '-' followed by anything else is invalid.
                self._consume()
                if self.c == '>':
                    self._consume()
                    return Token(TokenTypes.ARROW, '->')
                else:
                    self._error()

            elif self.c == '=':
                # '==>' is a DOUBLEARROW, '==' followed by anything else is
                # invalid. '=' followed by anything but a '=' is simply an
                #  EQUALS.
                self._consume()
                if self.c == '=':
                    self._consume()
                    if self.c == '>':
                        self._consume()
                        return Token(TokenTypes.DOUBLEARROW, '==>')
                    else:
                        self._error()
                else:
                    return Token(TokenTypes.EQUALS, '=')

            elif self.c == '#':
                # Consume everything until the end-of-line.
                lexeme = ""
                while self.c != TokenTypes.EOF and self.c != '\n':
                    self._consume()

            elif self.c.isdigit():
                lexeme = ""
                while self.c != TokenTypes.EOF and self.c.isdigit():
                    lexeme += self.c
                    self._consume()
                return Token(TokenTypes.NUMBER, lexeme)

            elif self.c.isalpha():
                lexeme = ""
                while self.c != TokenTypes.EOF and (self.c.isalpha() or
                                                    self.c.isdigit() or
                                                    self.c == '_'):
                    lexeme += self.c
                    self._consume()
                if lexeme == 'configuration':
                    t = Token(TokenTypes.CONFIGURATION, lexeme)
                elif lexeme == 'productions':
                    t = Token(TokenTypes.PRODUCTIONS, lexeme)
                else:
                    t = Token(TokenTypes.ID, lexeme)
                return t

            else:
                # Any other character not in the above definitions is invalid.
                self._error()
        return Token(TokenTypes.EOF, "<EOF>")

    def _consume(self):
        """Advance to the next character of input, or EOF."""
        if self.c in ['\n', '\r']:
            self.line_num += 1
            self.char_num += 1
        else:
            self.char_num += 1

        self.p += 1
        if self.p >= len(self.input):
            self.c = TokenTypes.EOF
        else:
            self.c = self.input[self.p]

    def _error(self):
        raise SyntaxError(f"Invalid characte {self.c} at [{self.line_num}:{self.char_num}]")
