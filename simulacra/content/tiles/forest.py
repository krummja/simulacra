from __future__ import annotations  # type: ignore

from engine.tile import Tile
from engine.hues import COLOR
from content.tiles import font_map


styles = {
    'basic_forest': {
        'ground_01': {
            'foreground': COLOR['rain forest'],
            'background': COLOR['black']
            },
        'ground_02': {
            'foreground': COLOR['olive'],
            'background': COLOR['black']
            },
        'trees': {
            'foreground': COLOR['ever green'],
            'background': COLOR['rain forest']
            },
        'rocks': {
            'foreground': COLOR['rain forest'],
            'background': COLOR['nero'],
            },
        'clutter': {
            'foreground': COLOR['rain forest'],
            'background': COLOR['eclipse'],
            },
        'gravel': {
            'foreground': COLOR['rain forest'],
            'background': COLOR['bisque'],
            },
        'flowers_01': {
            'foreground': COLOR['rain forest'],
            'background': COLOR['deep pink'],
            },
        'flowers_02': {
            'foreground': COLOR['rain forest'],
            'background': COLOR['cyan'],
            }
        }
    }

basic_forest = {
    'ground_01': Tile(
        move_cost=1,
        transparent=True,
        char=font_map['blank'],
        color=styles['basic_forest']['ground_01']['foreground'],
        bg=styles['basic_forest']['ground_01']['background']
        ),
    'ground_02': Tile(
        move_cost=1,
        transparent=True,
        char=font_map['blank'],
        color=styles['basic_forest']['ground_02']['foreground'],
        bg=styles['basic_forest']['ground_02']['background']
        ),
    'gravel_01': Tile(
        move_cost=1,
        transparent=True,
        char=font_map['gravel_01'],
        color=styles['basic_forest']['gravel']['foreground'],
        bg=styles['basic_forest']['gravel']['background'],
        ),
    'gravel_02': Tile(
        move_cost=1,
        transparent=True,
        char=font_map['gravel_02'],
        color=styles['basic_forest']['gravel']['foreground'],
        bg=styles['basic_forest']['gravel']['background'],
        ),
    'tree_01': Tile(
        move_cost=0,
        transparent=False,
        char=font_map['tree_01'],
        color=styles['basic_forest']['trees']['foreground'],
        bg=styles['basic_forest']['trees']['background'],
        ),
    'rock_01': Tile(
        move_cost=0,
        transparent=False,
        char=font_map['rock_01'],
        color=styles['basic_forest']['rocks']['foreground'],
        bg=styles['basic_forest']['rocks']['background'],
        ),
    'rock_02': Tile(
        move_cost=0,
        transparent=False,
        char=font_map['rock_02'],
        color=styles['basic_forest']['rocks']['foreground'],
        bg=styles['basic_forest']['rocks']['background'],
        ),
    'clutter_01': Tile(
        move_cost=1,
        transparent=True,
        char=font_map['clutter'],
        color=styles['basic_forest']['clutter']['foreground'],
        bg=styles['basic_forest']['clutter']['background']
        ),
    'paving_stones_01': Tile(
        move_cost=1,
        transparent=True,
        char=font_map['paving_stones_01'],
        color=styles['basic_forest']['gravel']['foreground'],
        bg=styles['basic_forest']['gravel']['background'],
        ),
    'paving_stones_02': Tile(
        move_cost=1,
        transparent=True,
        char=font_map['paving_stones_02'],
        color=styles['basic_forest']['gravel']['foreground'],
        bg=styles['basic_forest']['gravel']['background'],
        ),
    'flowers_01': Tile(
        move_cost=1,
        transparent=True,
        char=font_map['flowers_01'],
        color=styles['basic_forest']['flowers_01']['foreground'],
        bg=styles['basic_forest']['flowers_01']['background'],
        ),
    'flowers_02': Tile(
        move_cost=1,
        transparent=True,
        char=font_map['flowers_01'],
        color=styles['basic_forest']['flowers_02']['foreground'],
        bg=styles['basic_forest']['flowers_02']['background'],
        )
    }
