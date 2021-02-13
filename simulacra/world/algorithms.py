from __future__ import annotations
from typing import TYPE_CHECKING
from collections import deque
from simulacra.core.options import *

import random

if TYPE_CHECKING:
    from .grid import Tile


def random_grass(ecs, tiles, threshold, width=STAGE_WIDTH, height=STAGE_HEIGHT):
    for x in range(width):
        for y in range(height):
            tile = tiles[x][y]
            if tile.UNFORMED:
                real_tile = ecs.engine.create_entity()
                roll = random.randrange(0, 100)

                if roll < threshold:
                    ecs.engine.prefabs.apply_to_entity(
                        real_tile, 'Grass Tile 1', {'Position': {'x': x, 'y': y}})
                else:
                    ecs.engine.prefabs.apply_to_entity(
                        real_tile, 'Grass Tile 2', {'Position': {'x': x, 'y': y}})
                tile.entity = real_tile
    return tiles


def random_assets(ecs, tiles, asset_list):

    thresholds = deque([])
    assets = deque([])
    queue = deque([])

    tile_count = STAGE_WIDTH * STAGE_HEIGHT

    for (asset, threshold) in asset_list:
        assets.append(asset)
        thresholds.append(threshold)

    # for x in range(STAGE_WIDTH):
    #     for y in range(STAGE_HEIGHT):
    #         tile = tiles[x][y]
    #         queue.append(tile)

    # While there's still tiles to process...
    while tile_count > 0:

        # Roll
        roll = random.randrange(0, 100)

        # Grab a threshold and an asset
        threshold = thresholds.popleft()
        asset = assets.popleft()

        # If the roll is above the threshold...
        if roll < threshold:
            # Success, grab a tile
            # tile = queue.popleft()
            x = random.randrange(0, STAGE_WIDTH)
            y = random.randrange(0, STAGE_HEIGHT)
            tile = tiles[x][y]
            if tile.UNFORMED:
                tile_count -= 1
                real_tile = ecs.engine.create_entity()
                tile.entity = real_tile
                ecs.engine.prefabs.apply_to_entity(
                    tile.entity, asset, {'Position': {'x': x, 'y': y}})

        thresholds.append(threshold)
        assets.append(asset)

    return tiles
