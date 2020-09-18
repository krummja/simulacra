from __future__ import annotations  # type: ignore
from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from simulacra.engine.actor import Actor
    from simulacra.engine.area import Area
    from simulacra.engine.item import Item
    from simulacra.engine.location import Location
    from simulacra.engine.model import Model


class Action:

    def __init__(self, actor: Actor) -> None:
        self.actor = actor