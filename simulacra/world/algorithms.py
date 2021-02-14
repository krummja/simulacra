from __future__ import annotations
from collections import deque
from simulacra.utils.geometry import Rect, Direction
from simulacra.core.options import *
import random



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
    tile_count = STAGE_WIDTH * STAGE_HEIGHT

    for (asset, threshold) in asset_list:
        assets.append(asset)
        thresholds.append(threshold)

    while tile_count > 0:
        threshold = thresholds.popleft()
        asset = assets.popleft()

        roll = random.randrange(0, 100)
        if roll < threshold:
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


class RandomBuilding:

    def __init__(self, ecs, tiles) -> None:
        self.ecs = ecs
        self.tiles = tiles
        self.width = random.randrange(5, 10)
        self.height = random.randrange(5, 10)
        self.x = random.randrange(10, STAGE_WIDTH - self.width - 10)
        self.y = random.randrange(10, STAGE_HEIGHT - self.height - 10)

        structure = Rect.from_edges(left = self.x,
                                    top = self.y,
                                    right = self.x + self.width,
                                    bottom = self.y + self.height)

        self.points = {}
        for (point, direction) in structure.iter_border():
            try:
                self.points[direction].append(point)
            except KeyError:
                self.points[direction] = [point]

        self.left = structure.left
        self.top = structure.top
        self.right = structure.right
        self.bottom = structure.bottom

    def build_doorway(self):
        sides = [Direction.up, Direction.down, Direction.left, Direction.right]
        side = sides[random.randrange(0, 4)]
        if side == Direction.up or side == Direction.down:
            codepoints = [0xE080, 0xE048, 0xE082]
            length = len(self.points[Direction.up])
            x_pos = random.randrange(self.left+0, self.left+length-3)

            if side == Direction.up:
                door_points = [(x_pos, self.top), (x_pos+1, self.top), (x_pos+2, self.top)]
            else:
                door_points = [(x_pos, self.bottom), (x_pos+1, self.bottom), (x_pos+2, self.bottom)]

        if side == Direction.left or side == Direction.right:
            codepoints = [0xE044, 0xE048, 0xE064]
            length = len(self.points[Direction.left])
            y_pos = random.randrange(self.top+0, self.top+length-3)
            door_points = [y_pos, y_pos+2]
            if side == Direction.left:
                door_points = [(self.left, y_pos), (self.left, y_pos+1), (self.left, y_pos+2)]
            else:
                door_points = [(self.right, y_pos), (self.right, y_pos+1), (self.right, y_pos+2)]

        data = list(zip(codepoints, door_points))

    def build_walls(self):

        self.points[Direction.up_left] = self.ecs.engine.create_entity()
        self.points[Direction.up_left].add('Renderable', {'codepoint': 0xE040})
        self.points[Direction.up_left].add('Position', {'x': self.left, 'y': self.top})

        self.points[Direction.up_right] = self.ecs.engine.create_entity()
        self.points[Direction.up_right].add('Renderable', {'codepoint': 0xE043})
        self.points[Direction.up_right].add('Position', {'x': self.right, 'y': self.top})

        self.points[Direction.down_left] = self.ecs.engine.create_entity()
        self.points[Direction.down_left].add('Renderable', {'codepoint': 0xE070})
        self.points[Direction.down_left].add('Position', {'x': self.left, 'y': self.bottom})

        self.points[Direction.down_right] = self.ecs.engine.create_entity()
        self.points[Direction.down_right].add('Renderable', {'codepoint': 0xE073})
        self.points[Direction.down_right].add('Position', {'x': self.right, 'y': self.bottom})

        for corner in [
            self.points[Direction.up_left],
            self.points[Direction.up_right],
            self.points[Direction.down_left],
            self.points[Direction.down_right],
            ]:
            corner.add('Blocker', {})
            corner.add('Opaque', {})

            (x, y) = corner['Position'].xy
            self.tiles[x][y].entity = corner

        for point in self.points[Direction.up] + self.points[Direction.down]:
            x, y = point
            point = self.ecs.engine.create_entity()
            point.add('Renderable', {'codepoint': 0xE041})
            point.add('Position', {'x': x, 'y': y})
            point.add('Blocker', {})
            point.add('Opaque', {})
            self.tiles[x][y].entity = point

        for point in self.points[Direction.left] + self.points[Direction.right]:
            x, y = point
            point = self.ecs.engine.create_entity()
            point.add('Renderable', {'codepoint': 0xE050})
            point.add('Position', {'x': x, 'y': y})
            point.add('Blocker', {})
            point.add('Opaque', {})
            self.tiles[x][y].entity = point


