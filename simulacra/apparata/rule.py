"""Basic rewrite rule for graph transformation."""
from __future__ import annotations

from apparata.graph import Graph


class Rule:
    """Representation of a production rule.

    Rules have the form L ==> R where L is a pattern graph and R a replacement
    graph. For example, the graph A->B may be rewritten to the graph A->C->B
    through the application of the rule A->B ==> A->C->B.
    """

    def __init__(self, *, pattern: Graph, replacement: Graph) -> None:
        """Constructor.

        Args:
            pattern (Graph): Left-hand side pattern graph to be transformed.
            replacement (Graph): Right-hand side replacement graph.
        """
        self.pattern = pattern
        self.replacement = replacement

    @property
    def lhs(self) -> Graph:
        """Alias property for pattern graph."""
        return self.pattern

    @lhs.setter
    def lhs(self, value: Graph) -> None:
        self.pattern = value

    @property
    def rhs(self) -> Graph:
        """Alias property for replacement graph."""
        return self.replacement

    @rhs.setter
    def rhs(self, value: Graph) -> None:
        self.replacement = value

    def __str__(self) -> str:
        return f"{self.pattern} ==> {self.replacement}"
