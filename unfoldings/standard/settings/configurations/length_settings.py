from ....prefix_obj import Event
from ..abstract import Settings, Configuration

from abc import ABC, abstractmethod


class LengthSettings(Settings, ABC):
    def __init__(self) -> None:
        super().__init__()
        self.saved: dict[Event, int] = {}

    @abstractmethod
    def _config_constructor(self, event: Event) -> Configuration:
        pass

    def configuration_length(self, event: Event) -> int:
        if event not in self.saved:
            self.create_config(event)

        return self.saved[event]

    def create_config(self, event: Event) -> Configuration:
        res = self._config_constructor(event)
        if event not in self.saved:
            self.saved[event] = len(res)
        return res
