from __future__ import annotations
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from engine.entities.entity import Entity
    from engine.components.component import Component
    from engine.model import Model


class DataManager:

    def __init__(self, model: Model) -> None:
        self._model = model

    def query(
            self,
            entity: Optional[str] = None,
            component: Optional[str] = None,
            key: Optional[str] = None,
            exclude: Optional[str] = None,
        ) -> Optional[Dict[str, Any]]:
        """Submit a query to get back a usable result.

            Entity  Component   Key     Returns
            ---------------------------------------------------------------
            Value   Value       Value   Data in Key on Component on Entity
            ---     Value       Value   Data in Key on all Component
            Value   Value       ---     Component on Entity
            ---     Value       ---     All Component
            Value   ---         ---     Entity
            ---     ---         ---     All Entity
        """
        self.exclude = exclude

        if component is not None and entity is not None:
            if key is not None:
                return self._try_get_value(entity, component, key)
            else:
                return self._try_get_component(entity, component)
        elif entity is not None:
            return self._try_get_entity(entity)
        elif component is not None:
            if key is not None:
                return self._get_all_values(component, key)
            else:
                return self._get_all_component(component)
        else:
            return self._get_all_entities()

    def _get_all_entities(self) -> List[Entity]:
        """Return a list of all entities that own actors."""
        return [actor.owner for actor in self._model.actors]

    def _try_get_entity(self, entity_name: str) -> Optional[Entity]:
        """Try to return a specific entity from the actor set."""
        for actor in self._model.actors:
            if actor.owner.uid == entity_name:
                return actor.owner
            else:
                pass

    def _get_all_components(self) -> List[Dict[str, Component]]:
        """Get all components from all entities."""
        all_entities = self._get_all_entities()
        components = []
        for entity in all_entities:
            if entity.uid == self.exclude:
                continue
            else:
                for component in entity.components.values():
                    components.append({entity.uid: component})
        return components

    def _try_get_component(
            self,
            entity_name: str,
            component_name: str
        ) -> Component:
        """Try to return a specific component on a specific entity."""
        if entity_name is not None:
            entity = self._try_get_entity(entity_name)
        if entity is not None:
            try:
                return entity.components[component_name]
            except KeyError:
                print(f"Entity {entity_name} has no component {component_name}!")

    def _get_all_values(
            self,
            component_name: str,
            key: str
        ) -> List[Dict[str, Any]]:
        """Get all values for a specified component on all entities."""
        all_components: List[Dict[str, Component]] = self._get_all_components()
        results = []
        for item in all_components:
            for k, v in item.items():
                if v.uid == component_name:
                    results.append({k: v[key]})
        return results

    def _get_all_component(
            self,
            component_name: str
        ) -> List[Dict[str, Component]]:
        """Get all instances of a specified component, keyed to entity."""
        component_list = []
        for item in self._get_all_components():
            for k, v in item.items():
                if v.uid == component_name:
                    component_list.append({k: v})
        return component_list

    def _try_get_value(
            self,
            entity_name: str,
            component_name: str,
            key: str
        ) -> Any:  # TODO: Create reliable data types for this
        """Try to get a specified value from a specified component on
        a specified entity.
        """
        all_values = self._get_all_values(component_name, key)
        if len(all_values) > 0:
            for item in all_values:
                try:
                    return item[entity_name]
                except KeyError:
                    pass
