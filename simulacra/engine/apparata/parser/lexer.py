"""Lexer module."""

from __future__ import annotations

from engine.apparata.parser.token import Token, TokenType


class Lexer:
    """Lexer for the parser module."""

    def __init__(self, input_stream: str) -> None:
        """Constructor.

        Args:
            input_stream (str): String input to be lexified.
        """
        self.input_stream = input_stream
        self.pos: int = 0
        self.line_num: int = 1
        self.char_num: int = 1

        if len(input_stream) != 0:
            self.char = self.input_stream[self.pos]
        else:
            self.char = TokenType.EOF

    def next_token(self) -> Token:
        """Return the next token from the input stream, ignoring whitespace."""
        while self.char != TokenType.EOF:

            if self.char in [' ', '\t', '\n', '\r']:
                self.consume()

            elif self.char in ['\'', '\"']:
                self.consume()
                return Token(TokenType.QUOTE, '"')

            elif self.char == ';':
                self.consume()
                return Token(TokenType.SEMICOLON, ';')

            elif self.char == ',':
                self.consume()
                return Token(TokenType.COMMA, ',')

            elif self.char == '{':
                self.consume()
                return Token(TokenType.LBRACE, '{')

            elif self.char == '}':
                self.consume()
                return Token(TokenType.RBRACE, '}')

            elif self.char == '(':
                self.consume()
                return Token(TokenType.LPAREN, '(')

            elif self.char == ')':
                self.consume()
                return Token(TokenType.RPAREN, ')')

            elif self.char == '-':
                self.consume()
                if self.char == '>':
                    self.consume()
                    return Token(TokenType.ARROW, '->')
                else:
                    self.error()

            elif self.char == '=':
                self.consume()
                return Token(TokenType.EQUALS, '=')

            elif self.char == '#':
                lexeme = ""
                while self.char != TokenType.EOF and self.char != '\n':
                    self.consume()

            elif self.char.isdigit():
                lexeme = ""
                while self.char != TokenType.EOF and self.char.isdigit():
                    lexeme += self.char
                    self.consume()
                return Token(TokenType.NUMBER, lexeme)

            elif self.char.isalpha():
                lexeme = ""
                while (self.char != TokenType.EOF and
                       (self.char.isalpha() or
                        self.char.isdigit() or
                        self.char == '_')):
                    lexeme += self.char
                    self.consume()
                return Token(TokenType.ID, lexeme)
            else:
                self.error()

        return Token(TokenType.EOF, "<EOF>")

    def consume(self) -> None:
        """Advance to the next character in the input stream, or EOF."""
        if self.char in ['\n', '\r']:
            self.line_num += 1
            self.char_num += 1
        else:
            self.char_num += 1

        self.pos += 1
        if self.pos >= len(self.input_stream):
            self.char = TokenType.EOF
        else:
            self.char = self.input_stream[self.pos]

    def error(self) -> None:
        raise SyntaxError(f"Invalid character {self.char} at "
                          f"[{self.line_num}:{self.char_num}]")
