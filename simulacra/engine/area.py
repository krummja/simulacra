from __future__ import annotations  # type: ignore
from typing import Dict, List, NamedTuple, Optional, Tuple, TYPE_CHECKING, Set
from collections import defaultdict

import numpy as np
import time
import tcod

from constants import *
from engine.particles import *
from engine.actor import Actor
from engine.character.player import Player
from engine.character.neutral import *
from engine.item import Item
from engine.location import Location 
from engine.graphic import Graphic
from engine.tile import tile_dt, tile_graphic, Tile

if TYPE_CHECKING:
    from numpy import ndarray
    import tcod.console as Console
    from engine.model import Model



class AreaLocation(Location):

    def __init__(self, area: Area, x: int, y: int) -> None:
        self.area = area
        self.x = x
        self.y = y


class Area:
    """An object which represents a single discrete area in the game.
    
    It holds the tile and entity data for that area.
    """

    DARKNESS = np.asarray((0, (0, 0, 0), (0, 0, 0)), dtype=tile_graphic)

    player: Player

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

        self.particle_system = ParticleSystem(30, 30)

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
        cam_x = self.camera_pos[0] - STAGE_PANEL_WIDTH // 2
        cam_y = self.camera_pos[1] - STAGE_PANEL_HEIGHT // 2
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

        screen_width = min(STAGE_PANEL_WIDTH - screen_left, self.width - world_left)
        screen_height = min(STAGE_PANEL_HEIGHT - screen_top, self.height - world_top)

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
        cam_x, cam_y = self.get_camera_pos()

        screen_view, world_view = self.get_camera_view(consoles)

        consoles['ROOT'].tiles_rgb[screen_view] = np.select(
            (self.visible[world_view], self.explored[world_view]),
            (self.tiles["light"][world_view], self.tiles["dark"][world_view]),
            self.DARKNESS,
        )

        visible_objs: Dict[Tuple[int, int], List[Graphic]] = defaultdict(list)
        for obj in self.actors:
            obj_x, obj_y = obj.location.x - cam_x, obj.location.y - cam_y
            if not (0 <= obj_x < STAGE_PANEL_WIDTH and 0 <= obj_y < STAGE_PANEL_HEIGHT):
                continue
            if not self.visible[obj.location.ij]:
                continue
            obj.character.bg = self.get_bg_color(consoles, (obj.location.y, obj.location.x))
            visible_objs[obj_y, obj_x].append(obj.character)

        for ij, graphics in visible_objs.items():
            graphic = min(graphics)
            consoles['ROOT'].tiles_rgb[["ch", "fg", "bg"]][ij] = graphic.char, graphic.color, graphic.bg

    def get_bg_color(self, consoles: Dict[str, Console], pos: Tuple[int, int]):
        tile = self.tiles[pos[0], pos[1]]
        return list(tile[2][1][0:3])

    def __getitem__(self, key: Tuple[int, int]) -> AreaLocation:
        """Return the AreaLocation for an x,y index."""
        return AreaLocation(self, *key)