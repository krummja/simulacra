from __future__ import annotations
from typing import Optional, TYPE_CHECKING

import numpy as np
import random
import tcod

from area import Area
from factories.factory_service import FactoryService
from geometry import *
from generators.cellular_automata import *
from data.tile_defs import *
from room import Room


class AreaFactory:

    tile_factory = FactoryService().tile_factory

    def __init__(
            self, 
            area: Area, 
            max_rooms: int, 
            max_size: int, 
            min_size: int
        ) -> None:
        self.area = area
        self.max_rooms = max_rooms
        self.max_room_size = max_size
        self.min_room_size = min_size
        self.rooms = []
        self.tiles = self.area.area_model.tiles
        
    def generate(
            self, 
            floor: Optional[str] = 'bare_floor', 
            wall: Optional[str] = 'evergreen_1'
        ) -> Area:
        self._generate_rooms(floor, wall)
        self._place_prefab('simulacra/generators/prefab_1.csv')
        return self.area

    def _generate_rooms(
            self, 
            floor: Optional[str] = 'bare_floor', 
            wall: Optional[str] = 'evergreen_1'
        ) -> Area:

        # Set everything on the map to the area's default wall type.
        self.tiles[...] = self.tile_factory.build(wall)
        
        # Randomize things a bit, including adding some floor tiles.
        self.roll_asset('grass_1', threshold=30)
        self.roll_asset('grass_2', threshold=30)
        self.roll_asset('evergreen_2', threshold=30)
        self.roll_asset('evergreen_3', threshold=30)
        self.roll_asset(floor, threshold=20)
              
        # Start building rooms.
        for _ in range(self.max_rooms):
            w = random.randint(self.min_room_size, self.max_room_size)
            h = random.randint(self.min_room_size, self.max_room_size)
            x = random.randint(0, self.area.width - w - 1)
            y = random.randint(0, self.area.height - h - 1)
            new_room: Room = Room(x, y, w, h)

            # Check for intersections and try again if found.
            if any(new_room.intersects(other) for other in self.rooms):
                continue
            
            # Connect a new room to an existing room.
            self._generate_tunnels(new_room)
            
            # Clear the inner portion of the room to the default floor type.
            self.tiles.T[new_room.inner] = self.tile_factory.build(floor)
            
            # Add the new room to the area's room list.
            self.rooms.append(new_room)

        return self.area
    
    def _generate_tunnels(self, new_room: Room) -> Area:
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
            self.tiles.T[tcod.line_where(*t_start, *t_middle)] = self.tile_factory.build('dirt_path')
            self.tiles.T[tcod.line_where(*t_middle, *t_end)] = self.tile_factory.build('dirt_path')
            
        return self.tiles

    def _assemble_prefab(self, prefab_file):
        
        # 1) Convert CSV to NumPy Array
        csv_array = np.genfromtxt(prefab_file, delimiter=',', dtype=np.int32)
        csv_array = [[tile_id for tile_id in row] for row in csv_array]
        
        # 2) Convert TILE_ID to CHAR_ID
        tile_to_char = lambda i: self.tile_factory.convert_to_char_id(i)
        prefab_array = np.array([[tile_to_char(tile_id) for tile_id in row] for row in csv_array])
        
        # 3) Map each CHAR_ID to a TILE_ID
        uid_lookup = self.tile_factory.convert_to_id_dict(tile_dict=all_tiles)
        prefab_array = np.array([[(lambda i: uid_lookup[i])(char_id) for char_id in row] for row in prefab_array])
        
        # 4) Map each TILE_UID to a Tile instance
        map_to_tile = lambda i: self.tile_factory.build(i)
        prefab_array = np.array([[map_to_tile(uid) for uid in row] for row in prefab_array])
        
        return prefab_array
    
    def _place_prefab(self, prefab_file) -> Area:
        prefab = self._assemble_prefab(prefab_file)
        width = prefab.shape[0]
        height = prefab.shape[1]
        self.tiles[0:height, 0:width] = prefab
        
    def _process_ascii_prefab(
            self,
            base: ndarray,
            rules: List[Tuple[str, str]] = [],
            tilemap: bool = False
        ) -> Area:
        """Iterate through an 1D array consisting of char strings and replace
        for Tile instances based on a supplied list of rewrite rules.
        
        - `base` is the input array of ASCII characters.
        - `rules` is a list of (ASCII character, tile UID) rewrite rules"""
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

    def roll_asset(
            self, 
            template: str,
            multi: bool = False,
            threshold: int = 50, 
            x: int = None, 
            y: int = None
        ) -> Area:
        _x_range = range(self.area.width) if x is None else x
        _y_range = range(self.area.height) if y is None else y

        _x = [x for x in range(self.area.width)] if x is None else [x]
        _y = [y for y in range(self.area.height)] if y is None else [y]

        for x in _x:
            for y in _y:
                roll = random.randint(0, 100)
                if roll < threshold:
                    if multi:
                        self.tiles[y, x] = self.tile_factory.build(template + '_bot')
                        self.tiles[y-1, x] = self.tile_factory.build(template + '_top')
                    else: 
                        self.tiles[y, x] = self.tile_factory.build(template)
        return self.area
    
    @property
    def start_tile(self):
        return self.rooms[0].center