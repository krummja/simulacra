
from simulacra.ecs.components.actor import Actor
from simulacra.ecs.components.motility import Motility
from simulacra.ecs.components.player import Player
from simulacra.ecs.components.position import Position
from simulacra.ecs.components.renderable import Renderable
from simulacra.ecs.components.tile import Tile
from simulacra.ecs.components.sprite import Sprite
from simulacra.ecs.components.obstacle import Obstacle


def all_components():
    return [
        Actor,
        Motility,
        Player,
        Position,
        Renderable,
        Tile,
        Sprite,
        Obstacle
        ]
