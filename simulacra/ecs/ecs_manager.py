from __future__ import annotations
from typing import TYPE_CHECKING

import os, json
import ecstremity as ecs

from simulacra.core.manager import Manager
from .components import all_components

if TYPE_CHECKING:
    from simulacra.core.game import Game


JSON_PATH = "simulacra/ecs/prefabs/"


class ECSManager(Manager):
    """Manager class that wraps the `ecstremity` ECS Engine."""

    def __init__(self, game: Game) -> None:
        self.game = game
        self.engine = ecs.Engine()

        for component in all_components():
            self.engine.components.register(component)

        for file in self.load_prefab_files():
            file = JSON_PATH + file
            with open(file) as f:
                definition = json.load(f)
                self.engine.prefabs.register(definition)

    def load_prefab_files(self):
        return [f for f in os.listdir(JSON_PATH) if f.endswith('.json')]
