from __future__ import annotations

from typing import Iterable, Self

from . import condition, prefix
from ..obj import ArcPair, Transition


class Event(Transition):
    """Класс события развертки"""
    def __init__(self,
                 name: str | None = None,
                 label: Transition | None = None,
                 arcs: Iterable[tuple[condition.Condition, ArcPair]] | None = None) -> None:
        super().__init__(name, arcs)
        self.net: prefix.Prefix | None = None
        self._label = label

    @classmethod
    def bound(cls, net: prefix.Prefix, index: int) -> Self:
        return super().bound(net, index)

    @property
    def label(self) -> Transition:
        """Переход, которым помечено условие"""
        if self.is_bound:
            return self.net.e_labels[self.index]

        return self._label

    def on_add(self, net: prefix.Prefix, index: int) -> None:
        super().on_add(net, index)
        net.e_labels[index] = self._label
