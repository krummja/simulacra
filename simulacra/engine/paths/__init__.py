from __future__ import annotations  # type: ignore
from typing import Optional, Type, TYPE_CHECKING


from engine.actor import Actor
from engine.graphic import *

if TYPE_CHECKING:
    from engine.model import Model
    from engine.actions import Action
    from engine.location import Location


class Path:
    
    def __init__(self, model: Model) -> None:
        self.model = model
        self.model.player.path = self