from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Type, TYPE_CHECKING

from entity import Entity
from actions import common

if TYPE_CHECKING:
    from action import Action, ActionWithItem
    from location import Location
    from component import Component


class ItemOption:

    def __init__(self, item: Item, text: str, command: Action):
        self.char = ord("-")
        self.color = (100, 100, 100)
        self.noun_text = text
        self.command = command


class Item(Entity):

    def __init__(
            self,
            uid: str = "",
            name: str = "",
            description: str = "",
            location: Optional[Location] = None,
            display: Optional[Dict[str, Any]] = None,
        ) -> None:
        super().__init__(location)
        
        # Basic properties
        self.uid = uid
        self._name = name
        self._owner = None
        self._location = location
        
        # TODO: Make a Description component
        self._description = description
        
        # Display Properties
        self.char = display['char']
        self.color = display['color']
        self.bg = display['bg']
  
    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def owner(self):
        return self._owner
    
    @owner.setter
    def owner(self, value) -> None:
        self._owner = value

    @property
    def location(self):
        return self._location
    
    @location.setter
    def location(self, value) -> None:
        self._location = value

    def copy(self):
        new_item = Item(
            self.uid,
            self._name,
            self._description,
            self.location
            )
        return super().copy_to(new_item)

    def __eq__(self, other: Item):
        return (self.uid == other.uid,
                self.name == other.name,
                self.description == other.description)
    
    def __ne__(self, other: Item):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash((self.uid, self.name, self.description))
        
    def lift(self) -> None:
        """Remove this item from any of its containers."""
        if self.owner:
            self.owner.remove(self)
            self.owner = None
        if self.location:
            item_list = self.location.area.items[self.location.xy]
            item_list.remove(self)
            if not item_list:
                del self.location.area.items[self.location.xy]
            self.location = None
            
    def place(self, location: Location) -> None:
        """Place this item on the floor at the given location."""
        assert not self.location, "This item already has a location."
        assert not self.owner, "Can't be placed because this item is currently owned."
        self.location = location
        items = location.area.items
        try:
            self.bg = location.area.area_model.get_bg_color(*location.xy)
            items[location.xy].append(self)
        except KeyError:
            items[location.xy] = [self]
            
    def plan_activate(self, action: ActionWithItem) -> ActionWithItem:
        return action
    
    def act_activate(self, action: ActionWithItem) -> None:
        raise Impossible(f"you can do nothing with the {self.noun_text}!")
    
    def consume(self, action: ActionWithItem) -> None:
        pass

    def __repr__(self):
        return repr(f"{self._name} : {self.char} : {self.equippable} : {self.slot}")