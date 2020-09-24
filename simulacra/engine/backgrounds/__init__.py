from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

from engine.paths import Path, Fighter
from engine.graphic import Graphic
from engine.actor import Actor

if TYPE_CHECKING:
    from engine.model import Model


class Background:
    
    def __init__(self, model: Model) -> None:
        self.model = model
        self.model.player.background = self