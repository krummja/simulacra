from __future__ import annotations
from typing import Dict, List, Protocol, Optional, TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from tcod.console import Console
    from state import State


class ViewObserver(Protocol):
    def update(self, subject: View) -> None:
        pass


class View(ABC):

    def __init__(self, state: State) -> None:
        self._state = state

    @abstractmethod
    def draw(self, consoles: Dict[str, Console]) -> None:
        raise NotImplementedError()
