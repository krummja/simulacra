from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from tcod.console import Console

    from state import State


class ViewObserver(Protocol):
    def update(self, subject: View) -> None:
        pass


class View(ABC):

    def __init__(self, state: State) -> None:
        self._state = state
