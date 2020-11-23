from __future__ import annotations
from typing import TYPE_CHECKING

from character import Character
from data.characters import character_templates

if TYPE_CHECKING:
    from model import Model
    from factories.factory_service import FactoryService


class CharacterFactory:

    def __init__(
            self,
            model: Model,
            factory_service: FactoryService
        ) -> None:
        self.model = model
        self.factory_service = factory_service
        self.template_instance_count = {}

    def build(self, uid, location):
        """Builds a character instance from a template using this uid.

        :param uid: uid of the template to instantiate.
        :param location: map position to spawn the instance.
        :return: Built instance from specified template.
        """
        character_template = character_templates[uid]
        if character_template:
            return self._create_template_instance(character_template, location)
        else:
            raise Exception(f"Could not find template for UID {uid}")

    def _create_template_instance(self, character_template, location) -> Character:
        instance_id = 0
        if character_template['uid'] in self.template_instance_count:
            instance_id = self.template_instance_count[character_template['uid']]
            self.template_instance_count[character_template['uid']] += 1
        else:
            self.template_instance_count[character_template['uid']] = 1

        instance_uid = character_template['uid'] + "_" + str(instance_id)
        new_instance = Character(
            uid=instance_uid,
            name=character_template['name'],
            location=location,
            display=character_template['display'],
            control=character_template['control']
            )
        self.model.entity_data.register(new_instance)
        return new_instance
