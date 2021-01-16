from __future__ import annotations
from typing import TYPE_CHECKING

from engine.entities.character import Character

if TYPE_CHECKING:
    from engine.areas.location import Location
    from engine.model import Model
    from factories.factory_service import FactoryService


class CharacterFactory:

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
        """Builds a character instance from a template using this uid.

        :param uid: uid of the template to instantiate.
        :param location: map position to spawn the instance.
        :return: Built instance from specified template.
        """
        # FIXME
        template = None
        if template:
            return self._assemble_template(template, location)
        else:
            raise Exception(f"Could not find template for UID {uid}")

    def _assemble_template(self, template, location) -> Character:
        instance_id = 0

        if template['uid'] in self.instance_count:
            instance_id = self.instance_count[template['uid']]
            self.instance_count[template['uid']] += 1
        else:
            self.instance_count[template['uid']] = 1

        instance_uid = template['uid'] + "_" + str(instance_id)
        new_instance = Character(
            uid=instance_uid,
            name=template['name'],
            location=location,
            display=template['display'],
            )
        self.model.entity_data.register(new_instance)
        return new_instance