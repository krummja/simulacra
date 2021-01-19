from __future__ import annotations
from typing import TYPE_CHECKING

import ecstremity as ecs

from simulacra.core.manager import Manager
from .components import all_components

if TYPE_CHECKING:
    from simulacra.core.game import Game


class ECSManager(Manager):
    """Manager class that wraps the `ecstremity` ECS Engine."""

    def __init__(self, game: Game) -> None:
        self.game = game
        self.engine = ecs.Engine()
        for component in all_components():
            self.engine.components.register(component)
