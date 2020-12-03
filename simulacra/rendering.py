from __future__ import annotations
from typing import Dict, List, Tuple, TYPE_CHECKING
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

        # Add the object to the list of visible entities
        visible_entities[obj_y, obj_x].append(obj.owner)

    # Items
    for (item_x, item_y), items in area.item_model.items.items():
        obj_x, obj_y = item_x - cam_x, item_y - cam_y
        for item in items:
            item.bg = area.area_model.get_bg_color(obj_x, obj_y)
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

def draw_frame(consoles: Dict[str, Console]) -> None:
    outer_frame_color = (200, 155, 155)
    inner_frame_color = (100, 0, 0)
    
    consoles['ROOT'].print_box(
        x=1, y=1, 
        width=4, height=4, 
        string="****************",
        fg=inner_frame_color)
    
    consoles['ROOT'].print_box(
        x=CONSOLE_WIDTH-5, y=1, 
        width=4, height=4, 
        string="****************",
        fg=inner_frame_color)
    
    consoles['ROOT'].print_box(
        x=1, y=CONSOLE_HEIGHT-5, 
        width=4, height=4, 
        string="****************",
        fg=inner_frame_color)
    
    consoles['ROOT'].print_box(
        x=CONSOLE_WIDTH-5, y=CONSOLE_HEIGHT-5, 
        width=4, height=4, 
        string="****************",
        fg=inner_frame_color)
    
    outer_vertical = "#" * CONSOLE_HEIGHT
    outer_horizontal = "#" * CONSOLE_WIDTH
    
    consoles['ROOT'].print_box(
        x=0, y=0,
        width=CONSOLE_WIDTH-1, height=1,
        string=outer_horizontal,
        fg=outer_frame_color)
    
    consoles['ROOT'].print_box(
        x=0, y=CONSOLE_HEIGHT-1,
        width=CONSOLE_WIDTH-1, height=1,
        string=outer_horizontal,
        fg=outer_frame_color)

    consoles['ROOT'].print_box(
        x=0, y=0,
        width=1, height=CONSOLE_HEIGHT,
        string=outer_vertical,
        fg=outer_frame_color)    
    
    consoles['ROOT'].print_box(
        x=CONSOLE_WIDTH-1, y=0,
        width=1, height=CONSOLE_HEIGHT,
        string=outer_vertical,
        fg=outer_frame_color) 
    
    inner_vertical = "*" * (CONSOLE_HEIGHT-8)
    inner_horizontal = "*" * (CONSOLE_WIDTH-8)
    consoles['ROOT'].print_box(
        x=1, y=5,
        width=1, height=CONSOLE_HEIGHT-8,
        string=inner_vertical,
        fg=inner_frame_color)
    
    consoles['ROOT'].print_box(
        x=CONSOLE_WIDTH-2, y=5,
        width=1, height=CONSOLE_HEIGHT-8,
        string=inner_vertical,
        fg=inner_frame_color)
    
    consoles['ROOT'].print_box(
        x=5, y=1,
        width=CONSOLE_WIDTH-8, height=1,
        string=inner_horizontal,
        fg=inner_frame_color)
    
    consoles['ROOT'].print_box(
        x=5, y=CONSOLE_HEIGHT-2,
        width=CONSOLE_WIDTH-8, height=1,
        string=inner_horizontal,
        fg=inner_frame_color)


def draw_logo(consoles: Dict[str, Console]) -> None:
    logo = np.array([
        "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",
        "!!                                                                              !!",
        "!  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  !",
        "! @@          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ !",
        "! @  ########  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ !",
        "! @ ########## @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ !",
        "! @ ##      ##   @@@@@                   @@@@@   @@              @@@@@@@   @@@@@ !",
        "! @ ##  @@ #####  @@@  ###### #### ##### @@@@  # @  ############  @@@@@  # @@@@@ !",
        "! @ ###  @  #####  @@@  #####  ###  ###  @@@  ##   ##### ######## @@@@  ## @@@@@ !",
        "! @  ###  @ ## ###  @  ### ##   ##  ##  @@@  ###  ###  # ##    ## @@@  ### @@@@@ !",
        "! @@  ###   ## ####   #### ## @ ##  ## @@@  #### ###     ##   ### @@  #### @@@@@ !",
        "! @@@  ###  ## ##### ##### ## @ ##  ## @@  ##### ##  @@@ ## ####  @  ##### @@@@@ !",
        "! @@@@  ### ## ## ##### ## ##   ###### @  ### ## ## @@@@ ######  @  ### ## @@@@@ !",
        "! @@@@@  ## ## ##  ###  ## ### #### ##   ###  ## ## @@@@ ##  ###   ###  ## @@@@@ !",
        "! @     ### ## ##   #   ##  ######  ##  ###   ## ##  @@  ##   ##  ###   ##   @@@ !",
        "! @ ######  ##### @    ###  ######  ##  ############ @  ### @ ##  ########## @@@ !",
        "! @ #####   ##### @@@ #####   # ## ####  ######## ##   #### @  ##  ########    @ !",
        "! @ #     @ ##    @@@       @     ######        ######        ####          ## @ !",
        "! @   @@@@@ ####  @@@@@@@@@@@@@@@    ######    ##########    #########  #####  @ !",
        "! @@@@@@@@@ ###  @@@@@@@@@@@@@@@@@@@   ###########   ###########  ##########  @@ !",
        "! @@@@@@@@@ ##  @@@@@@@@@@@@@@@@@@@@@@    ######        ######       ####    @@@ !",
        "! @@@@@@@@@ #  @@@@@@@@@@@@@@@@@@@@@@@@@@        @@@@@@        @@@@@      @@@@@@ !",
        "! @@@@@@@@@   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ !",
        "!  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  !",
        "!!                                                                              !!",
        "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",
        ])

    logo = np.array([list(line) for line in logo])
    height = logo.shape[0]

    vertical_offset: int = 4

    row_index = 0
    for line in logo:
        width = len(line)
        col_index = 0
        if row_index <= height:
            for char in line:
                if col_index <= width:
                    if char == "#":
                        consoles['ROOT'].print(
                            ((CONSOLE_WIDTH - width) // 2) + col_index,
                            vertical_offset + row_index,
                            chr(42),
                            fg=(200, 100, 155)
                            )

                    elif char == "@":
                        consoles['ROOT'].print(
                            ((CONSOLE_WIDTH - width) // 2) + col_index,
                            vertical_offset + row_index,
                            chr(42),
                            fg=(100, 0, 0)
                            )

                    elif char == "!":
                        consoles['ROOT'].print(
                            ((CONSOLE_WIDTH - width) // 2) + col_index,
                            vertical_offset + row_index,
                            chr(35),
                            fg=(200, 155, 155)
                            )

                    else:
                        consoles['ROOT'].print(
                            ((CONSOLE_WIDTH - width) // 2) + col_index,
                            vertical_offset + row_index,
                            " "
                            )

                    col_index += 1
            row_index += 1