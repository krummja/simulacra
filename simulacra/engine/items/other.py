from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

from engine.items import Item
from engine.graphic import Graphic

if TYPE_CHECKING:
    from engine.actor import Actor


class Corpse(Item):

    char = ord("%")
    color = (127, 0, 0)
    render_order = 2

    def __init__(self, actor: Actor) -> None:
        super().__init__()
        self.name = f"{actor.character.name} Corpse"