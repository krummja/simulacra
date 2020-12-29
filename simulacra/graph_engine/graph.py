from __future__ import annotations
from typing import Union, Optional, List

import copy
import logging
import pickle
import sys

from .vertex import Vertex

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

V = Union[str, Vertex]


class Graph:

    def __init__(self) -> None:
        self._vertices = {}
        self._edges = {}
        self._neighbors = {}
        self._solutions = []
        self._match_history = []

    def add_edge(self, n: V, m: V) -> None:
        if isinstance(n, str):
            n = self._vertices[n]
        else:
            self.add_vertex(n)

        if isinstance(m, str):
            m = self._vertices[m]
        else:
            self.add_vertex(m)

        self._edges[n.vid].append(m)
        self._neighbors[n.vid].append(m)
        self._neighbors[m.vid].append(n)

        n.degree += 1
        m.degree += 1

    def add_vertex(self, vertex: Vertex) -> Vertex:
        if vertex.vid not in self._vertices:
            self._vertices[vertex.vid] = vertex
            self._edges[vertex.vid] = []
            self._neighbors[vertex.vid] = []
        else:
            vertex = self._vertices[vertex.vid]
        return vertex

    def delete_edge(self, start_vid: str, end_vid: str) -> bool:
        if start_vid not in self._vertices or end_vid not in self._vertices:
            return False

        start_vertex = self._vertices[start_vid]
        end_vertex = self._vertices[end_vid]

        if end_vertex not in self._edges[start_vid]:
            return False

        self._edges[start_vid].remove(end_vertex)
        self._neighbors[start_vid].remove(end_vertex)
        self._neighbors[end_vid].remove(start_vertex)

        start_vertex.degree -= 1
        end_vertex.degree -= 1
        return True

    def delete_vertex(self, vid: str) -> Optional[Vertex]:
        if vid not in self._vertices:
            return None

        for end_vertex in self._edges[vid]:
            self.delete_edge(vid, end_vertex.vid)

        for start_vid in self._vertices:
            self.delete_edge(start_vid, vid)

        self._edges.pop(vid)
        for _vid in self._neighbors:
            if _vid in self._neighbors[_vid]:
                self._neighbors[_vid].remove(vid)
        self._neighbors.pop(vid)

        return self._vertices.pop(vid)

    @property
    def edges(self):
        for start_vid in self._edges:
            for end_vertex in self._edges[start_vid]:
                start_vertex = self._vertices[start_vid]
                yield (start_vertex, end_vertex)

    def find_vertex(self, name: str) -> Optional[Vertex]:
        for vertex in self.vertices:
            if vertex.name == name:
                return vertex
        return None

    def has_edge_between_vertices(self, start_vid, end_vid) -> bool:
        if start_vid not in self._vertices or end_vid not in self._vertices:
            return False
        end_vertex = self._vertices[end_vid]
        return end_vertex in self._edges[start_vid]

    @property
    def labels(self) -> List[str]:
        return [v.label for v in self.vertices]

    @property
    def names(self) -> List[str]:
        return [v.name for v in self.vertices]

    @property
    def vertex_count(self):
        return len(self.vertices)

    @property
    def vertices(self):
        return self._vertices.values()

    def search(self, q):
        logging.debug("In Graph.search")
        logging.debug("Searching for %s in %s" % (q, self))

        # matches is a dict of vid(query) -> vid(data) mappings of which query
        # vertex is matched to which data graph vertex
        matches = {}

        # Find candidates for each query vertex. Only search subgraphs if all
        # query vertices have at least one data vertex candidate.
        self._solutions = []

        logging.debug("BEFORE SUBGRAPH SEARCH")
        if self._find_candidates(q):
            logging.debug(">>> SUBGRAPH SEARCH <<<")
            self._subgraph_search(matches, q)
        logging.debug("AFTER SUBGRAPH SEARCH")

        logging.debug("Out Graph.search")
        return self._solutions

    def _filter_candidates(self, u) -> List[Vertex]:
        return [vertex for vertex in self.vertices if vertex.label == u.label]

    def _find_candidates(self, q) -> bool:
        logging.debug("In Graph._find_candidates()")
        if self.vertex_count == 0 or q.vertex_count == 0:
            logging.debug("No candidates")
            return False

        for u in q.vertices:
            u.candidates = self._filter_candidates(u)
            if len(u.candidates) == 0:
                logging.debug("No candidates")
                return False

        cand_str = ""
        for i in u.candidates:
            cand_str += str(i) + " "
        logging.debug("Raw candidates for %s are %s" % (u, cand_str))
        return True

    def _find_matched_neighbors(self, u, matches) -> List[Vertex]:
        if u is None or matches is None or len(matches) == 0:
            return []

        return [v for v in self._neighbors[u.vid] if v.vid in matches]

    def _is_joinable(self, u, v, q, matches) -> bool:
        if len(matches) == 0:
            return True

        neighbors = q._find_matched_neighbors(u, matches)
        for n in neighbors:
            m = self._vertices[matches[n.vid]]
            if (q.has_edge_between_vertices(u.vid, n.vid) and
                self.has_edge_between_vertices(v.vid, m.vid)):
                return True
            elif (q.has_edge_between_vertices(n.vid, u.vid) and
                  self.has_edge_between_vertices(m.vid, v.vid)):
                return True
            else:
                return False

        return False

    def _next_unmatched_vertex(self, matches) -> Optional[Vertex]:
        for vertex in self.vertices:
            if vertex.vid not in matches:
                return vertex
        return None

    def _refine_candidates(self, candidates, u, matches) -> List[Vertex]:
        new_candidates = []
        for c in candidates:
            if c.degree >= u.degree and c.vid not in matches.values():
                new_candidates.append(c)
        return new_candidates

    def _restore_state(self, matches):
        return pickle.loads(self._match_history.pop())

    def __repr__(self):
        s = "digraph {\n"

        if len(self._vertices) == 1:
            # Only one vertex. Print it's name.
            for vertexID,vertex in self._vertices.items():
                s += f"{vertex.name}, {vertex.vid}"
        else:
            for vid, neighbors in self._edges.items():
                for neighbor in neighbors:
                    s += (f"{self._vertices[vid].name}_{self._vertices[vid].vid} "
                          f"-> {neighbor.name}_{neighbor.vid};\n")
        s = s + "\n}"
        return s

    def _subgraph_search(self, matches, q):
        # If every query vertex has been matched, then we're done. Store the
        # solution we found and return.
        logging.debug('In Graph._subgraph_search()')
        if len(matches) == len(q.vertices):
            logging.debug('Found a solution to %s' % matches)
            self._solutions.append(copy.deepcopy(matches))
            return

        # Get the next query result that needs a match.
        u = q._next_unmatched_vertex(matches)
        logging.debug('Next unmatched vertex is %s' % u)
        cand_str = ""
        for i in u.candidates:
            cand_str += str(i) + " "
        logging.debug('Raw candidates of %s are [%s]' % (u, cand_str))

        # Save the current candidates of u so we can restore them after we try
        # all existing mappings.
        old_candidates = u.candidates

        # Refine the list of candidate vertices from those obviously bad.
        u.candidates = self._refine_candidates(u.candidates, u, matches)
        cand_str = ""
        for i in u.candidates:
            cand_str += str(i) + " "
        logging.debug('Refined candidates are [%s]' % cand_str)

        # Check the candidates for a possible match.
        for v in u.candidates:
            logging.debug('Checking candidate %s for vertex %s' % (v, u))
            # Check to see u and v are joinable in self.
            if self._is_joinable(u, v, q, matches):
                logging.debug('%s is joinable to %s' % (v, u))
                # Yes they are, so store the mapping and try the next vertex.
                self._update_state(u, v, matches)
                logging.debug('Matches is now %s' % matches)
                self._subgraph_search(matches, q)

                # Undo the last mapping.
                matches = self._restore_state(matches)

        # _refine_candidates() may have removed vertices. Restore them before
        # trying another solution (returning from this recursive call).
        u.candidates = old_candidates
        logging.debug('Out Graph._subgraph_search()')

    def _update_state(self, u, v, matches):
        self._match_history.append(pickle.dumps(matches))
        matches[u.vid] = v.vid