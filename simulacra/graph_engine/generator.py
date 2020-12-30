"""GraphEngine graph generator module."""

from __future__ import annotations
from typing import Dict, List, TYPE_CHECKING

import logging
import random
import sys

from graph_engine.parser import Parser
from graph_engine.lexer import Lexer
from graph_engine.vertex import Vertex

if TYPE_CHECKING:
    from graph_engine.graph import Graph


class Generator:
    """Transformation engine for graphs.

    Given a set of productions of the form LHS ==> RHS, and using a starting
    graph G, uses graph isomorphic searching to find instances of LHS in G
    and replaces these LHS vertices with RHS.

    The engine continues to apply these transformations until G contains a
    given number of vertices. This assumes that the productions generally
    increase the number of vertices.
    """

    def apply_productions(self, start_graph: Graph, productions, config):
        logging.debug('In Generator.apply_productions()')
        while start_graph.vertex_count < int(config['min_vertices']):
            # The current behavior of the generator is to try to get to min_vertices
            # with the available rule. Because it can always add vertices, and because
            # it doesn't enforce identity on the nodes, we get into the following
            # situation:

            #   min = 4
            #   A;
            #   A ==> A -> B;
            #   B ==> B -> C;
            #   C ==> C -> D;

            # The resulting output is not what might be expected:

            #   B2 <- A -> B1 -> C          actual output
            #   A -> B -> C -> D            expected output



            matches = self._find_matching_productions(start_graph, productions)
            if len(matches) == 0:
                raise RuntimeError('No productions match the given graph.')
            # (prod, mapping) = random.choice(matches)
            for prod, mapping in matches:
                self._apply_production(start_graph, prod, mapping)

    def generate_from_file(self, file_name):
        grammar_file = open(file_name, 'r')
        file = self._parse_grammar_file(grammar_file.read())
        grammar_file.close()

        self.apply_productions(file.start_graph, file.productions, file.config)
        return file.start_graph

    def _add_new_edges(self, graph, production, rhs_mapping):
        logging.debug('>>> Generator._add_new_edges() <<<')
        for rhs_edge in production.rhs.edges:
            graph_start_vid = rhs_mapping[rhs_edge[0].vid]
            graph_end_vid = rhs_mapping[rhs_edge[1].vid]
            if not graph.has_edge_between_vertices(graph_start_vid, graph_end_vid):
                graph.add_edge(graph_start_vid, graph_end_vid)
        logging.debug('graph is now %s' % graph)

    def _add_new_vertices(self, graph, production, rhs_mapping):
        logging.debug('>>> Generator._add_new_vertices() <<<')
        for rhs_vertex in production.rhs.vertices:
            if rhs_vertex.name not in production.lhs.names:
                new_vid = f"v{graph.vertex_count}"
                new_vertex = graph.add_vertex(Vertex(new_vid,
                                                     label=rhs_vertex.label,
                                                     number=rhs_vertex.number))
                logging.debug('Added vertex %s' % new_vertex)
                rhs_mapping[rhs_vertex.vid] = new_vid
        logging.debug('Graph is now %s' % graph)

    def _apply_production(self, graph, production, lhs_mapping: Dict[str, str]):
        """
        Applies the given production to the given graph.
        """
        rhs_mapping = self._map_rhs_to_graph(graph, production, lhs_mapping)
        self._delete_missing_vertices(graph, production, lhs_mapping)
        self._delete_missing_edges(graph, production, lhs_mapping, rhs_mapping)
        self._add_new_vertices(graph, production, rhs_mapping)
        self._add_new_edges(graph, production, rhs_mapping)

    def _delete_missing_edges(self, graph, production, lhs_mapping, rhs_mapping):
        logging.debug('>>> Generator._delete_missing_edges() <<<')
        for lhs_edge in production.lhs.edges:
            start_vid = lhs_mapping[lhs_edge[0].vid]
            end_vid = lhs_mapping[lhs_edge[1].vid]

            rhs_start = [rhs_vid for rhs_vid, graph_id in rhs_mapping.items() \
                         if graph_id == start_vid]
            if len(rhs_start) == 0:
                logging.debug('edge start from %s to %s does not appear in RHS.' % (lhs_edge[0], lhs_edge[1]))
                graph.delete_edge(start_vid, end_vid)
                continue

            rhs_end = [rhs_vid for rhs_vid, graph_id in rhs_mapping.items() \
                       if graph_id == end_vid]
            if len(rhs_end) == 0:
                logging.debug('edge start from %s to %s does not appear in RHS.' % (lhs_edge[0], lhs_edge[1]))
                graph.delete_edge(start_vid, end_vid)
                continue

            if not production.rhs.has_edge_between_vertices(rhs_start[0], rhs_end[0]):
                logging.debug('edge start from %s to %s does not appear in RHS.' % (lhs_edge[0], lhs_edge[1]))
                graph.delete_edge(start_vid, end_vid)

    def _delete_missing_vertices(self, graph, production, lhs_mapping):
        logging.debug('>>> Generator._delete_missing_vertices() <<<')
        for lhs_vertex in production.lhs.vertices:
            if not production.rhs.find_vertex(lhs_vertex.name):
                graph_vid = lhs_mapping[lhs_vertex.vid]
                logging.debug('Deleting vertex %s' % graph_vid)
                graph.delete_vertex(graph_vid)

    def _find_matching_productions(self, graph, productions):
        logging.debug('In Generator._find_matching_productions()')
        solutions = []
        for prod in productions:
            logging.debug('Checking productions LHS %s' % prod.lhs)
            matches: List[Graph] = graph.search(prod.lhs)
            print(f"MATCHES: {len(matches)}")
            if len(matches) > 0:
                for match in matches:
                    solutions.append( (prod, match) )
                    logging.debug('Production %s matches' % prod.lhs)
            else:
                logging.debug('Production %s does not match' % prod.lhs)
        logging.debug('Out Generator._find_matching_productions()')
        return solutions

    def _map_rhs_to_graph(self, graph, production, lhs_mapping):
        rhs_mapping = {}

        for rhs_vertex in production.rhs.vertices:
            if rhs_vertex.name in production.lhs.names:
                lhs_vertex = production.lhs.find_vertex(rhs_vertex.name)
                print(f"LHS_MAPPING: {type(lhs_mapping)}")
                rhs_mapping[rhs_vertex.vid] = lhs_mapping[lhs_vertex.vid]
        return rhs_mapping

    def _parse_grammar_file(self, grammar_file):
        parser = Parser(Lexer(grammar_file))
        parser.parse()
        return parser
