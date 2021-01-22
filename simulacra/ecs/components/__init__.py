
from simulacra.ecs.components.actor import Actor
from simulacra.ecs.components.motility import Motility
from simulacra.ecs.components.player import Player
from simulacra.ecs.components.position import Position
from simulacra.ecs.components.renderable import Renderable
from simulacra.ecs.components.tile import Tile


def all_components():
    return [
        Actor,
        Motility,
        Player,
        Position,
        Renderable,
        Tile
        ]
