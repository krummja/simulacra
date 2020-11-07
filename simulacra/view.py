from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from tcod.console import Console


class View(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def draw(self, consoles: Dict[str, Console]) -> None:
        raise NotImplementedError()
