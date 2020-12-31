from __future__ import annotations
from typing import List, Tuple, Optional

import random
import numpy as np
import tcod

from content.factories.factory_service import FactoryService
from content.tiles.tile_defs import all_tiles, color_list
from engine.areas.area import Area
from engine.geometry import Rect


class AreaFactory:
    """Build a new Area."""

    tile_factory = FactoryService().tile_factory

    def __init__(
            self,
            area: Area,
            *,
            max_rooms: int,
            min_size: int,
            max_size: int
        ) -> None:
        self.area = area
        self.max_rooms = max_rooms
        self.min_room_size = min_size
        self.max_room_size = max_size
        self.rooms = []
        self.tiles = self.area.area_model.tiles

    def generate(
            self,
            floor: Optional[str] = 'bare_floor',
            wall: Optional[str] = 'evergreen_1'
        ) -> Area:
        self._generate_rooms(floor, wall)
        self._place_prefab('prefab_1')
        return self.area

    def _generate_rooms(
            self,
            floor: Optional[str] = 'bare_floor',
            wall: Optional[str] = 'bare_wall'
        ) -> Area:

        # Set everything on the map to the area's default wall type.
        self.tiles[...] = self.tile_factory.build(wall,
                                                  color=(100, 150, 30),
                                                  bg=(25, 40, 40))

        # Randomize things a bit, including adding some floor tiles.
        self._roll_asset('grass_1',
                         colors=[(95, 150, 95),
                                 (90, 160, 60),
                                 (100, 150, 30)],
                         bgs=[(25, 40, 40)],
                         threshold=30)

        self._roll_asset('grass_2',
                         colors=[(95, 150, 95),
                                 (90, 160, 60),
                                 (100, 150, 30)],
                         bgs=[(25, 40, 40)],
                         threshold=30)

        # Start building rooms.
        for _ in range(self.max_rooms):
            w = random.randint(self.min_room_size, self.max_room_size)
            h = random.randint(self.min_room_size, self.max_room_size)
            x = random.randint(0, self.area.width - w - 1)
            y = random.randint(0, self.area.height - h - 1)

            new_room: Rect = Rect.from_edges(left=x, top=y, right=x+w, bottom=y+h)

            # Check for intersections and try again if found.
            if any(new_room.intersects(other) for other in self.rooms):
                continue

            # Connect a new room to an existing room.
            self._generate_tunnels(new_room)

            # Clear the inner portion of the room to the default floor type.
            print(new_room.inner)
            self.tiles.T[new_room.inner] = self.tile_factory.build(
                floor, color=(25, 40, 40)
                )

            # Add the new room to the area's room list.
            self.rooms.append(new_room)

        return self.area

    def _generate_tunnels(self, new_room: Rect) -> Area:

        if self.rooms:

            if random.randint(0, 99) < 80:
                other_room = min(self.rooms, key=new_room.distance_to)
            else:
                other_room = self.rooms[-1]

            t_start = new_room.center
            t_end = other_room.center

            if random.randint(0, 1):
                t_middle = t_start[0], t_end[1]
            else:
                t_middle = t_end[0], t_start[1]

            self.tiles.T[
                tcod.line_where(*t_start, *t_middle)
                ] = self.tile_factory.build('dirt_1', color=(180, 100, 55))

            self.tiles.T[
                tcod.line_where(*t_middle, *t_end)
                ] = self.tile_factory.build('dirt_1', color=(180, 100, 55))

        return self.tiles

    def _assemble_prefab(self, prefab_id):
        # TODO: This is an unholy abomination that needs to be banished from this class

        # Load the tilemap, foreground color, and background color CSV files
        tilemap_file = 'simulacra/content/areas/prefabs/' + prefab_id + '_Tilemap.csv'
        color_file = 'simulacra/content/areas/prefabs/' + prefab_id + '_Foreground.csv'
        bg_file = 'simulacra/content/areas/prefabs/' + prefab_id + '_Background.csv'

        # Turn them into arrays
        tilemap_array = np.genfromtxt(tilemap_file, delimiter=',', dtype=np.int)
        color_array = np.genfromtxt(color_file, delimiter=',', dtype=np.int)
        bg_array = np.genfromtxt(bg_file, delimiter=',', dtype=np.int)

        # Store the shape... we'll use it in a bit
        prefab_shape = tilemap_array.shape

        # Destructure into lists
        tilemap_array = [[tile_id for tile_id in row] for row in tilemap_array]
        color_array = [[color_id for color_id in row] for row in color_array]
        bg_array = [[bg_id for bg_id in row] for row in bg_array]

        # Convert TILE_ID to CHAR_ID
        tile_to_char = lambda i: self.tile_factory.convert_to_char_id(i)
        prefab_array = np.array([
            [tile_to_char(tile_id) for tile_id in row] for row in tilemap_array
            ])

        # Map each CHAR_ID to a TILE_ID
        uid_lookup = self.tile_factory.convert_to_id_dict(tile_dict=all_tiles)
        prefab_array = np.array([[
                (lambda i: uid_lookup[i])(char_id) for char_id in row
                ] for row in prefab_array])

        # Map COLOR_IDs and BG_IDs to actual color values:
        color_array = np.array([[color_list[i] for i in row] for row in color_array])
        bg_array = np.array([[color_list[i] for i in row] for row in bg_array])

        # Compose all values into a final array structure
        def compose(prefab, color, bg):
            tile_id_list = prefab.flatten().tolist()
            color_id_list = []
            bg_id_list = []

            for row in color:
                for color in row:
                    color_id_list.append(tuple(color))

            for row in bg:
                for bg in row:
                    bg_id_list.append(tuple(bg))

            _composition = []
            for i in range(len(tile_id_list)):
                definition = (tile_id_list[i], color_id_list[i], bg_id_list[i])
                _composition.append(definition)

            return np.array(_composition).reshape(*prefab_shape, 3)

        prefab_array = compose(prefab_array, color_array, bg_array)

        # FINALLY, map each prefab_array tuple into a new Tile instance
        _tile_list = []
        for y in range(prefab_array.shape[0]):
            for x in range(prefab_array.shape[1]):
                uid = prefab_array[y, x][0]
                color = prefab_array[y, x][1]
                bg = prefab_array[y, x][2]
                _tile_list.append(self.tile_factory.build(uid, color=color, bg=bg))

        return np.array(_tile_list).reshape(prefab_shape)

    def _place_prefab(self, prefab_id) -> Area:
        prefab = self._assemble_prefab(prefab_id)
        width = prefab.shape[0]
        height = prefab.shape[1]
        self.tiles[0:height, 0:width] = prefab

    def _process_ascii_prefab(
            self,
            base: np.ndarray,
            rules: List[Tuple[str, str]] = None,
        ) -> Area:
        """Iterate through an 1D array consisting of char strings and replace
        for Tile instances based on a supplied list of rewrite rules.

        - `base` is the input array of ASCII characters.
        - `rules` is a list of (ASCII character, tile UID) rewrite rules"""
        if rules is None:
            rules = []

        height: int = base.shape[0]
        base_row: int = 0

        for line in base:
            width: int = len(line)
            base_col: int = 0
            if base_row <= height:
                for char in line:
                    if base_col <= width:
                        for rule in rules:
                            if char == rule[0]:
                                self.tiles[
                                    base_row + 5,
                                    base_col + 5
                                    ] = self.tile_factory.build(rule[1])
                        base_col += 1
                base_row += 1
        return self.tiles

    def _roll_asset(
            self,
            template: str,
            colors = None,
            bgs = None,
            threshold: int = 50,
            x: int = None,
            y: int = None
        ) -> Area:
        if colors is None:
            colors = [(255, 255, 255)]
        if bgs is None:
            bgs = [(0, 0, 0)]

        _x_range = range(self.area.width) if x is None else x
        _y_range = range(self.area.height) if y is None else y

        _x = [x for x in range(self.area.width)] if x is None else [x]
        _y = [y for y in range(self.area.height)] if y is None else [y]

        for x in _x:
            for y in _y:
                roll = random.randint(0, 100)
                if roll < threshold:
                    color = colors[random.randint(0, len(colors)-1)]
                    bg = bgs[random.randint(0, len(bgs)-1)]
                    self.tiles[y, x] = self.tile_factory.build(template, color, bg)
        return self.area

    def _generate_bsp(self, width: int, height: int):
        bsp = tcod.bsp.BSP(x=0, y=0, width=width, height=height)
        bsp.split_recursive(
            depth=10,
            min_width=15,
            min_height=15,
            max_horizontal_ratio=2.0,
            max_vertical_ratio=2.0,
            )

        for node in bsp.pre_order():
            if node.children:
                pass
                # node1, node2 = node.children
                # Connect Node1, Node2
            else:
                room = Rect.from_edges(
                    left=node.x,
                    top=node.y,
                    right=node.w,
                    bottom=node.h
                    )
                yield room

    def _generate_cellular(self):
        pass

    @property
    def start_tile(self):
        return self.rooms[0].center
