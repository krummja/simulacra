from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

from engine.tile import Tile
from engine.hues import COLOR


WALL_01 = Tile(
    move_cost=0,
    transparent=False,
    char=130,
    fg=COLOR['roman coffee'],
    bg=COLOR['eclipse']
)

WALL_02 = Tile(
    move_cost=0,
    transparent=False,
    char=131,
    fg=COLOR['roman coffee'],
    bg=COLOR['eclipse']
)

BARE_WALL_01 = Tile(
    move_cost=0,
    transparent=False,
    char=132,
    fg=COLOR['roman coffee'],
    bg=COLOR['eclipse']
)

BARE_WALL_02 = Tile(
    move_cost=0,
    transparent=False,
    char=135,
    fg=COLOR['roman coffee'],
    bg=COLOR['eclipse']
)

DOOR_01 = Tile(
    move_cost=0,
    transparent=False,
    char=133,
    fg=COLOR['chocolate'],
    bg=COLOR['eclipse']
)

CORNER = Tile(
    move_cost=0,
    transparent=False,
    char=130,
    fg=COLOR['roman coffee'],
    bg=COLOR['eclipse']
)

FLOOR = Tile(
    move_cost=1,
    transparent=True,
    char=127,
    fg=COLOR['eclipse'],
    bg=COLOR['charcoal']
)

TREE = Tile(
    move_cost=0,
    transparent=False,
    char=140,
    fg=COLOR['kelly green'],
    bg=COLOR['black']
)

BARREL_01 = Tile(
    move_cost=0,
    transparent=False,
    char=134,
    fg=COLOR['chocolate'],
    bg=COLOR['eclipse']
)

FLOOR_GRATE_01 = Tile(
    move_cost=1,
    transparent=True,
    char=138,
    fg=COLOR['eclipse'],
    bg=COLOR['dim gray'],
)

CLUTTER_01 = Tile(
    move_cost=1,
    transparent=True,
    char=139,
    fg=COLOR['eclipse'],
    bg=COLOR['dim gray'],
)

WINDOW_01 = Tile(
    move_cost=0,
    transparent=True,
    char=141,
    fg=COLOR['slate blue'],
    bg=COLOR['eclipse']
)