from __future__ import annotations
from typing import TYPE_CHECKING

from interface_element import InterfaceElement
from data.interface_elements import interface_templates

if TYPE_CHECKING:
    from model import Model


class InterfaceFactory:
    
    def __init__(self) -> None:
        self.instance_count = {}
        
    def build(self, uid: str):
        template = interface_templates[uid]
        if template:
            return self._assemble_template(template)
        else:
            raise Exception(f"Could not find template UID {uid}")
    
    def _assemble_template(self, template):
        instance_id = 0
        
        if template['uid'] in self.instance_count:
            instance_id = self.instance_count[template['uid']]
            self.instance_count[template['uid']] += 1
        else:
            self.instance_count[template['uid']] = 1
        
        instance_uid = template['uid'] + "_" + str(instance_id)
        
        # TODO: Instead of passing in content from the template, I could have different assemblers for interface content, then pass that content in. That would work fine for string content.
        new_instance = InterfaceElement(
            uid=instance_uid,
            x=template['position']['x'],
            y=template['position']['y'],
            width=template['size']['width'],
            height=template['size']['height'],
            title=template['name'],
            string=template['content']
            )
        return new_instance