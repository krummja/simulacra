from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

from engine.tile import Tile
from engine.hues import COLOR


WALL_01 = Tile(
    move_cost=0,
    transparent=False,
    char=130,
    fg=COLOR['rosy brown'],
    bg=COLOR['eclipse']
)

WALL_02 = Tile(
    move_cost=0,
    transparent=False,
    char=131,
    fg=COLOR['roman coffee'],
    bg=COLOR['eclipse']
)

EMBOSSED_FLOOR_01 = Tile(
    move_cost=1,
    transparent=True,
    char=135,
    fg=COLOR['peru'],
    bg=COLOR['nero']
)

EMBOSSED_FLOOR_02 = Tile(
    move_cost=1,
    transparent=True,
    char=137,
    fg=COLOR['peru'],
    bg=COLOR['nero']
)

EMBOSSED_WALL_01 = Tile(
    move_cost=0,
    transparent=False,
    char=132,
    fg=COLOR['light slate gray'],
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

FLOOR_01 = Tile(
    move_cost=1,
    transparent=True,
    char=127,
    fg=COLOR['eden'],
    bg=COLOR['charcoal']
)

FLOOR_02 = Tile(
    move_cost=1,
    transparent=True,
    char=127,
    fg=COLOR['tan'],
    bg=COLOR['charcoal']
)

TREE = Tile(
    move_cost=0,
    transparent=False,
    char=140,
    fg=COLOR['kelly green'],
    bg=COLOR['eden']
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
    fg=COLOR['tan'],
    bg=COLOR['dim gray'],
)

CLUTTER_01 = Tile(
    move_cost=1,
    transparent=True,
    char=139,
    fg=COLOR['eden'],
    bg=COLOR['eclipse'],
)

WINDOW_01 = Tile(
    move_cost=0,
    transparent=True,
    char=141,
    fg=COLOR['light blue'],
    bg=COLOR['eclipse']
)

ALTAR_01 = Tile(
    move_cost=0,
    transparent=True,
    char=142,
    fg=COLOR['mint cream'],
    bg=COLOR['gray']
)

BOULDER_01 = Tile(
    move_cost=0,
    transparent=False,
    char=143,
    fg=COLOR['eden'],
    bg=COLOR['gray'],
)

BOULDER_02 = Tile(
    move_cost=0,
    transparent=False,
    char=144,
    fg=COLOR['eden'],
    bg=COLOR['gray'],
)

CLEAR = Tile(
    move_cost=1,
    transparent=True,
    char=127,
    fg=COLOR['eden'],
    bg=COLOR['gray']
)