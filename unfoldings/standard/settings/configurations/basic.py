from abc import ABC
from typing import Iterator, cast

from ....prefix_obj import Event
from ..abstract import Configuration
from .length_settings import LengthSettings


class BasicConfiguration(Configuration):
    def __init__(self, event: Event) -> None:
        self.events: set[Event] = set()
        self._init(event, self.events)

    def _init(self, event: Event, st: set[Event]) -> None:
        if event in st:
            return
        st.add(event)

        for c, _ in event.preset:
            if c.input is not None:
                self._init(c.input, st)

    def __iter__(self) -> Iterator[Event]:
        return iter(self.events)

    def __len__(self) -> int:
        return len(self.events)


class BasicConfigurationSettings(LengthSettings, ABC):
    def _config_constructor(self, event: Event) -> BasicConfiguration:
        return BasicConfiguration(event)

    def create_config(self, event: Event) -> BasicConfiguration:
        return cast(BasicConfiguration, super().create_config(event))

    def compare_events(self, event1: Event, event2: Event) -> int:
        return self.configuration_length(event1) - self.configuration_length(event2)
