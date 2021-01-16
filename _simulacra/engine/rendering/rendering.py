"""ENGINE.RENDERING.Rendering"""
from __future__ import annotations

import time
from collections import defaultdict
from typing import TYPE_CHECKING, Dict, List, Tuple

import numpy as np

from config import *
from engine.tiles.tile import tile_graphic
from engine.rendering.noise import NoiseMachine
from engine.rendering.hues import COLOR

if TYPE_CHECKING:
    from tcod.console import Console

    from engine.areas import Area
    from .graphic import Graphic


noise_machine = NoiseMachine()

frames = 0
start_time = time.time()


def frame_count() -> float:
    """Count the number of frames since process start."""
    global frames
    frames += 1
    return frames


def elapsed_time() -> float:
    """Get the number of seconds since process start."""
    global start_time
    current_time = time.time()
    return current_time - start_time


def render_area_tiles(area: Area, consoles: Dict[str, Console]) -> None:
    _frames = frame_count()
    _elapsed = elapsed_time()
    # print(_elapsed)

    screen_view, world_view = area.camera.get_camera_view()
    consoles['ROOT'].clear()
    consoles['ROOT'].tiles_rgb[screen_view] = select_tile_mask(area, world_view)


def select_tile_mask(area: Area, world_view):
    UNKNOWN = np.asarray((0, COLOR['nero'], COLOR['black']), dtype=tile_graphic)

    if_visible = area.area_model.visible[world_view]
    if_explored = area.area_model.explored[world_view]
    lit_tiles = area.area_model.tiles["light"][world_view]
    unlit_tiles = area.area_model.tiles["dark"][world_view]

    condlist = (if_visible, if_explored)
    choicelist = (lit_tiles, unlit_tiles)

    #! (default, default, LIT,  LIT,  LIT,  LIT,  default, ...)
    #* (False,   False,   True, True, True, True, False,   ...)
    #? (LIT,     LIT,     LIT,  LIT,  LIT,  LIT,  LIT,     ...)

    return np.select(condlist=condlist, choicelist=choicelist, default=UNKNOWN)


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

    # Characters
    for ij, graphics in visible_entities.items():
        graphic = min(graphics)
        consoles['ROOT'].tiles_rgb[
            ["ch", "fg", "bg"]][ij] = graphic.char, graphic.color, graphic.bg


def render_visible_particles(area: Area, consoles: Dict[str, Console]) -> None:
    visible_particles: Dict[Tuple[int, int], List[Graphic]] = defaultdict(list)
    cam_x, cam_y = area.camera.get_camera_pos()

    # Grab the Tuple[int, int] keys and List[Particle] values
    for (p_x, p_y), particles in area.particle_model.particles.items():
        # Derive camera-adjusted x,y values
        obj_x, obj_y = p_x - cam_x, p_y - cam_y
        for particle in particles:
            particle.bg = area.area_model.get_bg_color(obj_x, obj_y)
        if not (0 <= obj_x < STAGE_PANEL_WIDTH and
                0 <= obj_y < STAGE_PANEL_HEIGHT):
            continue
        if not area.area_model.visible[p_y, p_x]:
            continue
        # Map the list of particles at the derived x,y to the visible dict
        visible_particles[obj_y, obj_x].extend(particles)

    # Pull the List[Particle] for key ij in visible particles
    for ij, graphics in visible_particles.items():
        # Only render the first item in the list
        graphic = min(graphics)
        # Render it to the console.
        consoles['ROOT'].tiles_rgb[
            ["ch", "fg", "bg"]][ij] = graphic.char, graphic.color, graphic.bg


def update_fov(area: Area) -> None:
    if not area.player.location:
        return
    area.area_model.visible = tcod.map.compute_fov(
        transparency=area.area_model.tiles["transparent"],
        pov=area.player.location.ij,
        radius=VIEW_RADIUS,
        light_walls=True,
        algorithm=tcod.FOV_RESTRICTIVE,
        )
    area.area_model.explored |= area.area_model.visible


def render_torch(area: Area, consoles: Dict[str, Console]) -> None:
    TORCH_RADIUS = 10
    SQUARED_TORCH_RADIUS = TORCH_RADIUS * TORCH_RADIUS

    # Derive the torch from noise based on current time.
    torch_t = time.perf_counter() * 5

    # Randomize the light position between -1.5 and 1.5
    cam_x, cam_y = area.camera.get_camera_pos()
    player_x = area.player.location.x
    player_y = area.player.location.y

    torch_x = (player_x + noise_machine.noise.get_point(torch_t) * 1.5)
    torch_y = (player_y + noise_machine.noise.get_point(torch_t + 11) * 1.5)

    # A little extra brightness, as a treat
    brightness = 0.2 * noise_machine.noise.get_point(torch_t + 17)

    # Squared distance using a mesh grid
    y, x = np.mgrid[:STAGE_WIDTH, :STAGE_HEIGHT]
    # Center the mesh grid on the target position
    x = (x.astype(np.float32) - torch_x)
    y = (y.astype(np.float32) - torch_y)

    # 2D squared distance array
    distance_squared = x ** 2 + y ** 2

    # Get the currently visible cells
    # (120, 120)
    fov = tcod.map.compute_fov(
        transparency = area.area_model.tiles["transparent"],
        pov=area.player.location.ij,
        radius=TORCH_RADIUS,
        light_walls=True,
        algorithm=tcod.FOV_RESTRICTIVE
        )
    visible = (distance_squared < SQUARED_TORCH_RADIUS) & \
            np.transpose(fov[:STAGE_HEIGHT, :STAGE_WIDTH], (1, 0))

    # Invert the values so that the center is the brightest point
    light = SQUARED_TORCH_RADIUS - distance_squared
    # Convert to a non-squared distance
    light /= SQUARED_TORCH_RADIUS
    # Add some randomness to the brightness
    light += brightness
    # Clamp the values
    light.clip(0, 1, out=light)
    # Set non-visible tiles to  d a r k n e s s
    light[~visible] = 0

    # Setup background colors for floating point math
    light_bg = area.area_model.tiles["light"]["bg"].astype(np.float16)
    dark_bg = area.area_model.tiles["dark"]["bg"].astype(np.float16)
    light_bg = light_bg[:STAGE_PANEL_HEIGHT, :STAGE_PANEL_WIDTH]
    dark_bg = dark_bg[:STAGE_PANEL_HEIGHT, :STAGE_PANEL_WIDTH]
    light = light[:STAGE_PANEL_WIDTH, :STAGE_PANEL_HEIGHT]

    consoles['ROOT'].tiles_rgb["bg"][:STAGE_PANEL_HEIGHT, :STAGE_PANEL_WIDTH] = (
        dark_bg + (light_bg - dark_bg) * \
        np.transpose(light[..., np.newaxis], (1, 0, 2)))

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

    # x, y, c = noise_machine.get_noise_at_point()

    _y = 0
    for line in logo:
        width = len(line)
        _x = 0
        if _y <= height:
            for char in line:
                if _x <= width:
                    if char == "#":  # SIMULACRA
                        consoles['ROOT'].print(
                            ((CONSOLE_WIDTH - width) // 2) + _x,
                            vertical_offset + _y,
                            chr(42),
                            fg=(noise_machine.get_noise_at_point(_x, _y),
                                noise_machine.get_noise_at_point(_x, _y) // 3,
                                noise_machine.get_noise_at_point(_x, _y)))

                    elif char == "@":  # BACKGROUND
                        consoles['ROOT'].print(
                            ((CONSOLE_WIDTH - width) // 2) + _x,
                            vertical_offset + _y,
                            chr(42),
                            fg=(20,
                                noise_machine.get_noise_at_point(_x, _y) // 4,
                                20))

                    elif char == "!":  # BORDER
                        consoles['ROOT'].print(
                            ((CONSOLE_WIDTH - width) // 2) + _x,
                            vertical_offset + _y,
                            chr(35),
                            fg=(noise_machine.get_noise_at_point(_x, _y),
                                noise_machine.get_noise_at_point(_x, _y) // 3,
                                noise_machine.get_noise_at_point(_x, _y)))

                    else:
                        consoles['ROOT'].print(
                            ((CONSOLE_WIDTH - width) // 2) + _x,
                            vertical_offset + _y,
                            " "
                            )

                    _x += 1
            _y += 1
