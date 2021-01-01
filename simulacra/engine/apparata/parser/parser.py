"""Parser module."""

from __future__ import annotations
from typing import Dict, Optional, Union

from collections import defaultdict

from engine.apparata.graph import Graph, GraphQuery
from engine.apparata.node import Node
from engine.apparata.parser.lexer import Lexer
from engine.apparata.parser.rule import Rule
from engine.apparata.parser.token import Token, TokenType


class Parser:
    """Parser for rules and directives."""

    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.lookahead = self.lexer.next_token()
        self.node_count = 0
        self.nodes: Dict[str, Dict[str, Union[str, int]]] = {}

    def parse(self) -> None:
        while self.lookahead.token_type != TokenType.EOF:
            self.parse_node_configuration()

    def consume(self) -> None:
        self.lookahead = self.lexer.next_token()

    def error(self, string: str) -> None:
        raise SyntaxError(f"Expecting {string} found {self.lookahead} on "
                          f"line {self.lexer.line_num}")

    def match(self, token_type: TokenType) -> Optional[Token]:
        if self.lookahead.token_type == token_type:
            old_token = self.lookahead
            self.consume()
            return old_token
        else:
            self.error(TokenType[token_type.name])

    def parse_property(self, current_node: str):
        """
        property -> ID '=' (ID | NUMBER)
        """
        key = self.match(TokenType.ID)
        self.match(TokenType.EQUALS)

        if self.lookahead.token_type == TokenType.ID:
            value = str(self.match(TokenType.ID))
        elif self.lookahead.token_type == TokenType.NUMBER:
            value = self.match(TokenType.NUMBER)
        else:
            self.error('ID or NUMBER')
        self.nodes[current_node][key] = value

    def parse_property_list(self, current_node: str):
        """
        property_list -> property ';' property_list | nil
        """
        while self.lookahead.token_type == TokenType.ID:
            self.parse_property(current_node)
            self.match(TokenType.SEMICOLON)

    def parse_node_configuration(self):
        """
        node_configuration -> node_uid '{' property_list '}'
        """
        current_node = self.match(TokenType.ID)
        self.nodes[current_node] = {}

        self.match(TokenType.LBRACE)
        self.parse_property_list(current_node)
        self.match(TokenType.RBRACE)
        self.node_count += 1
