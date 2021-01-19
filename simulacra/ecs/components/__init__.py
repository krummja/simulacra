__all__ = ['Position', 'Renderable']

from simulacra.ecs.components.position import Position
from simulacra.ecs.components.renderable import Renderable

def all_components():
    return [
        Position,
        Renderable
        ]
