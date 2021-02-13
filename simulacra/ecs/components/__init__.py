
from simulacra.ecs.components.actor import Actor
from simulacra.ecs.components.blocker import Blocker
from simulacra.ecs.components.motility import Motility
from simulacra.ecs.components.is_player import IsPlayer
from simulacra.ecs.components.position import Position
from simulacra.ecs.components.renderable import Renderable
from simulacra.ecs.components.tile import Tile
from simulacra.ecs.components.sprite import Sprite
from simulacra.ecs.components.name import Name
from simulacra.ecs.components.opaque import Opaque


def all_components():
    return [
        Actor,
        Blocker,
        Motility,
        IsPlayer,
        Position,
        Renderable,
        Tile,
        Sprite,
        Name,
        Opaque,
        ]
