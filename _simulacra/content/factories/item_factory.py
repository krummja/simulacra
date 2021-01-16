from __future__ import annotations
from typing import TYPE_CHECKING

from content.items.items import item_templates
from engine.entities.item import Item

if TYPE_CHECKING:
    from engine.areas.location import Location
    from engine.model import Model
    from factories.factory_service import FactoryService


class ItemFactory:

    def __init__(self) -> None:
        self._model = None
        self.instance_count = {}

    @property
    def model(self) -> Model:
        return self._model

    @model.setter
    def model(self, value: Model) -> None:
        self._model = value

    def build(self, uid: str, location: Location):
        template = item_templates[uid]
        if template:
            return self._assemble_template(template, location)
        else:
            raise Exception(f"Could not find template for UID {uid}")

    def _assemble_template(self, template, location) -> Item:
        instance_id = 0

        if template['uid'] in self.instance_count:
            instance_id = self.instance_count[template['uid']]
            self.instance_count[template['uid']] += 1
        else:
            self.instance_count[template['uid']] = 1

        instance_uid = template['uid'] + "_" + str(instance_id)
        new_instance = Item(
            uid=instance_uid,
            name=template['name'],
            description=template['description'],
            display=template['display'],
            location=location,
            slot=template['slot']
            )

        # for definition in template['components']:
        #     name = definition[0]
        #     config = definition[1]
        #     new_instance.register_component(
        #         component_templates[name](**config))

        area = self.model.area_data.current_area
        try:
            area.item_model.items[location.xy].append(new_instance)
            new_instance.bg = area.area_model.get_bg_color(*location.xy)
        except KeyError:
            area.item_model.items[location.xy] = [new_instance]

        return new_instance
