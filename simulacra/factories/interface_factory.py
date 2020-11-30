from __future__ import annotations
from typing import TYPE_CHECKING

from views.elements.base_element import BaseElement, BaseRenderable
from data.interface_elements import interface_templates

if TYPE_CHECKING:
    from model import Model


class InterfaceFactory:
    
    def __init__(self) -> None:
        self.instance_count = {}
        
    def build(self, uid: str):
        template = interface_templates[uid]
        x = template['x']
        y = template['y']
        width = template['width'] 
        height = template['height']
        try:
            framed = template['framed']
        except KeyError:
            framed = False
        try:
            title = template['title']
        except KeyError:
            title = ""
        try:
            fg = template['fg']
        except KeyError:
            fg = (255, 255, 255)
        try:
            bg = template['bg']
        except KeyError:
            bg = (0, 0, 0)
        
        config = {
            'x': x, 'y': y, 'width': width, 'height': height,
            'framed': framed, 'title': title, 'fg': fg, 'bg': bg
        }
        renderable = template['renderable']    
        
        if template:
            return self._assemble_template(uid, config, renderable)
        else:
            raise Exception(f"Could not find template UID {uid}")
    
    def _assemble_template(self, template_uid, template_config, renderable):
        instance_id = 0
        
        if template_uid in self.instance_count:
            instance_id = self.instance_count[template_uid]
            self.instance_count[template_uid] += 1
        else:
            self.instance_count[template_uid] = 1
        
        instance_uid = template_uid + "_" + str(instance_id)
        new_instance = BaseElement(
            uid=instance_uid,
            **template_config
            )
        new_instance.renderable = renderable(new_instance)
        
        return new_instance