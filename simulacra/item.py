from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Type, TYPE_CHECKING

from entity import Entity

if TYPE_CHECKING:
    from location import Location
    from component import Component


class Item(Entity):
    """
    Items have:
        - a material, a type, and can be used
        - stats
        - a rarity, a level, and a value
    Items can:
        - be sharpened, altered, destroyed, and repaired
        - be held and displayed
        - be painted, customized, and engraved
    """

    def __init__(
            self,
            name: str = "",
            description: str = "",
            location: Location = None
        ) -> None:
        super().__init__(location)
        self._name = name
        self._description = description

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    def copy(self):
        new_item = Item(self._name, self._description, self.location)
        return super().copy_to(new_item)

# class Item(Entity):
#
#     ident = '<unset>'
#     _container = None
#
#     @property
#     def container(self):
#         return self._container
#
#     @container.setter
#     def container(self, value) -> None:
#         self._container = value
#
#     @classmethod
#     def place(
#             cls,
#             char: int,
#             color: Tuple[int, int, int],
#             noun_text: str,
#             location: Location,
#             components: Optional[List[Type[Component]]] = None,
#             component_configs: Optional[Dict[str, Any]] = None,
#         ) -> None:
#         self = cls(location)
#         self.char = char
#         self.color = color
#         self.noun_text = noun_text
#
#         if components is not None:
#             for component in components:
#                 self.components.add(component(self))
#
#                 if component_configs is not None:
#                     for key, value in component_configs.items():
#                         self.components[key].configure(**value)
#
#         try:
#             self.bg = self.location.area.area_model.get_bg_color(*location.xy)
#             location.area.item_model.items[location.xy].append(self)
#         except KeyError:
#             location.area.item_model.items[location.xy] = [self]
#
#     @classmethod
#     def give(cls) -> None:
#         pass
