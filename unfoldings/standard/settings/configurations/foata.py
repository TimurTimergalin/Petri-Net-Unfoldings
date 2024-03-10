from abc import ABC
from typing import Iterator, cast
from itertools import chain

from ....prefix_obj import Event
from ..abstract import Configuration
from .length_settings import LengthSettings


class FoataConfiguration(Configuration):
    def __init__(self, event: Event) -> None:
        self.events: list[list[Event]] = []
        self._init(event)
        self.events.reverse()

    def _init(self, event: Event, met: set[Event] | None = None, before: int = 0) -> None:
        if met is None:
            met = set()

        met.add(event)

        if before == 0:
            self.events.append([event])
            before += 1
        else:
            self.events[-before].append(event)

        for c, _ in event.preset:
            if c.input is not None:
                self._init(c.input, met, before - 1)

    def __iter__(self) -> Iterator[Event]:
        return chain.from_iterable(self.events)

    def __len__(self) -> int:
        return sum(1 for _ in self)


class FoataConfigurationSettings(LengthSettings, ABC):
    def _config_constructor(self, event: Event) -> FoataConfiguration:
        return FoataConfiguration(event)

    def create_config(self, event: Event) -> FoataConfiguration:
        return cast(FoataConfiguration, super().create_config(event))

    def compare_events(self, event1: Event, event2: Event) -> int:
        length_cmp = self.configuration_length(event1) - self.configuration_length(event2)
        if length_cmp != 0:
            return length_cmp

        labels1 = sorted(x.comparable_label for x in self.create_config(event1))
        labels2 = sorted(x.comparable_label for x in self.create_config(event2))

        if labels1 < labels2:
            return -1
        elif labels1 > labels2:
            return 1

        foata_normal_form1 = [sorted(y.comparable_label
                                     for y in x)
                              for x in self.create_config(event1).events]
        foata_normal_form2 = [sorted(y.comparable_label
                                     for y in x)
                              for x in self.create_config(event2).events]

        if foata_normal_form1 < foata_normal_form2:
            return -1
        if foata_normal_form1 > foata_normal_form2:
            return 1
        return 0
