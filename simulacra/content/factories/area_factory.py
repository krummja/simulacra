from __future__ import annotations
from typing import List, Tuple, Optional, Generator

from enum import Enum
import math
import random
import numpy as np
import tcod

from engine.util import vector2, magnitude, normalize_vector

from engine.rendering.hues import COLOR
from content.architect.cellular_automata import Anneal, Amoeba, Conway, Life34, Bugs
from content.factories.tile_factory import TileFactory
from content.tiles.tile_defs import all_tiles, color_list
from engine.areas.area import Area
from engine.geometry.direction import Direction
from engine.geometry.circ import Circ
from engine.geometry.size import Size
from engine.geometry.point import Point
from engine.geometry.rect import Rect

from content.areas.structures.corridor import Corridor

from engine import apparata



class TerrainType(Enum):
    Plain = 0
    Swamp = 1
    Forest = 2
    Hill = 3
    Mountain = 4
    Canyon = 5
    Water = 6


class SaturationType(Enum):
    Dry = 0
    Damp = 1
    Wet = 2


class AreaFactory:
    """Build a new Area."""

    tile_factory = TileFactory()

    def __init__(
            self,
            area: Area,
        ) -> None:
        self.area = area
        self.rooms = []
        self.owned = np.zeros(area.shape, dtype=np.int)
        self.working = np.zeros(area.shape, dtype=np.int)
        self.tiles = self.area.area_model.tiles
        self.nodes = []

    def generate(self) -> Area:
        self._test_bsp_overlap()
        # self._generate_rooms(max_rooms=10, min_size=30, max_size=50)

    def generate_nodes_in_radius(
            self,
            max_nodes: int,
            min_size: int,
            max_size: int,
            radius: int
        ) -> None:
        for i in range(max_nodes):
            x, y = self.get_random_points_in_circle(radius)
            w = random.randint(min_size, max_size)
            h = random.randint(min_size, max_size)
            new_node = Rect.centered_at(center=Point(x, y), size=Size(w, h))
            self.nodes.append(new_node)

    def get_random_points_in_circle(self, radius: int):
        t = 2 * math.pi * random.random()
        u = random.random() * random.random()
        r = 2 - u if u > 1 else u
        x = int(radius * r * math.cos(t) + (256 // 2))
        y = int(radius * r * math.sin(t) + (256 // 2))
        return x, y

    def _test_generate_from_corridor(self):
        S = Rect.centered_at(center=Point(128, 128), size=Size(30, 30))
        self.tiles.T[S.outer] = self.tile_factory.build(
            'bare_floor', bg=COLOR['dark dark green']
            )

        directions = [Direction.up, Direction.down, Direction.left, Direction.right]
        direction = random.choice(directions)
        corridor = Corridor(
            start=S,
            direction=direction,
            interval=6,
            count=6
            )

        for cell in corridor.cells:
            self.tiles.T[cell.outer] = self.tile_factory.build(
                'bare_floor', bg=COLOR['dark dark green'])
            self.tiles.T[cell.center] = self.tile_factory.build(
                'bare_floor', bg=COLOR['red'])

        connection = corridor.cells[len(corridor.cells)-1]
        self.tiles.T[connection.outer] = self.tile_factory.build('bare_floor', bg=(0, 0, 100))

        T = Rect.centered_at(size=Size(20, 20), center=Point(
            connection.center.x + (direction.value[0] * 10),
            connection.center.y + (direction.value[1] * 10)
            ))

        self.tiles.T[T.outer] = self.tile_factory.build('bare_floor', bg=(0, 100, 0))
        return self.area

    def _generate_path(
            self, *,
            size: int,
            min_cells: int,
            max_cells: int,
            start: Rect,
        ) -> None:
        cell_count = random.randint(min_cells, max_cells)
        directions = [Direction.up, Direction.down, Direction.left, Direction.right]
        direction = random.choice(directions)

        cell_list = []
        previous = start
        while cell_count > 0:
            if direction == Direction.up:
                cell = Rect.centered_at(
                    center=Point(previous.center.x, previous.top - (size // 2)),
                    size=Size(size, size))
                cell_list.append(cell)
                previous = cell

            elif direction == Direction.down:
                cell = Rect.centered_at(
                    center=Point(previous.center.x, previous.bottom + (size // 2)),
                    size=Size(size, size))
                cell_list.append(cell)
                previous = cell

            elif direction == Direction.left:
                cell = Rect.centered_at(
                    center=Point(previous.left - (size // 2), previous.center.y),
                    size=Size(size, size))
                cell_list.append(cell)
                previous = cell

            elif direction == Direction.right:
                cell = Rect.centered_at(
                    center=Point(previous.right + (size // 2) , previous.center.y),
                    size=Size(size, size))
                cell_list.append(cell)
                previous = cell

            cell_count -= 1
        return cell_list, direction

    def _test_bsp_overlap(self):
        cells = 0
        used = 0

        r = Rect.centered_at(center=Point(128, 128), size=Size(30, 30))
        s = Rect.centered_at(center=Point(128, 80), size=Size(20, 20))
        rooms = [r, s]
        for cell in self._generate_bsp(
                depth=24,
                min_width=10,
                min_height=10,
                max_horizontal_ratio=3.0,
                max_vertical_ratio=3.0,
            ):
            self.tiles.T[cell.inner] = self.tile_factory.build('bare_floor', bg=(100, 0, 0))
            cells += 1
            for room in rooms:
                if room.intersects(cell):
                    used += 1
                    self.tiles.T[cell.inner] = 0
                    self.tiles.T[cell.inner] = self.tile_factory.build('bare_floor', bg=(0, 100, 0))
        for room in rooms:
            self.tiles.T[room.outer] = self.tile_factory.build('bare_floor', bg=(0, 200, 0))
        return self.area

    def _test_box_align_process(self):
        r1 = Rect.centered_at(center=Point(128, 128), size=Size(20, 20))
        r2 = Rect.centered_at(center=Point(128, 128), size=Size(60, 60))

        offset = 0
        while r1.intersects(r2):
            r2 = r2.shift(right=offset, left=offset)
            print(r1.center, r2.center)
            print(r1.left, r2.right)
            offset += 1

        r3 = Rect.centered_at(center=Point(128, 128), size=Size(30, 30))

        offset = 0
        rects = [r1, r2]
        for rect in rects:
            while r3.intersects(rect):
                r3 = r3.shift(right=offset, left=offset)
                offset += 1

        tiles = self.area.area_model.tiles
        tiles.T[r1.outer] = self.tile_factory.build('bare_floor', bg=(100, 0, 0))
        tiles.T[r2.outer] = self.tile_factory.build('bare_floor', bg=(0, 0, 100))
        tiles.T[r3.outer] = self.tile_factory.build('bare_floor', bg=(0, 100, 0))

    def _generate_graph(self):
        """
        Notes
        ------------------------
        One way to get at how to build this is to ask what each constituent
        part of the final map should be structured as. From that I can
        generalize some basic building operations (e.g. make a room of
        x by y and make n copies, place them along an axis edge-to-edge).
        """
        graph = apparata.graph.Graph()

        S = apparata.node.Node(uid="S", number=1)
        S.data = Rect.centered_at(center=Point(128, 128), size=Size(30, 30))
        n1 = self._add_node(graph, S, Direction.right, 50)
        n2 = self._add_node(graph, n1, Direction.up, 40)
        n3 = self._add_node(graph, n2, Direction.left, 30)
        self._add_node(graph, n3, Direction.left, 55)

        for node in graph.nodes:
            self.tiles.T[
                node.data.outer
                ] = self.tile_factory.build('bare_floor', bg=(150, 0, 0))

        for edge in graph.edges:
            n = edge[0]
            m = edge[1]
            self.tiles.T[
                tcod.line_where(*n.data.center, *m.data.center)
                ] = self.tile_factory.build('bare_floor', bg=(0, 0, 150))

    def _add_node(self, graph, previous, direction, distance):
        new_node = apparata.node.Node(uid=str(self.nodes))
        x = previous.data.center.x + (distance * direction.value[0])
        y = previous.data.center.y + (distance * direction.value[1])
        w = random.randint(8, 20)
        h = random.randint(8, 20)
        new_node.data = Rect.centered_at(center=Point(x, y), size=Size(w, h))
        graph.add_edge(previous, new_node)
        self.nodes += 1
        return new_node

    def _generate_base_terrain(
            self,
            terrain: TerrainType,
            saturation: SaturationType
        ) -> None:
        pass

    def _generate_topography(self) -> None:
        # Anneal (d=0.5)        blob shapes with connected voids
        # Amoeba (d=0.15)       great for clusters of grass/foliage
        # Life34 (d=0.12-0.2)   makes cool clusters, maybe for rocks or veins
        # Conway (d=0.5)        granular shapes with large open voids
        anneal = Anneal(shape=self.area.shape, density=0.5)
        anneal.generate(iterations=10)

        amoeba = Amoeba(shape=self.area.shape, density=0.15)
        amoeba.generate(iterations=10)

        conway = Conway(shape=self.area.shape, density=0.5)
        conway.generate(iterations=10)

        map_data = np.zeros(shape=self.area.shape, dtype=np.int)
        map_data[anneal.board == 1] = 1
        map_data[amoeba.board == 1] = 2
        map_data[conway.board == 1] = 3

        tiles = self.area.area_model.tiles

        # Open everything up to bare floor
        tiles[...] = self.tile_factory.build('bare_floor', bg=(25, 40, 40))

        tiles.T[map_data == 1] = self.tile_factory.build(
            'grass_1', color=(95, 150, 95), bg=(25, 40, 40))
        tiles.T[map_data == 2] = self.tile_factory.build(
            'grass_2', color=(100, 150, 30), bg=(25, 40, 40))
        tiles.T[map_data == 3] = self.tile_factory.build(
            'bare_floor', bg=(25, 40, 40))

        # Use the inverted Anneal map (the 0 values) to "punch" the floor back out
        tiles.T[anneal.board == 0] = self.tile_factory.build(
            'boulder_1', color=COLOR['dark chocolate'], bg=(25, 40, 40))

    def _generate_rooms(
            self,
            *,
            max_rooms: int,
            min_size: int,
            max_size: int,
            floor: Optional[str] = 'bare_floor',
            wall: Optional[str] = 'bare_wall',
        ) -> Area:

        # Set everything on the map to the area's default wall type.
        # self.tiles[...] = self.tile_factory.build(wall,
        #                                           color=(100, 150, 30),
        #                                           bg=(25, 40, 40))

        # Randomize things a bit, including adding some floor tiles.
        # self._roll_asset('grass_1',
        #                  colors=[(95, 150, 95),
        #                          (90, 160, 60),
        #                          (100, 150, 30)],
        #                  bgs=[(25, 40, 40)],
        #                  threshold=30)

        # self._roll_asset('grass_2',
        #                  colors=[(95, 150, 95),
        #                          (90, 160, 60),
        #                          (100, 150, 30)],
        #                  bgs=[(25, 40, 40)],
        #                  threshold=30)

        # Start building rooms.
        for _ in range(max_rooms):
            w = random.randint(min_size, max_size)
            h = random.randint(min_size, max_size)
            x = random.randint(0, self.area.width - w - 1)
            y = random.randint(0, self.area.height - h - 1)

            new_room: Rect = Rect.from_edges(left=x, top=y, right=x+w, bottom=y+h)

            # Check for intersections and try again if found.
            if any(new_room.intersects(other) for other in self.rooms):
                continue

            # Connect a new room to an existing room.
            # self._generate_tunnels(new_room)

            # Clear the inner portion of the room to the default floor type.
            self.tiles.T[new_room.outer] = self.tile_factory.build(
                floor, bg=COLOR['red']
                )
            self.tiles.T[new_room.inner] = self.tile_factory.build(
                floor, bg=COLOR['dark red']
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
        # This is an unholy abomination that needs to be banished from this class

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

    def _generate_bsp(
            self, *,
            depth: int,
            min_width: int,
            min_height: int,
            max_horizontal_ratio: float,
            max_vertical_ratio: float
        ) -> Generator[Rect, None, None]:
        bsp = tcod.bsp.BSP(x=0, y=0, width=256, height=256)
        bsp.split_recursive(
            depth=depth,
            min_width=min_width,
            min_height=min_height,
            max_horizontal_ratio=max_horizontal_ratio,
            max_vertical_ratio=max_vertical_ratio,
            )

        for node in bsp.in_order():
            if node.children:
                pass
            else:
                room = Rect.from_edges(
                    left=node.x,
                    top=node.y,
                    right=node.x + node.w,
                    bottom=node.y + node.h
                    )
                yield room

    def _generate_cellular(self):
        pass

    @property
    def start_tile(self):
        return self.rooms[0].center


class AreaPainter:

    def __init__(self, area: Area, colors, bgs) -> None:
        self.area = area
        self.colors = colors
        self.bgs = bgs

    def paint_area(self):
        pass

    def _paint_base_terrain(self):
        pass

    def _paint_topography(self):
        pass

    def _paint_terrain(self):
        pass

    def _paint_settlements(self):
        pass

    def _paint_paths(self):
        pass

    def _paint_structures(self):
        pass
