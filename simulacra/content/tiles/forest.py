from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING, Optional

from engine.tile import Tile
from engine.hues import COLOR
from content.tiles import font_map


styles = {
    'basic_forest': {
        'ground': {
            'foreground': COLOR['eden'],
            'background': COLOR['black']
        },
        'trees': {
            'foreground': COLOR['kelly green'],
            'background': COLOR['eden']
        },
        'rocks': {
            'foreground': COLOR['eden'],
            'background': COLOR['dim gray'],
        }
    }
}


basic_forest = {
    'ground': Tile(
        move_cost=1,
        transparent=True,
        char=font_map['blank'],
        fg=styles['basic_forest']['ground']['foreground'],
        bg=styles['basic_forest']['ground']['background']
    ),
    'tree_01': Tile(
        move_cost=0,
        transparent=False,
        char=font_map['tree_01'],
        fg=styles['basic_forest']['trees']['foreground'],
        bg=styles['basic_forest']['trees']['background'],
    ),
    'rock_01': Tile(
        move_cost=0,
        transparent=False,
        char=font_map['rock_01'],
        fg=styles['basic_forest']['rocks']['foreground'],
        bg=styles['basic_forest']['rocks']['background'],
    ),
    'rock_02': Tile(
        move_cost=0,
        transparent=False,
        char=font_map['rock_02'],
        fg=styles['basic_forest']['rocks']['foreground'],
        bg=styles['basic_forest']['rocks']['background'],
    ),
    'clutter_01': Tile(
        move_cost=1,
        transparent=True,
        char=font_map['clutter'],
        fg=styles['basic_forest']['rocks']['foreground'],
        bg=styles['basic_forest']['rocks']['background']
    )
}