from __future__ import annotations
from typing import Dict, Generic, TYPE_CHECKING

from state import State, T

if TYPE_CHECKING:
    from tcod.console import Console
    from model import Model


class AreaState(Generic[T], State[T]):

    def __init__(self, model: Model) -> None:
        super().__init__()
        self._model = model
        self._view = None
