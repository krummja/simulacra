from __future__ import annotations
from typing import TYPE_CHECKING

import logging
import random
import sys

from graph_engine.parser import Parser
from graph_engine.lexer import Lexer
from graph_engine.vertex import Vertex


class Generator:
    """Transformation engine for graphs.
    
    Given a set of productions of the form LHS ==> RHS, and using a starting
    graph G, uses graph isomorphic searching to find instances of LHS in G
    and replaces these LHS vertices with RHS.
    
    The engine continues to apply these transformations until G contains a
    given number of vertices. This assumes that the productions generally
    increase the number of vertices.
    """
    
    def apply_productions(self, start_graph, productions, config):
        pass
    
    def _add_new_edges(self, graph, production, rhs_mapping):
        pass
    
    def _add_new_vertices(self, graph, production, rhs_mapping):
        pass
    
    def _apply_production(self, graph, production, lhs_mapping):
        pass
    
    def _delete_missing_edges(self, graph, production, lhs_mapping, rhs_mapping):
        pass
    
    def _delete_missing_vertices(self, graph, production, lhs_mapping):
        pass
    
    def _find_matching_production(self, graph, productions):
        pass
    
    def _map_rhs_to_graph(self, graph, production, lhs_mapping):
        pass
    
    def _parse_grammar_file(self, grammar_file):
        pass