from __future__ import annotations
from typing import TYPE_CHECKING

from control import Control

if TYPE_CHECKING:
    from actor import Actor


class Behavior(Control):
    """Base class for NPC behaviors"""

    def __init__(self, actor: Actor) -> None:
        super().__init__(actor)
