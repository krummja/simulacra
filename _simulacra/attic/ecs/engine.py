from __future__ import annotations
from typing import Dict
from abc import ABC
from uuid import uuid1

from ecs.entity import Entity
from ecs.component import Component


class Registry(ABC):

    def __init__(self, ecs: Engine) -> None:
        self.ecs = ecs


class ComponentRegistry(Registry):
    _definitions: Dict[str, Component] = {}

    def register(self, component: Component):
        self._definitions[component.uid] = component

    def create(self, type_or_class, properties):
        pass


class EntityRegistry(Registry):
    _entities: Dict[str, Entity] = {}

    def register(self, entity: Entity):
        self._entities[entity.uid] = entity

    def create(self, uid: str) -> Entity:
        entity = Entity(uid, self.ecs)
        self.register(entity)
        return entity

    def destroy(self, entity: Entity) -> None:
        entity.destroy()

    def get(self, uid: str) -> Entity:
        return self._entities[uid]


class Engine:

    def __init__(self) -> None:
        self.components = ComponentRegistry(self)
        self.entities = EntityRegistry(self)

    def generate_uid(self) -> str:
        return uuid1().hex

    def create_entity(self, uid: str) -> Entity:
        return self.entities.create(uid)

    def register_component(self, component: Component) -> None:
        self.components.register(component)

    def get_entity(self, uid: str) -> Entity:
        return self.entities.get(uid)

    def create_component(self, component_type, properties) -> None:
        self.components.create(component_type, properties)
