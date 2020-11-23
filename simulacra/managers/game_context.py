from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model import Model


class GameContext:

    def __init__(self, model: Model):
        self.player = None
        self.factory_service = None
        self.character_factory = None
