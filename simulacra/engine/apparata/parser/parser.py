"""Parser module."""

from __future__ import annotations
from typing import Dict, Optional, Union, Tuple

import re

from engine.apparata.graph import Graph, GraphQuery
from engine.apparata.node import Node
from engine.apparata.parser.lexer import Lexer
# from engine.apparata.parser.rule import Rule, Transformation
from engine.apparata.parser.token import Token, TokenType


class Parser:
    """Parser for rules and directives."""

    def __init__(self, lexer: Lexer) -> None:
        """Constructor.

        `nodes` is a dictionary of
        """
        self.lexer = lexer
        self.lookahead = self.lexer.next_token()
        self.node_count = 0
        self.edge_count = 0
        self.unconfigured_nodes = []
        self.unconfigured_edges = []
        self.nodes: Dict[str, Dict[str, Union[str, int]]] = {}
        self.edges: Dict[Tuple[str, str]] = {}

        self.gquery = GraphQuery()

    def parse(self) -> None:
        while self.lookahead.token_type != TokenType.EOF:
            self.parse_configurations()

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
        self.error(TokenType[token_type.name])

    def parse_node_property(self, current_node: str):
        """
        node_property -> ID '=' (ID | NUMBER)
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

    def parse_node_property_list(self, current_node: str):
        """
        node_property_list -> property ';' node_property_list | nil
        """
        if current_node not in self.nodes.keys():
            self.nodes[current_node] = {}
            self.node_count += 1

        while self.lookahead.token_type == TokenType.ID:
            self.parse_node_property(current_node)
            self.match(TokenType.SEMICOLON)

    def parse_edge_property(self, connecting_node, current_node):
        """
        edge_property -> ID '=' (ID | NUMBER)
        """
        key = self.match(TokenType.ID)
        self.match(TokenType.EQUALS)

        if self.lookahead.token_type == TokenType.ID:
            value = str(self.match(TokenType.ID))
        elif self.lookahead.token_type == TokenType.NUMBER:
            value = self.match(TokenType.NUMBER)
        else:
            self.error('ID or NUMBER')
        self.edges[(connecting_node, current_node)][key] = value

    def parse_edge_property_list(self, connecting_node, current_node):
        """
        edge_property_list -> property ';' edge_property_list | nil
        """
        while self.lookahead.token_type == TokenType.ID:
            self.parse_edge_property(connecting_node, current_node)
            self.match(TokenType.SEMICOLON)

    def parse_edge_configuration(self, connecting_node):
        """
        edge_configuration -> '->' ID '{' property_list '}'
        """
        while self.lookahead.token_type == TokenType.ARROW:
            self.match(TokenType.ARROW)

            current_node = self.match(TokenType.ID)

            if current_node not in self.nodes.keys():
                self.node_count += 1
                self.nodes[current_node] = {}
                self.unconfigured_nodes.append(current_node)

            if (connecting_node, current_node) not in self.edges.keys():
                self.edges[(connecting_node, current_node)] = {}
                self.edge_count += 1

            self.match(TokenType.LBRACE)
            self.parse_edge_property_list(connecting_node, current_node)
            self.match(TokenType.RBRACE)

    def parse_configurations(self):
        """
        configurations -> ID '{' property_list [edge_config] '}'
        """
        current_node = self.match(TokenType.ID)

        self.match(TokenType.LBRACE)
        self.parse_node_property_list(current_node)
        self.parse_edge_configuration(current_node)
        self.match(TokenType.RBRACE)

    def parse_node_uid(self, token: Token, graph: Graph) -> Node:
        label = re.match('[A-z]+', token.text).group(0)
        match = re.search('[0-9]+$', token.text)
        number = match.group(0) if match is not None else None
        name = Node.make_name(label, number)
        node = graph.find_node(name)
        if node is None:
            node = Node(f"N{graph.node_count}", label=label, number=number)
            graph.add_node(node)
        return node

    def parse_edges(self, graph: Graph) -> None:
        pass

    def parse_nodes(self):
        """Build the starting graph by first parsing nodes in the node dict."""

    def parse_transformations(self):
        """Take in a generated topology and do some work to it."""
