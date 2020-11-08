from __future__ import annotations
from typing import Dict, List, Protocol, Optional, TYPE_CHECKING
from contextlib import suppress
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from tcod.console import Console


class ViewObserver(Protocol):
    def update(self, subject: View) -> None:
        pass


class View(ABC):

    def __init__(self) -> None:
        self._observers: List[ViewObserver] = []

    # def attach(self, observer: ViewObserver) -> None:
    #     if observer not in self._observers:
    #         self._observers.append(observer)
    #
    # def detach(self, observer: ViewObserver) -> None:
    #     with suppress(ValueError):
    #         self._observers.remove(observer)
    #
    # def notify(self, modifier: Optional[ViewObserver] = None) -> None:
    #     for observer in self._observers:
    #         if modifier != observer:
    #             observer.update(self)

    @abstractmethod
    def draw(self, consoles: Dict[str, Console]) -> None:
        raise NotImplementedError()


# TODO: I need to figure out a good way to get data sources like Storage inside here.
