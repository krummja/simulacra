from __future__ import annotations
from typing import Type, TYPE_CHECKING

from ecstremity import Component

if TYPE_CHECKING:
    from .render_manager import RenderManager


class WorldRenderer:

    def __init__(self, manager: RenderManager) -> None:
        self.manager = manager
        self.area_grid = self.manager.game.area.current_area.grid
        self.console = self.manager.root_console

    def render_ground_tile(self, x, y) -> None:
        pass

    def draw_to_stage(
            self,
            x: int,
            y: int,
            target: Type[Component],
            layer: int = 0
        ) -> None:
        pass


class EntityRenderer:

    def __init__(self, manager: RenderManager) -> None:
        self.manager = manager
