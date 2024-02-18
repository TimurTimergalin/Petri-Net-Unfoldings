from __future__ import annotations

from typing import Iterable, Self

from . import event, prefix
from ..obj import ArcPair, Place


class Condition(Place):
    """Класс условия развертки"""
    def __init__(self,
                 name: str | None = None,
                 label: Place | None = None,
                 arcs: Iterable[tuple[event.Event, ArcPair]] | None = None) -> None:
        super().__init__(name, arcs)
        self.net: prefix.Prefix | None = None
        self._label = label

    @classmethod
    def bound(cls, net: prefix.Prefix, index: int) -> Self:
        return super().bound(net, index)

    @property
    def label(self) -> Place:
        """Место, которым помечено условие"""
        if self.is_bound:
            return self.net.c_labels[self.index]

        return self._label

    def on_add(self, net: prefix.Prefix, index: int) -> None:
        super().on_add(net, index)
        net.c_labels[index] = self._label
