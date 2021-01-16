from __future__ import annotations
from typing import Dict, TYPE_CHECKING

from config import *
from engine.rendering import COLOR

from interface.elements.base_element import BaseElement, ElementConfig
from .base_menu_view import BaseMenuView

if TYPE_CHECKING:
    from tcod.console import Console
    from engine.states.base_menu_state import BaseMenuState
    from engine.components.equipment import EquipmentSlot


class EquipmentSlotElement:

    def __init__(self, parent: EquipmentMenuView, data: EquipmentSlot, index: int) -> None:
        self.parent = parent
        self.index = index

        if data[self.index].item is not None:
            self.char = data[self.index].renderables['char']
            self.color = data[self.index].renderables['color']
            self.fg = (255, 255, 255)
            self.name = data[self.index].renderables['name']
            self.description = data[self.index].renderables['description']
        else:
            self.char = ord("-")
            self.color = (100, 100, 100)
            self.fg = (100, 100, 100)
            self.name = data[self.index].slot
            self.description = ""

    def draw(self, i: int, consoles: Dict[str, Console]) -> None:
        selected = (255, 0, 255)

        consoles['ROOT'].tiles_rgb[["ch", "fg"]][
            self.parent.y + i + 2,
            self.parent.x + 2
            ] = self.char, self.color

        consoles['ROOT'].print(
            x = self.parent.x + 4,
            y = self.parent.y + 2 + i,
            string = self.name,
            fg = selected if self.index == self.parent._state.selection else self.fg
            )


class EquipmentMenuView(BaseMenuView):

    def __init__(self, state: BaseMenuState) -> None:
        super().__init__(
            state = state,
            config=ElementConfig(
                position=("bottom", "right"),
                width=SIDE_PANEL_WIDTH,
                height=(SIDE_PANEL_HEIGHT // 2) + 2,
                fg=(255, 255, 255),
                title="EQUIPMENT",
                framed=True,
                frame_fg=(255, 0, 255)
                ))

        data = self._state.data

        self.lhand_slot = EquipmentSlotElement(self, data, 0)
        self.rhand_slot = EquipmentSlotElement(self, data, 1)

        self.head_slot = EquipmentSlotElement(self, data, 2)
        self.neck_slot = EquipmentSlotElement(self, data, 3)
        self.shoulders_slot = EquipmentSlotElement(self, data, 4)
        self.arms_slot = EquipmentSlotElement(self, data, 5)
        self.hands_slot = EquipmentSlotElement(self, data, 6)
        self.torso_slot = EquipmentSlotElement(self, data, 7)
        self.back_slot = EquipmentSlotElement(self, data, 8)
        self.waist_slot = EquipmentSlotElement(self, data, 9)
        self.legs_slot = EquipmentSlotElement(self, data, 10)
        self.feet_slot = EquipmentSlotElement(self, data, 11)

    def draw_content(self, consoles: Dict[str, Console]) -> None:
        self.draw_help(consoles)
        self.draw_equipment(consoles)

        consoles['ROOT'].draw_frame(
            x=0, y=0,
            width=STAGE_PANEL_WIDTH, height=STAGE_PANEL_HEIGHT,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
            )

    def draw_equipment(self, consoles: Dict[str, Console]) -> None:

        self.lhand_slot.draw(0, consoles)
        self.rhand_slot.draw(2, consoles)

        self.head_slot.draw(5, consoles)
        self.neck_slot.draw(7, consoles)
        self.shoulders_slot.draw(9, consoles)
        self.arms_slot.draw(11, consoles)
        self.hands_slot.draw(13, consoles)
        self.torso_slot.draw(15, consoles)
        self.back_slot.draw(17, consoles)
        self.waist_slot.draw(19, consoles)
        self.legs_slot.draw(21, consoles)
        self.feet_slot.draw(23, consoles)
