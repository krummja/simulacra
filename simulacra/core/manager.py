from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC

if TYPE_CHECKING:
    from core.game import Game


class Manager(ABC):
    """
    The Manager class handles the processing of all game data that does not otherwise
    belong to the ECS.

    While the RenderSystem is responsible for handling the Renderable components of
    all entities in the game, the RenderManager actually handles the console and the
    battery of render functions that draw to the game screen.

    Another way to think of it: Managers coordinate systems and provide the resources
    systems need to do their work. The RenderSystem doesn't have any business having
    the actual render logic, as it is only concerned with processing Renderables.

    Instead, the RenderManager holds reference to the game's root_console, which
    the RenderSystem can grab and utilize.
    """

    @property
    def game(self) -> Game:
        return self._game

    @game.setter
    def game(self, value: Game) -> None:
        self._game = value
