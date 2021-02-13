from __future__ import annotations
from typing import Dict, TYPE_CHECKING

from simulacra.data.areas.unnamed_area import UnnamedArea
from .manager import Manager
from simulacra.world.area import Area

if TYPE_CHECKING:
    from .game import Game


class OverworldBuilder:

    def __init__(self) -> None:
        pass


# class RegionAlphaBuilder(InitRegion, AbstractRegionBuilder, RegionAlphaMixin):
#     pass

class RegionAlphaBuilder:
    pass


class Region:
    def __init__(self, name, areas):
        self.name = name
        self.areas = areas


class WorldBuilder:

    def __init__(self, manager: WorldManager) -> None:
        self.manager = manager
        self.builder = None

    def overworld(self):
        self.builder = OverworldBuilder()

    def core_plot(self, nodes):
        self.builder = RegionAlphaBuilder(nodes[0])
        alpha = self.get_region()
        return alpha

    def get_region(self):
        region = Region('NAME_UNDEFINED', 'AREAS_UNDEFINED')
        name = self.builder.get_name()
        region.name = name

        areas = self.builder.get_areas()
        region.areas = areas

        return region


class WorldManager(Manager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.build = WorldBuilder(self)
        self.regions = None
        self.current_region = None
        self.current_area = self.new()


    def new(self):
        """Builds a new Overworld consisting of a selection of Regions, where each
        Region contains a selection of Areas."""
        area = Area(self)
        area.initialize_area()
        return area

        # regions = {}
        # overworld, nodes = self.build.overworld()
        # regions[overworld.name] = overworld

        # alpha = self.build.core_plot(nodes)
        # regions[alpha.name] = alpha

        # self.regions = regions
        # self.current_region = regions['alpha']
        # self.current_area = regions['alpha'].areas[0]
