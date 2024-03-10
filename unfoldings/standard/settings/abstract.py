from abc import ABC, abstractmethod

from typing import Iterator, Any

from collections import Counter

from ...obj import Place
from ...prefix_obj import Event
from ...obj import Marking


# Скопированная реализация collections.Counter._keep_positive (это внутренний метод, его присутствие не гарантированно
# во всех версиях python)
def keep_positive(counter: Counter[Any]) -> None:
    non_positive = [elem for elem, count in counter.items() if not count > 0]
    for elem in non_positive:
        del counter[elem]


class Configuration(ABC):
    @abstractmethod
    def __init__(self, event: Event) -> None:
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[Event]:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    def mark(self) -> Marking:
        res: Counter[Place] = Counter()

        for e in self:
            preset_marking = Marking(c.label for c, _ in e.preset)
            postset_marking = Marking(c.label for c, _ in e.postset)
            res.update(postset_marking)
            res.subtract(preset_marking)

        keep_positive(res)
        return Marking(res)


class Settings(ABC):
    @abstractmethod
    def compare_events(self, event1: Event, event2: Event) -> int:
        pass

    @abstractmethod
    def create_config(self, event: Event) -> Configuration:
        pass

    @abstractmethod
    def check_cutoff(self, event: Event) -> bool:
        pass

    @abstractmethod
    def update_cutoff(self, event: Event) -> None:
        pass

    @abstractmethod
    def check_and_update_cutoff(self, event: Event) -> bool:
        cond = self.check_cutoff(event)

        if not cond:
            self.update_cutoff(event)

        return cond
