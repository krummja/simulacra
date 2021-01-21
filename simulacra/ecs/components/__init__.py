
from simulacra.ecs.components.actor import Actor
from simulacra.ecs.components.motility import Motility
from simulacra.ecs.components.player import Player
from simulacra.ecs.components.position import Position
from simulacra.ecs.components.renderable import Renderable


def all_components():
    return [
        Actor,
        Motility,
        Player,
        Position,
        Renderable
        ]
