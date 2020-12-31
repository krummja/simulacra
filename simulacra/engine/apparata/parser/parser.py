"""Parser module."""

from __future__ import annotations
from typing import Optional

from apparata.graph import Graph, GraphQuery
from apparata.node import Node
from apparata.parser.lexer import Lexer
from apparata.parser.rule import Rule
from apparata.parser.token import Token, TokenType


class Parser:
    """Parser for rules and directives."""

    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.lookahead = self.lexer.next_token()
        self.directives = []

    def parse(self) -> None:
        pass

    def consume(self) -> None:
        pass

    def error(self) -> None:
        pass

    def match(self, token_type: TokenType) -> Optional[Token]:
        pass

    def parse_definition(self) -> None:
        """
        definition -> ID | Rule '{' property_list '}'
        """

    def parse_property_list(self) -> None:
        """
        property_list -> property ';' property_list | nil
        """

    def parse_property(self) -> None:
        """
        property -> ID '=' '(' KEY ',' VALUE ')'
        """
