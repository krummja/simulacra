"""GraphEngine parser module."""

from __future__ import annotations
from typing import Optional

import logging
import re

from graph_engine.production import Production
from graph_engine.lexer import Lexer
from graph_engine.graph_token import Token, TokenTypes

from graph_engine.graph import Graph
from graph_engine.vertex import Vertex


class Parser:
    """Parser for graph productions."""

    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.lookahead = self.lexer.next_token()
        self.config = {}
        self.productions = []
        self.start_graph = None

        self._parsed_vertices = 0

    def parse(self) -> None:
        """grammar_file -> configuration productions"""
        self._parse_configuration()
        self._parse_productions()

    def _consume(self) -> None:
        """Consume the current token and advance to the next."""
        self.lookahead = self.lexer.next_token()

    def _error(self, string: str) -> None:
        raise SyntaxError(f"Expecting {string} found {self.lookahead} on "
                          f"line {self.lexer.line_num}")

    def _match(self, token_type) -> Optional[Token]:
        if self.lookahead.token_type == token_type:
            old_token = self.lookahead
            self._consume()
            return old_token
        else:
            self._error(TokenTypes[token_type.name])

    def _parse_config(self) -> None:
        """
        config -> ID '=' (ID | NUMBER)
        """
        key = self._match(TokenTypes.ID)
        self._match(TokenTypes.EQUALS)
        if self.lookahead.token_type == TokenTypes.ID:
            value = self._match(TokenTypes.ID)
        elif self.lookahead.token_type == TokenTypes.NUMBER:
            value = self._match(TokenTypes.NUMBER)
        else:
            self._error("ID or NUMBER")

        self.config[key.text] = value.text

    def _parse_config_list(self) -> None:
        """
        config_list -> config ';' config_list | nil
        """
        while self.lookahead.token_type == TokenTypes.ID:
            self._parse_config()
            self._match(TokenTypes.SEMICOLON)

    def _parse_configuration(self) -> None:
        """
        configuration -> 'configuration' '{' config_list '}'
        """
        self._match(TokenTypes.CONFIGURATION)
        self._match(TokenTypes.LBRACE)
        self._parse_config_list()
        self._match(TokenTypes.RBRACE)

    def _parse_edge_list(self, graph: Graph) -> None:
        """
        edge_list -> ID | ID '->' edge_list
        """
        current_vertex_token = self._match(TokenTypes.ID)
        current_vertex = self._parse_vertex_vid(current_vertex_token, graph)

        while self.lookahead.token_type == TokenTypes.ARROW:
            self._match(TokenTypes.ARROW)
            next_vertex_token = self._match(TokenTypes.ID)
            next_vertex = self._parse_vertex_vid(next_vertex_token, graph)
            graph.add_edge(current_vertex, next_vertex)
            current_vertex = next_vertex

    def _parse_graph(self) -> Graph:
        """
        graph -> edge_list | edge_list ',' graph
        """
        logging.debug('*** Parsing New Graph ***')
        graph = Graph()
        self._parse_edge_list(graph)
        while self.lookahead.token_type == TokenTypes.COMMA:
            self._match(TokenTypes.COMMA)
            self._parse_edge_list(graph)
        logging.debug('*** End Parsing ***')
        return graph

    def _parse_production(self) -> None:
        """
        prod -> graph '==>' graph
        """
        lhs = self._parse_graph()
        self._match(TokenTypes.DOUBLEARROW)
        rhs = self._parse_graph()
        self.productions.append( Production(lhs, rhs) )

    def _parse_production_list(self) -> None:
        """
        prod_list -> prod ';' prod_list | nil
        """
        while self.lookahead.token_type == TokenTypes.ID:
            self._parse_production()
            self._match(TokenTypes.SEMICOLON)

    def _parse_productions(self) -> None:
        """
        productions -> 'productions' '{' start_graph prod_list '}'
        """
        self._match(TokenTypes.PRODUCTIONS)
        self._match(TokenTypes.LBRACE)
        self._parse_start_graph()
        self._parse_production_list()
        self._match(TokenTypes.RBRACE)

    def _parse_start_graph(self) -> None:
        """
        start_graph -> graph ';'
        """
        self.start_graph = self._parse_graph()
        self._match(TokenTypes.SEMICOLON)

    def _parse_vertex_vid(self, token: Token, graph: Graph) -> Vertex:
        """
        Parses the given token (ID) into a text label and optional vertex
        number (e.g. "A1"). If a vertex with these two data don't exist in
        the given graph, it is added. Otherwise, the existing vertex from the
        graph is returned.
        """
        label = re.match('[A-z]+', token.text).group(0)
        match = re.search('[0-9]+$', token.text)
        number = match.group(0) if match is not None else None
        name = Vertex.make_name(label, number)
        vertex = graph.find_vertex(name)
        if vertex is None:
            vertex = Vertex("v%d" % graph.vertex_count, label=label, number=number)
            logging.debug('Vertex was None. Adding new Vertex as %s' % vertex.vid)
            graph.add_vertex(vertex)
        return vertex
