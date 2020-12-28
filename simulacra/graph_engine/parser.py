from __future__ import annotations

import logging
import random
import sys

from graph_engine.production import Production
from graph_engine.lexer import Lexer
from graph_engine.token import Token, TokenTypes

from graph_engine.graph import Graph
from graph_engine.vertex import Vertex


class Parser:
    
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.lookahead = self.lexer.next_token()
        self.config = {}
        self.productions = []
        self.start_graph = None
        
        self._parsed_vertices = 0
        
    def parse(self):
        self._parse_configuration()
        self._parse_productions()
    
    def _consume(self) -> None:
        self.lookahead = self.lexer.next_token()
        
    def _error(self, string: str) -> None:
        pass
    
    def _match(self, token_type):
        pass
    
    def _parse_config(self):
        pass
    
    def _parse_config_list(self):
        pass
    
    def _parse_configuration(self):
        pass
    
    def _parse_edge_list(self, graph: Graph):
        pass
    
    def _parse_graph(self):
        pass
    
    def _parse_production(self):
        pass
    
    def _parse_production_list(self):
        pass
    
    def _parse_productions(self):
        pass
    
    def _parse_start_graph(self):
        pass
    
    def _parse_vertex_vid(self, token: Token, graph: Graph) -> Vertex:
        pass
        