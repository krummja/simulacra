"""Rewrite rule for graph transformation"""

from __future__ import annotations

from engine.apparata.graph import Graph


class Rule:
    """Representation of a Rule."""

    def __init__(self, *, pattern: Graph, replacement: Graph) -> None:
        """Constructor."""
        self.pattern = pattern
        self.replacement = replacement


class Transformation:
    """Representation of a transformation rule."""

    def __init__(self, *, pattern: Graph, replacement: Graph) -> None:
        """Constructor."""
        self.pattern = pattern
        self.replacement = replacement
