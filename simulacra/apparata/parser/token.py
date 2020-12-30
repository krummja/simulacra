"""Token module."""

from __future__ import annotations
from enum import Enum


class TokenType(Enum):
    """Enum representing all token types."""
    EOF = 0
    SEMICOLON = 1
    EQUALS = 2
    LBRACE = 3
    RBRACE = 4
    ARROW = 5
    LPAREN = 6
    RPAREN = 7
    QUOTE = 8
    COMMA = 9
    PROPERTY = 10
    NUMBER = 11
    ID = 12


class Token:
    """Token abstraction."""

    def __init__(self, token_type: int, text: str) -> None:
        """Constructor.

        Args:
            token_type (TokenType): A numeric token type representation.
            text (str): A lexeme
        """
        self.token_type = token_type
        self.text = text

    def __str__(self) -> str:
        return f"{self.text}, {TokenType(self.token_type).name}"
