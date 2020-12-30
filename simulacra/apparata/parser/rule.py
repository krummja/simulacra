"""Rewrite rule for graph transformation"""

from __future__ import annotations

from apparata.graph import Graph


class Rule:
    """Representation of a Rule."""

    def __init__(self, *, pattern: Graph, replacement: Graph) -> None:
        """Constructor."""
        self.pattern = pattern
        self.replacement = replacement
