from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING, Optional

from engine.tile import Tile
from engine.hues import COLOR
from content.tiles import font_map


styles = {
    'bare': {
        'foreground': COLOR['peru'],
        'background': COLOR['nero']
    },
    'ornate': {
        # 'foreground': COLOR[''],
        # 'background': COLOR['']
    }
}


floors = {
    'bare': {
        'blank': Tile(
            move_cost=1,
            transparent=True,
            char=font_map['blank'], 
            fg=styles['bare']['foreground'], 
            bg=styles['bare']['background'],
        ),
    },
    # 'ornate': {
    #     'blank': Tile(
    #         move_cost=1,
    #         transparent=True,
    #         char=font_map['blank'], 
    #         fg=styles['ornate']['foreground'], 
    #         bg=styles['ornate']['background'],
    #     ),
    # }
}