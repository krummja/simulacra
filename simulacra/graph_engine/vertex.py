from __future__ import annotations
from typing import Optional

class Vertex:
    
    def __init__(
            self, 
            vid: str, 
            label: Optional[str] = None, 
            number: Optional[int] = None
        ) -> None:
        self.vid = vid
        self.label = label
        self.number = number
        self.degree = 0
        self.candidates = []
        
    @staticmethod
    def make_name(label, number):
        if label is None and number is None:
            return ''
        if number is None:
            return label
        if label is None:
            return str(number)
        else:
            return f"{label}, {number}"
    
    @property
    def name(self):
        return self.make_name(self.label, self.number)
    
    def __str__(self) -> str:
        return (f"{self.vid}, {self.label}, "
                f"{self.number if self.number is not None else ''}")