from __future__ import annotations

from enum import Enum


class TokenTypes(Enum):
    """An Enum to represent all token types."""
    
    EOF = 0
    SEMICOLON = 1
    EQUALS = 2
    CONFIGURATION = 3
    PRODUCTIONS = 4
    LBRACE = 5
    RBRACE = 6
    DOUBLEARROW = 7
    ARROW = 8
    ID = 9
    NUMBER = 10
    COMMA = 11
    

class Token:
    
    def __init__(self, token_type: int, text: str) -> None:
        """An abstract token.
        
        Args:
            token_type (int): a numeric token type from TokenTypes
            text (str): a lexeme
        """
        self.token_type = token_type
        self.text = text
    
    def __str__(self) -> str:
        return f"{self.text}, {TokenTypes(self.type).name}"