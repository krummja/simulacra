from __future__ import annotations  # type: ignore
from typing import Dict, List, NamedTuple, Optional, Tuple, TYPE_CHECKING, Set
from collections import defaultdict

import numpy as np
import tcod

from simulacra.constants import CONSOLE_WIDTH, CONSOLE_HEIGHT
from .actor import Actor
from .item import Item
from .location import Location 
from .tile import tile_dt, Tile

if TYPE_CHECKING:
    from numpy import ndarray
    import tcod.console as Console
    from .model import Model


class AreaLocation(Location):

    def __init__(self, area: Area, x: int, y: int) -> None:
        self.area = area
        self.x = x
        self.y = y


class Area:
    """An object which represents a single discrete area in the game.
    
    It holds the tile and entity data for that area.
    """

    player: Actor

    def __init__(self, model: Model, width: int, height: int) -> None:
        self.model: Model = model
        self.width: int = width
        self.height: int = height
        self.shape: Tuple[int, int] = height, width

        self.tiles: ndarray = np.zeros(self.shape, dtype=tile_dt)
        self.explored: ndarray = np.zeros(self.shape, dtype=bool)
        self.visible: ndarray = np.zeros(self.shape, dtype=bool)

        self.actors: Set[Actor] = set()
        self.items: Dict[Tuple[int, int], List[Item]] = {}
        self.camera_pos: Tuple[int, int] = (0, 0)

    def is_blocked(self, x: int, y: int) -> bool:
        """Return True if this position is impassable."""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return True
        if not self.tiles[y, x]["move_cost"]:
            return True
        if any(actor.location.xy == (x, y) for actor in self.actors):
            return True

        return False

    def update_fov(self) -> None:
        """Update the player's fiew of view."""
        if not self.player.location:
            return
        self.visible = tcod.map.compute_fov(
            transparency=self.tiles["transparent"],
            pov=self.player.location.ij,
            radius=20,
            light_walls=True,
            algorithm=tcod.FOV_RESTRICTIVE
        )

        self.explored |= self.visible

    def get_camera_pos(self) -> Tuple[int, int]:
        """Get the upper left XY camera position."""
        cam_x = self.camera_pos[0] - CONSOLE_WIDTH // 2
        cam_y = self.camera_pos[1] - CONSOLE_HEIGHT // 2
        return cam_x, cam_y

    def get_camera_view(
            self, consoles: Dict[str, Console]
        ) -> Tuple[Tuple[ slice, slice], Tuple[slice, slice]]:
        """Return (screen_view, world_view) as 2D slices for NumPy."""
        cam_x, cam_y = self.get_camera_pos()

        screen_left = max(0, -cam_x)
        screen_top = max(0, -cam_y)

        world_left = max(0, cam_x)
        world_top = max(0, cam_y)

        screen_width = min(CONSOLE_WIDTH - screen_left, self.width - world_left)
        screen_height = min(CONSOLE_HEIGHT - screen_top, self.height - world_top)

        screen_view = np.s_[
            screen_top : screen_top + screen_height,
            screen_left : screen_left + screen_width
        ]

        world_view = np.s_[
            world_top : world_top + screen_height,
            world_left : world_left + screen_width
        ]

        return screen_view, world_view

    def render(self, consoles: Dict[str, Console]) -> None:
        pass

    def __getitem__(self, key: Tuple[int, int]) -> AreaLocation:
        """Return the AreaLocation for an x,y index."""
        return AreaLocation(self, *key)