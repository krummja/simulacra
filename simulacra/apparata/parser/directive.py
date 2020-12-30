"""Directive for world generator."""

from __future__ import annotations


class Directive:
    """Representation of a world generation directive.

    Directives have the form L( = R)
        - 'L' is some property of an area-mappable object
        - Optionally, an equals sign denotes assignment to the property.
        - If an equals sign is present, two different value types may be used:
            - a number (integer or float)
            - a string-number tuple
        - If an equals sign is not present, the directive is interpreted
          as a boolean command, flipping a False value to True.
    """

    def __init__(self, *, pattern, replacement) -> None:
        """Constructor."""
        self.pattern = pattern
        self.replacement = replacement

    @property
    def left_hand_side(self):
        """Alias property for pattern graph."""
        return self.pattern

    @left_hand_side.setter
    def left_hand_side(self, value) -> None:
        self.pattern = value

    @property
    def right_hand_side(self):
        """Alias property for replacement graph."""
        return self.replacement

    @right_hand_side.setter
    def right_hand_side(self, value) -> None:
        self.replacement = value

    def __str__(self) -> str:
        return f"{self.pattern} ==> {self.replacement}"
