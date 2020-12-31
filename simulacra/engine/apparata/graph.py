"""Directional Graph"""

from __future__ import annotations
from typing import (Dict, Generator, List, Optional, Tuple, Union)

import copy
import pickle

from .node import Node

Edge = Tuple[Node, Node]


class Graph:
    """Representation of a directed graph consisting of Node objects.
    The graph can search for subgraphs.
    The graph maintains node degrees as the sum of in- and outdegrees.
    """

    def __init__(self) -> None:
        """Constructor."""
        self._nodes: Dict[str, Node] = {}
        self._edges: Dict[str, List[Node]] = {}
        self._neighbors: Dict[str, List[Node]] = {}

    @property
    def node_count(self) -> int:
        return len(self._nodes)

    @property
    def edge_count(self) -> int:
        return len(self._edges)

    def add_edge(self, n: Union[Node, str], m: Union[Node, str]) -> None:
        """Add an edge to the graph by adding two adjacent Nodes.

        Args:
            n (Node | str): Either add an existing Node or make a new one.
            m (Node | str): Either add an existing Node or make a new one.
        """
        if isinstance(n, str):
            n = self._nodes[n]
        else:
            self.add_node(n)

        if isinstance(m, str):
            m = self._nodes[m]
        else:
            self.add_node(m)

        self._edges[n.uid].append(m)
        self._neighbors[n.uid].append(m)
        self._neighbors[m.uid].append(n)

    def add_node(self, node: Node) -> Node:
        if node.uid not in self._nodes:
            self._nodes[node.uid] = node
            self._edges[node.uid] = []
            self._neighbors[node.uid] = []
        else:
            node = self._nodes[node.uid]
        return node

    def remove_edge(self, start_uid: str, end_uid: str) -> bool:
        if start_uid not in self._nodes or end_uid not in self._nodes:
            return False

        start_node = self._nodes[start_uid]
        end_node = self._nodes[end_uid]

        if end_node not in self._edges[start_uid]:
            return False

        self._edges[start_uid].remove(end_node)
        self._neighbors[start_uid].remove(end_node)
        self._neighbors[end_uid].remove(start_node)

        start_node.degree -= 1
        end_node.degree -= 1
        return True

    def remove_node(self, uid: str) -> Optional[Node]:
        if uid not in self._nodes:
            return None

        for end_node in self._edges[uid]:
            self.remove_edge(uid, end_node.uid)
        for start_uid in self._nodes:
            self.remove_edge(start_uid, uid)

        self._edges.pop(uid)
        for _uid in self._neighbors:
            if _uid in self._neighbors[_uid]:
                self._neighbors[_uid].remove(uid)
        self._neighbors.pop(uid)

        return self._nodes.pop(uid)

    @property
    def edges(self) -> Generator[Edge, None, None]:
        for start_uid in self._edges:
            for end_node in self._edges[start_uid]:
                start_node = self._nodes[start_uid]
                yield (start_node, end_node)

    def find_node(self, name: str) -> Optional[Node]:
        for node in self.nodes:
            if node.name == name:
                return node
        return None

    def has_adjacent_nodes(self, start_uid: str, end_uid: str) -> bool:
        if start_uid not in self._nodes or end_uid not in self._nodes:
            return False
        end_node = self._nodes[end_uid]
        return end_node in self._edges[start_uid]

    @property
    def labels(self) -> List[str]:
        return [node.label for node in self._nodes]

    @property
    def names(self) -> List[str]:
        return [node.name for node in self._nodes]

    @property
    def nodes(self) -> List[Node]:
        return self._nodes.values()

    @property
    def neighbors(self) -> Dict[str, List[Node]]:
        return self._neighbors


class GraphQuery:
    """Processor for matching Subgraphs of Graphs."""

    def __init__(self, data_graph: Graph) -> None:
        """Constructor.

        Args:
            data_graph (Graph): The base graph we're checking against.
        """
        self._data_graph = data_graph
        self._solutions: List[ Dict[str, Node] ] = []
        self._match_history: List[ Dict[str, Node] ] = []

    def search(self, query_graph: Graph) -> List[ Dict[str, Node] ]:
        matches = {}
        self._solutions = []

        if self.find_candidates(query_graph):
            self.subgraph_search(matches, query_graph)
        return self._solutions

    def filter_candidates(self, query_node: Node) -> List[Node]:
        return [node for node in self._data_graph.nodes if node.label == query_node.label]

    def find_candidates(self, query_graph: Graph) -> bool:
        if self._data_graph.node_count == 0 or query_graph.node_count == 0:
            return False

        for node in query_graph.nodes:
            node.candidates = self.filter_candidates(node)
            if len(node.candidates) == 0:
                return False

            candidate_string = ""
            for candidate in node.candidates:
                candidate_string += str(candidate) + " "
            return True

    def find_matched_neighbors(
            self,
            query_node: Node,
            matches: List[Node]
        ) -> List[Node]:
        if query_node is None or matches is None or len(matches) == 0:
            return []
        return [node for node in self._data_graph.neighbors[node.uid] \
                if node.uid in matches]

    def is_matchable(
            self,
            query_node: Node,
            data_node: Node,
            query_graph: Graph,
            matches: List[Node]
        ) -> bool:
        """Check whether query_node and data_node are matchable for a solution.

        The method iterates through all matched query nodes adjacent to
        query_node. If some adjacent query node, n, is already matched with a
        data node, m, then it checks whether there is a corresponding edge
        between query_node and m in the local data graph going in the same
        direction as the edge between query_node and query node n.

        Args:
            query_node (Node): Target node in the query graph.
            data_node (Node): Target node in the local data graph.
            query_graph (Graph): The query graph to check.
            matches (List[Node]): A list of previously matched nodes

        Returns:
            bool: Returns True if query_node and data_node can be matched.
        """
        if len(matches) == 0:
            return True

        neighbors = self.find_matched_neighbors(query_node, matches)
        for n in neighbors:
            m = self._data_graph.nodes[matches[n.uid]]

            if (query_graph.has_adjacent_nodes(query_node.uid, n.uid) and
                query_graph.has_adjacent_nodes(data_node.uid, m.uid)):
                return True
            elif (query_graph.has_adjacent_nodes(n.uid, query_node.uid) and
                  query_graph.has_adjacent_nodes(m.uid, data_node.uid)):
                return True
            else:
                return False

        return False

    def next_unmatched_node(self, matches: List[Node]) -> Optional[Node]:
        for node in self._data_graph.nodes:
            if node.uid not in matches:
                return node
        return None

    def refine_candidates(
            self,
            candidates: List[Node],
            query_node: Node,
            matches: List[Node]
        ) -> List[Node]:
        new_candidates: List[Node] = []
        for cand in candidates:
            if cand.degree >= query_node.degree and cand.uid not in matches.values():
                new_candidates.append(cand)
        return new_candidates

    def restore_state(self) -> List[Node]:
        return pickle.loads(self._match_history.pop())

    def __repr__(self):
        string = "digraph {\n"
        graph = self._data_graph

        if len(graph.nodes) == 1:
            for uid, node in graph.nodes.items():
                string += f"{node.name}, {node.uid}"
        else:
            for uid, neighbors in graph.edges.items():
                for neighbor in neighbors:
                    string += (f"{graph.nodes[uid].name}_{graph.nodes[uid].uid} "
                               f"-> {neighbor.name}_{neighbor.uid};\n")
        string += "\n}"
        return string

    def subgraph_search(self, matches: List[Node], query_graph: Graph) -> Node:

        # If all nodes have been matched, we're done. Store the solution
        # and return.
        if len(matches) == len(query_graph.nodes):
            self._solutions.append(copy.deepcopy(matches))
            return

        # Get the next query node that needs a match.
        query_node = self.next_unmatched_node(matches)
        candidate_string = ""
        for data_node in query_node.candidates:
            candidate_string += str(data_node) + " "

        # Save the current candidate list of query_node so we can restore
        # them after we've exhausting existing mappings.
        old_candidates = query_node.candidates

        # Refine the list of candidate nodes from those obviously not good.
        query_node.candidates = self.refine_candidates(query_node.candidates,
                                                       query_node,
                                                       matches)
        candidate_string = ""
        for data_node in query_node.candidates:
            candidate_string += str(data_node) + " "

        # Check each candidate for a possible match.
        for data_node in query_node.candidates:
            # Check to see if query_node and data_node are matchable in the
            # data graph.
            if self.is_matchable(query_node, data_node, query_graph, matches):
                # They are - store the mapping and continuel.
                self.update_state(query_graph, data_node, matches)
                self.subgraph_search(matches, query_graph)

                # Undo the last mapping.
                matches = self.restore_state()

        # refine_candidates() may have removed nodes. Restore them before
        # trying another solution (returning form the recursive call).
        query_node.candidates = old_candidates

    def update_state(
            self,
            query_node: Node,
            data_node: Node,
            matches: Dict[str, Node]
        ) -> None:
        self._match_history.append(pickle.dumps(matches))
        matches[query_node.uid] = data_node.uid
