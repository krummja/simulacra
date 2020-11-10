from __future__ import annotations
from typing import List, Tuple, TYPE_CHECKING
from collections import defaultdict

import numpy as np

from config import *
from hues import COLOR
from tile import tile_graphic

if TYPE_CHECKING:
    from tcod.console import Console
    from graphic import Graphic
    from area import Area


def render_area_tiles(area: Area, consoles: Dict[str, Console]) -> None:

    DARKNESS = np.asarray(
        (0, COLOR['nero'], COLOR['black']),
        dtype=tile_graphic
        )

    consoles['ROOT'].clear()

    screen_view, world_view = area.camera.get_camera_view()

    # noinspection PyTypeChecker
    consoles['ROOT'].tiles_rgb[screen_view] = np.select(
        (area.area_model.visible[world_view],
         area.area_model.explored[world_view]),
        (area.area_model.tiles["light"][world_view],
         area.area_model.tiles["dark"][world_view]),
        DARKNESS
        )


def render_visible_entities(area: Area, consoles: Dict[str, Console]) -> None:
    visible_entities: Dict[Tuple[int, int], List[Graphic]] = defaultdict(list)

    cam_x, cam_y = area.camera.get_camera_pos()

    # Actors
    for obj in area.actor_model.actors:
        # Get each object's coordinates
        obj_x, obj_y = obj.location.x - cam_x, obj.location.y - cam_y

        # Ensure the object is within the stage view boundaries
        if not (0 <= obj_x < STAGE_PANEL_WIDTH and
                0 <= obj_y < STAGE_PANEL_HEIGHT):
            continue

        # Make sure the location is in the player's current FOV
        if not area.area_model.visible[obj.location.ij]:
            continue

        # Adjust the object background color
        obj.owner.bg = area.area_model.get_bg_color(obj_x, obj_y)
        print(obj.owner.location.xy)
        print(obj_x, obj_y)

        # Add the object to the list of visible entities
        visible_entities[obj_y, obj_x].append(obj.owner)

    # Items
    for (item_x, item_y), items in area.item_model.items.items():
        obj_x, obj_y = item_x - cam_x, item_y - cam_y
        if not (0 <= obj_x < STAGE_PANEL_WIDTH and
                0 <= obj_y < STAGE_PANEL_HEIGHT):
            continue
        if not area.area_model.visible[item_y, item_x]:
            continue

        visible_entities[obj_y, obj_x].extend(items)

    for ij, graphics in visible_entities.items():
        graphic = min(graphics)
        consoles['ROOT'].tiles_rgb[
            ["ch", "fg", "bg"]][ij] = graphic.char, graphic.color, graphic.bg


def update_fov(area: Area) -> None:
    if not area.player.location:
        return
    area.area_model.visible = tcod.map.compute_fov(
        transparency=area.area_model.tiles["transparent"],
        pov=area.player.location.ij,
        radius=10,
        light_walls=True,
        algorithm=tcod.FOV_RESTRICTIVE,
        )

    area.area_model.explored |= area.area_model.visible
