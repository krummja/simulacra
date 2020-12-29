"""GraphEngine production module."""

from __future__ import annotations


class Production:
    """Represents a production consisting of a left and right side."""

    def __init__(self, left, right) -> None:
        """Constructor.

        Args:
            left (): graph object on the left side of the rule.
            right (): graph object on the right side of the rule.
        """
        self._lhs = left
        self._rhs = right

    def __str__(self):
        return str(self._lhs) + ' ==> ' + str(self._rhs) + '\n'

    @property
    def lhs(self):
        return self._lhs

    @lhs.setter
    def lhs(self, value):
        self._lhs = value

    @property
    def rhs(self):
        return self._rhs

    @rhs.setter
    def rhs(self, value):
        self._rhs = value
