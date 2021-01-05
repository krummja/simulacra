"""Node of a Graph"""

from __future__ import annotations
from typing import Any, Dict, List, Optional


class Node:
    """Representation of a graph node.

    A node must have a unique string ID. It may have a label and a number.
    Graphs update node degrees as the graph is updated."""

    def __init__(
            self,
            uid: str,
            label: Optional[str] = None,
            number: Optional[int] = None,
            data: Dict[str, Any] = None
        ) -> None:
        """Constructor.

        Args:
            uid (str): Unique ID for identifying this node.
            label (str, optional): Label character (A-Z). Defaults to None.
            number (int, optional): Integer index. Defaults to None.
        """
        self.uid = uid
        self.label = label
        self.number = number

        self.degree: int = 0
        self.candidates: List[Node] = []

        if data is None:
            self._data = {}
        else:
            self._data = data

    @property
    def data(self) -> Dict[str, Any]:
        return self._data

    @data.setter
    def data(self, value: Dict[str, Any]) -> None:
        self._data = value

    @staticmethod
    def make_name(label: Optional[str], number: Optional[int]) -> str:
        if label is None and number is None:
            return ''
        if number is None:
            return label
        if label is None:
            return str(number)
        return f"{label}, {number}"

    @property
    def name(self) -> str:
        return self.make_name(self.label, self.number)

    def __str__(self) -> str:
        return (
            f"{self.uid}, {self.label}, "
            f"{self.number if self.number is not None else ''}"
            )
