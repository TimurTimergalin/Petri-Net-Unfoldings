from __future__ import annotations

from typing import Generator, cast, Callable

from . import event
from . import condition
from ..obj import PetriNet, Place, Transition, place, transition


class Prefix(PetriNet):
    """Класс префикса развертки сети Петри

    Новые аттрибуты:

    c_labels -- массив мест, которыми помечены условия развертки

    e_labels -- массив переходов, которыми помечены события развертки
    """
    def __init__(self) -> None:
        super().__init__()
        self.c_labels: list[Place] = []
        self.e_labels: list[Transition] = []
        self.c_counter = 1
        self.e_counter = 0

    @property
    def place_factory(self) -> Callable[[PetriNet, int], condition.Condition]:
        return condition.Condition.bound

    @property
    def transition_factory(self) -> Callable[[PetriNet, int], event.Event]:
        return event.Event.bound

    def add_place(self, p: place.Place) -> None:
        assert isinstance(p, condition.Condition)
        p._name = f"c{self.c_counter}"
        self.c_counter += 1
        super().add_place(p)

    def add_transition(self, t: transition.Transition) -> None:
        assert isinstance(t, event.Event)
        t._name = f"e{self.e_counter}"
        self.e_counter += 1
        super().add_transition(t)

    def places(self) -> Generator[condition.Condition, None, None]:
        for c in super().places():
            yield cast(condition.Condition, c)

    def transitions(self) -> Generator[event.Event, None, None]:
        for e in super().transitions():
            yield cast(event.Event, e)
