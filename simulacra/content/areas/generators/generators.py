from __future__ import annotations
from typing import Any, List, Optional
from abc import ABC, abstractmethod


class Algorithm(ABC):

    def __init__(self) -> None:
        self._children: List[Algorithm] = []

    @property
    def parent(self) -> Algorithm:
        return self._parent

    @parent.setter
    def parent(self, value: Optional[Algorithm]) -> None:
        self._parent = value

    def add(self, algorithm: Algorithm) -> None:
        self._children.append(algorithm)
        algorithm.parent = self

    def remove(self, algorithm: Algorithm) -> None:
        self._children.remove(algorithm)
        algorithm.parent = None

    @property
    def is_composite(self) -> bool:
        return False

    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError("No generator implemented!")
