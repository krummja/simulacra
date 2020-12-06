from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING
from abc import abstractmethod


class Effect:
    
    def __init__(
            self, 
            console, 
            start_frame=0, 
            stop_frame=0, 
            delete_count=None
        ) -> None:
        self._console = console
        self._start_frame = start_frame
        self._stop_frame = stop_frame
        self._delete_count = delete_count

    def update(self, frame_n):
        pass

    @abstractmethod
    def reset(self):
        pass
    
    @abstractmethod
    def _update(self, frame_n):
        pass
    
    @abstractmethod
    @property
    def stop_frame(self):
        pass
    
    @property
    def delete_count(self):
        return self._delete_count
    
    @property
    def console(self):
        return self._console
    
    @delete_count.setter
    def delete_count(self, value):
        self._delete_count = value
        
    @property
    def frame_update_count(self):
        return 1
    
    def process_event(self, event):
        return event