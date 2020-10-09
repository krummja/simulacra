from __future__ import annotations
from typing import List, Set, Tuple
from collections import defaultdict

import numpy as np

from config import *
from engine.geometry import *
from engine.location import Location
from engine.graphic import Graphic
from engine.tile import tile_dt, tile_graphic
from engine.hues import COLOR

if TYPE_CHECKING:
    from numpy import ndarray
    from tcod.console import Console
    from engine.components.actor import Actor
    from engine.items import Item
    from engine.player import Player


class AreaLocation(Location):

    def __init__(self: AreaLocation, area: Area, x: int, y: int) -> None:
        self.area = area
        self.x = x
        self.y = y


class Area:

    DARKNESS = np.asarray(
        (0, COLOR['nero'], COLOR['black']),
        dtype=tile_graphic
        )

    _player: Player = None

    def __init__(self, model, width, height) -> None:
        self.model = model
        self.width = width
        self.height = height
        self.shape: Tuple[int, int] = height, width

        self.tiles: ndarray = np.zeros(self.shape, dtype=tile_dt)
        self.explored: ndarray = np.zeros(self.shape, dtype=bool)
        self.visible: ndarray = np.zeros(self.shape, dtype=bool)

        self.actors: Set[Actor] = set()
        self.items: Dict[Tuple[int, int], List[Item]] = {}
        self.nearby_items: List[List[Item]] = []
        self.camera_pos: Tuple[int, int] = (0, 0)

        self.fov_radius = 8

    @property
    def player(self: Area) -> Player:
        return self._player

    @player.setter
    def player(self: Area, value: Player) -> None:
        self._player = value

    def is_blocked(self, x: int, y: int) -> bool:
        """Return True if this position is impassable."""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return True

        # Tiles with high move cost are treated as blocking
        if not self.tiles[y, x]["move_cost"]:
            return True

        # Can't walk through actors
        if any(actor.location.xy == (x, y) for actor in self.actors):
            return True

        return False

    def update_fov(self) -> None:
        """Update the player's field of view."""
        if not self.player.location:
            return
        self.visible = tcod.map.compute_fov(
            transparency=self.tiles["transparent"],
            pov=self.player.location.ij,
            radius=10,
            light_walls=True,
            algorithm=tcod.FOV_RESTRICTIVE
            )

        self.explored |= self.visible

    def get_camera_pos(self: Area) -> Tuple[int, int]:
        """Get the upper left XY camera position."""
        cam_x = self.camera_pos[0] - STAGE_PANEL_WIDTH // 2
        cam_y = self.camera_pos[1] - STAGE_PANEL_HEIGHT // 2
        return cam_x, cam_y

    def get_camera_view(
            self: Area
        ) -> Tuple[Tuple[slice, slice], Tuple[slice, slice]]:
        """Return (screen_view, world_view) as 2D slices for NumPy."""
        cam_x, cam_y = self.get_camera_pos()

        screen_left = max(0, -cam_x)
        screen_top = max(0, -cam_y)

        world_left = max(0, cam_x)
        world_top = max(0, cam_y)

        screen_width = min(
            STAGE_PANEL_WIDTH - screen_left, self.width - world_left
            )
        screen_height = min(
            STAGE_PANEL_HEIGHT - screen_top, self.height - world_top
            )

        screen_view = np.s_[
            screen_top: screen_top + screen_height,
            screen_left: screen_left + screen_width
            ]

        world_view = np.s_[
            world_top: world_top + screen_height,
            world_left: world_left + screen_width
            ]

        return screen_view, world_view

    def render(self, consoles: Dict[str, Console]) -> None:
        consoles['ROOT'].clear()
        cam_x, cam_y = self.get_camera_pos()
        screen_view, world_view = self.get_camera_view()

        # noinspection PyTypeChecker
        consoles['ROOT'].tiles_rgb[screen_view] = np.select(
            (self.visible[world_view], self.explored[world_view]),
            (self.tiles["light"][world_view], self.tiles["dark"][world_view]),
            self.DARKNESS
            )

        visible_objs: Dict[Tuple[int, int], List[Graphic]] = defaultdict(list)
        for obj in self.actors:
            obj_x, obj_y = obj.location.x - cam_x, obj.location.y - cam_y

            if not (0 <= obj_x < STAGE_PANEL_WIDTH and
                    0 <= obj_y < STAGE_PANEL_HEIGHT):
                continue
            if not self.visible[obj.location.ij]:
                continue
            obj.owner.bg = self.get_bg_color(
                obj.location.x,
                obj.location.y
                )

            visible_objs[obj_y, obj_x].append(obj.owner)

        for (item_x, item_y), items in self.items.items():
            obj_x, obj_y = item_x - cam_x, item_y - cam_y
            if not (0 <= obj_x < CONSOLE_WIDTH and 0 <= obj_y < CONSOLE_HEIGHT):
                continue
            if not self.visible[item_y, item_x]:
                continue
            visible_objs[obj_y, obj_x].extend(items)

        for ij, graphics in visible_objs.items():
            graphic = min(graphics)
            consoles['ROOT'].tiles_rgb[
                ["ch", "fg", "bg"]
                ][ij] = graphic.char, graphic.color, graphic.bg

    def examine_nearby(self: Area):
        self.nearby_items.clear()
        for position in Point(*self.model.player.location.xy).neighbors:
            try:
                if self.items[position[0], position[1]]:
                    self.nearby_items.append(self.items[position])
            except KeyError:
                continue

    def get_bg_color(self: Area, x: int, y: int) -> Tuple[int, int, int]:
        tile = self.tiles[y, x]
        return list(tile[2][1][0:3])

    def __getitem__(self: Area, key: Tuple[int, int]) -> AreaLocation:
        return AreaLocation(self, *key)
